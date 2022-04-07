## Ubuntu install sublime text

Download Sublime text
----
Using wget or browser to download tarfile from 
[https://download.sublimetext.com/sublime_text_3_build_3126_x64.tar.bz2](https://download.sublimetext.com/sublime_text_3_build_3126_x64.tar.bz2), 

Extract tar file
----
right click to extract or using the follow command:
```
tar -jxvf sublime_text_3_build_3126_x64.tar.bz2
```

Create startup file
----
Move the extracted file to /opt directory.
```
sudo mv sublime_text_3 /opt/sublime_text
```
then, create file /usr/bin/subl to startup sublime_text,
write the follow content to file /usr/bin/subl
```
#!/bin/bash
exec '/opt/sublime_text/sublime_text "$@"'
```

Auto installation by shell script
----
```shell
#!/bin/bash

download_addr_deb="https://download.sublimetext.com/sublime-text_build-3126_amd64.deb"
download_addr_tar="https://download.sublimetext.com/sublime_text_3_build_3126_x64.tar.bz2"

sublime_source=$1

if [ -z $sublime_source ]; then
    sublime_source=./sublime_text_3_build_3126_x64.tar.bz2
fi

if [ ! -e $sublime_source ]; then
    wget $download_addr_tar
fi

# tar -jxvf sublime_text_3_build_3126_x64.tar.bz2 
tar -jxvf $sublime_source
mv sublime_text_3 /opt/sublime_text
if [ ! -e /usr/bin/subl ]; then
    touch /usr/bin/subl 
    echo -e "#!/bin/bash" >> /usr/bin/subl
    echo -e 'exec /opt/sublime_text/sublime_text "$@"' >> /usr/bin/subl
    chmod 755 /usr/bin/subl
fi
```
