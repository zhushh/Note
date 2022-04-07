#### Http热重启机制

热重启原理，就是不中断已有连接服务的情况，重新启动程序。主要需要解决两个问题：

1.不关闭当前正在监听服务的socket重启自己

2.已连接处理中的请求要么完成处理，要么超时处理



##### 主要步骤如下

- 启动程序时，监听USR2信号
- 收到信号时，fork子进程（使用相同的命令），将服务监听的socket文件描述符传递给子进程
- 子进程监听父进程的socket，这时子进程和父进程都可以接收请求
- 子进程启动成功后，发送信号通知父进程停止接收新的连接，等待旧连接处理完成（或超时）
- 父进程退出，升级完成



##### 细节处理

- 父进程将socket文件描述符传递给子进程，可以通过命令行或者环境变量等
- 子进程启动时，使用和父进程一样的命令行
- server.Shutdown()优雅关闭方法是go1.8的新特性
- server.Serve(l)方法在Shutdown时立即返回，Shutdown方法则阻塞至context完成，所以Shutdown的方法写在主goroutine中



##### 代码

```go
type SelfMacaron struct {
	*macaron.Macaron
}

var (
	server   *http.Server
	listener net.Listener
	graceful = flag.Bool("graceful", false, "listen on fd open 3 (internal use only)")
)

// 修改macaron的Run方法
func (sm *SelfMacaron) Run(host string, port int) {
	addr := host + ":" + strconv.FormatInt(int64(port), 10)
	log.Printf("listening on %s\n", addr)
	server = &http.Server{Addr: addr, Handler: sm.Macaron}

    // 初始化
	var err error
	if *graceful {
		log.Printf("graceful run\n")
		f := os.NewFile(3, "")
		listener, err = net.FileListener(f)
	} else {
		log.Printf("run\n")
		listener, err = net.Listen("tcp", server.Addr)
	}
	if err != nil {
		return
	}

    // 判断是否为子进程，如果是，发送信号关闭父进程
	if *graceful {
		parent := syscall.Getppid()
		log.Printf("main: killing parent pid:%v", parent)
		syscall.Kill(parent, syscall.SIGTERM)
	}

    // 启动服务
	go func() {
		err = server.Serve(listener)
		log.Printf("server.Serve err: %+v\n", err)
	}()
	signalHandler()
	log.Printf("signal end")
}

// 重启入口
func reload() error {
	tl, ok := listener.(*net.TCPListener)
	if !ok {
		return errors.New("listener is not tcp listener")
	}

	f, err := tl.File()
	if err != nil {
		return err
	}

	args := []string{"-graceful"}
	cmd := exec.Command(os.Args[0], args...)
	//cmd.Stdout = os.Stdout
	//cmd.Stderr = os.Stderr
	// put socket FD at the first entry
	cmd.ExtraFiles = []*os.File{f}
	return cmd.Start()
}

// 信号处理
func signalHandler() {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM, syscall.SIGUSR2)
	for {
		sig := <-ch
		log.Printf("signal: %v", sig)

		// timeout context for shutdown
		ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
		defer cancel()

		switch sig {
		case syscall.SIGINT, syscall.SIGTERM:
			// stop
			log.Printf("stop")
			signal.Stop(ch)
			server.Shutdown(ctx)
			log.Printf("graceful shutdown")
			return
		case syscall.SIGUSR2:
			// reload
			log.Printf("reload")
			err := reload()
			if err != nil {
				log.Fatalf("graceful restart error: %v", err)
			}
			server.Shutdown(ctx)
			log.Printf("graceful reload")
			return
		}
	}
}
```



##### systemd&supervisor

父进程退出后，子进程会挂到1号进程上面，这种情况下使用systemd和supervisord等管理程序会显示进程处于failed的状态，解决这个问题两个方法：

1. 使用pidfile，每次进程重启更新pidfile，让进程管理者通过这个文件感知mainpid的变更
2. 起master来管理服务进程，每次热重启master拉起一个新的进程，把旧的kil掉。这时master的pid没有变化，对于进程管理者来说进程处于正常状态。[实现方式](https://github.com/kuangchanglang/graceful)



##### Going框架实现热重启



udp server fork方法

```go
// Fork 热重启fork子进程，老进程停止接收请求
func (srv *UDPServer) Fork() (int, error) {
	SysLogf("fork udp server")
	if srv.closing {
		return 0, fmt.Errorf("udp server already forked")
	}

	file, err := srv.conn.File()
	if err != nil {
		return 0, fmt.Errorf("udp server get conn file fail:%s", err)
	}
	return StartNewProcess(0, file.Fd())
}
```



tcp server fork方法

```go
// Fork 热重启fork子进程，老进程停止接收请求
func (srv *TCPServer) Fork() (int, error) {
	SysLogf("fork tcp server")
	if srv.closing {
		return 0, fmt.Errorf("tcp server already forked")
	}
	file, err := srv.conn.File()
	if err != nil {
		return 0, fmt.Errorf("tcp server get conn file fail:%s", err)
	}
	return StartNewProcess(file.Fd(), 0)
}
```



信号处理接口

```go
// HandleSignals 监听信号
func HandleSignals(srv GracefulRestart) {
	signalChan := make(chan os.Signal)

	signal.Notify(signalChan, syscall.SIGTERM, syscall.SIGUSR2, syscall.SIGSEGV)
	SysLogf("server notify signal: SIGTERM SIGUSR2")

	for {
		sig := <-signalChan
		switch sig {
		case syscall.SIGTERM:
			attr.AttrAPI(3242880, 1) //SIGTERM软件终止信号
			SysLogf("receive SIGTERM signal, shutdown server")
			srv.Shutdown()
		case syscall.SIGSEGV:
			attr.AttrAPI(3242881, 1) //SIGSEGV段非法错误信号
			SysLogf("receive SIGSEGV signal, shutdown server")
		case syscall.SIGUSR2:
			attr.AttrAPI(3242882, 1) //SIGUSR2用户信号
			SysLogf("receive SIGUSR2 signal, graceful restarting server")
			if pid, err := srv.Fork(); err != nil {
				attr.AttrAPI(3241494, 1) //热重启fork失败
				SysLogf("start new process failed: %v, continue serving", err)
			} else {
				SysLogf("start new process succeed, the new pid is %d", pid)
				srv.Shutdown()
			}
		default:
		}
	}
}
```





https://juejin.im/entry/5a4ef011f265da3e36410f0e

https://grisha.org/blog/2014/06/03/graceful-restart-in-golang/

http://blog.nella.org/zero-downtime-upgrades-of-tcp-servers-in-go/

