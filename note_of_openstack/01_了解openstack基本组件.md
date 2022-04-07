---
name: 01_了解openstack的基本组件.md
update: 2017-04-12
date: 2017-04-12
keywords: openstack,Nova,switf,Quantum
---

OpenStack三大基本组件
----
* 虚拟机管理系统组件-Nova

    Nova在openstack中是主要负责管理虚拟机资源的组件；

* 虚拟网络管理组件-Quantum

    Quantum负责管理openstack的虚拟网络，采用的是代理模式；

* 存储管理组件-Glance与switf

    因为虚拟机Image的传输需要很大的网络带宽，所以Nova就把虚拟机的Image管理独立出去，就是Glance；
    Glance也是一个代理，设计成代理是为了方便不同客户需求，比如有公司希望使用自己的镜像就可以在Glance
    后台接入自己的虚拟机镜像管理服务，如果客户不想那么麻烦，那么可以使用开源免费的switf存储服务；
    switf不仅提供虚拟机镜像服务，还是object storage及云存储的开源实现。

