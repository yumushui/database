

参考
http://www.yunweipai.com/35237.html


----------------------

web架构介绍

http://www.yunweipai.com/35228.html

1.1：单机房架构

client  www.magedu.com
A 机房业务入口  firewall   101.200.188.230
HA proxy + keepalived    -  HA proxy  + keepalived
Nginx+PHP A   Nginx+PHP B    Nginx+PHP C 
   - Image rsync Image
   - mysql  mysql
   - Redis Server1  Redis Server2  Redis Server3

1.2  多机房架构

client  www.magedu.com
A 机房业务入口  firewall   101.200.188.230
HA proxy + keepalived    -  HA proxy  + keepalived           B 机房业务入口  firewall   101.200.188.230
Nginx+PHP A   Nginx+PHP B    Nginx+PHP C                 --  HA proxy + keepalived    -  HA proxy  + keepalived
   - Image rsync Image
   - mysql  mysql
   - Redis Server1  Redis Server2  Redis Server3

1.3  公有云架构

WEB Android  iOS    客户层
阿里云  阿里云SLB
nginx1      nginx2   负载层
前端   V1          V2              V3                   V4
    cp-front  kkb-angular  kkb-live kkb-www kkb-wx   kkb-crm
              angular      kkb-cms                   kkb-wx-new 

后端 cp-back
    cp-csft
    kkb-old-bak 

数据层   mysql   redis     rabbitmq  

管理平台  spring-boot-admin
日志平台  ELK 
Pass层    docker   k8s


1.4  私有云架构

私有云web架构

client 
DNS服务器： 223.6.6.6
浏览器： http://www.magedu.com 
firewall - firewall  101.2200.188.210   101.200.188.211
VIP 172.16.0.248/249
HA proxy 四层负载  外网IP 172.16.0.151
HA proxy + Keepalived 内网IP 10.0.0.253

Nginx web服务器 www.megedu.com  外网IP： 172.16.0.201   内网IP： 10.0.0.1
Tomcat 服务器  内网IP 10.0.0.101  - 写 mysql主库
Tomcat 服务器  内网IP 10.0.0.102  - 读 mysql从库
Tomcat 服务器  内网IP 10.0.0.103  - 文件存储服务器 nfs 主
Tomcat 服务器  内网IP 10.0.0.104  - 缓存服务器 Redis 










----------------------

负载均衡简介

http://www.yunweipai.com/35234.html

负载均衡：Load Balance，简称LB，是一种服务或基于硬件设备等实现的高可用反向代理技术，负载均衡将特定的业务(web服务、网络流量等)分担给指定的一个或多个后端特定的服务器或设备，从而提高了公司业务的并发处理能力、保证了业务的高可用性、方便了业务后期的水平动态扩展

阿里云SLB介绍 ：https://yq.aliyun.com/articles/1803

为什么使用负载均衡
Web服务器的动态水平扩展-->对用户无感知
增加业务并发访问及处理能力-->解决单服务器瓶颈问题
节约公网IP地址-->降低IT支出成本
隐藏内部服务器IP-->提高内部服务器安全性
配置简单-->固定格式的配置文件
功能丰富-->支持四层和七层，支持动态下线主机
性能较强-->并发数万甚至数十万

负载均衡类型

四层：
LVS：Linux Virtual Server
HAProxy：High Availability Proxy
Nginx：1.9版之后

七层：
HAProxy
Nginx

硬件：
F5          https://f5.com/zh
Netscaler   https://www.citrix.com.cn/products/citrix-adc/
Array       https://www.arraynetworks.com.cn/
深信服       http://www.sangfor.com.cn/
北京灵州     http://www.lingzhou.com.cn/cpzx/llfzjh/

应用场景
四层：Redis、Mysql、RabbitMQ、Memcache等
七层：Nginx、Tomcat、Apache、PHP、图片、动静分离、API等

随着公司业务的发展，公司负载均衡服务既有四层的，又有七层的，通过LVS实现四层和Nginx实现七层的负载均衡对机器资源消耗比较大，并且管理复杂度提升，运维总监要求，目前需要对前端负载均衡服务进行一定的优化和复用，能否用一种服务同既能实现七层负载均衡，又能实现四层负载均衡，并且性能高效，配置管理容易，而且还是开源。

在企业生产环境中，每天会有很多的需求变更，比如增加服务器、新业务上线、url路由修改、域名配置等等，对于前端负载均衡设备来说，容易维护，复杂度低，是首选指标。在企业中，稳定压倒一切，与其搞得很复杂，经常出问题，不如做的简单和稳定。在企业中，90%以上的故障，来源于需求变更。可能是程序bug，也可能是人为故障，也可能是架构设计问题等。前端负载均衡设备为重中之重，在软件选型上一定充分考虑，能满足业务的前提下，尽可能降低复杂度，提高易维护性

------------------------

HAProxy介绍

HAProxy是法国开发者
威利塔罗(Willy Tarreau)
在2000年使用C语言开发的一个开源软件，是一款具备高并发(一万以上)、高性能的TCP和HTTP负载均衡器，支持基于cookie的持久性，自动故障切换，支持正则表达式及web状态统计，目前最新TLS版本为2.0

历史版本：


历史版本更新功能：1.4  1.5  1.6  1.7  1.8 1.9  2.0 2.1 2.2-dev
1.8：多线程，HTTP/2缓存……
1.7：服务器动态配置，多类型证书……
1.6：DNS解析支持，HTTP连接多路复用……
1.5：开始支持SSL，IPV6，会话保持……

从2013年HAProxy 分为社区版和企业版，企业版将提供更多的特性和功能以及全天24小时的技术支持等服务。

企业版
企业版网站：https://www.haproxy.com/

社区版
社区版网站：http://www.haproxy.org/

github：https://github.com/haproxy

版本对比
功能	社区版	企业版
高级HTTP / TCP负载平衡和持久性	支持	支持
高级健康检查	支持	支持
应用程序加速	支持	支持
高级安全特性	支持	支持
高级管理	支持	支持
HAProxy Dev Branch新功能		支持
24*7 支持服务		支持
实时仪表盘		支持
VRRP和Route Health Injection HA工具		支持
ACL，映射和TLS票证密钥同步		支持
基于应用程序的高级DDoS和Bot保护(自动保护)		支持
Bot(机器人)监测		支持
Web应用防火墙		支持
HTTP协议验证		支持
实时集群追踪		支持

HAProxy功能

支持功能：
TCP 和 HTTP反向代理
SSL/TSL服务器
可以针对HTTP请求添加cookie，进行路由后端服务器
可平衡负载至后端服务器，并支持持久连接
支持所有主服务器故障切换至备用服务器
支持专用端口实现监控服务
支持停止接受新连接请求，而不影响现有连接
可以在双向添加，修改或删除HTTP报文首部
响应报文压缩
支持基于pattern实现连接请求的访问控制
通过特定的URI为授权用户提供详细的状态信息



支持http反向代理
支持动态程序的反向代理
支持基于数据库的反向代理

不具备的功能：
正向代理--squid，nginx
缓存代理--varnish
web服务--nginx、tengine、apache、php、tomcat
UDP--目前不支持UDP协议
单机性能--相比LVS性能较差


------------------------

编译安装HAProxy

http://www.yunweipai.com/35252.html

编译安装HAProxy 2.0 LTS版本，更多源码包下载地址：http://www.haproxy.org/download/

解决lua环境
HAProxy 支持基于lua实现功能扩展，lua是一种小巧的脚本语言，于1993年由巴西里约热内卢天主教大学（Pontifical Catholic University of Rio de Janeiro）里的一个研究小组开发，其设计目的是为了嵌入应用程序中，从而为应用程序提供灵活的扩展和定制功能。

Lua 官网：www.lua.org

Lua 应用场景

游戏开发
独立应用脚本
Web 应用脚本
扩展和数据库插件，如MySQL Proxy
安全系统，如入侵检测系统
Centos 基础环境
参考链接：http://www.lua.org/start.html

HAProxy-编译安装插图

由于CentOS7 之前版本自带的lua版本比较低并不符合HAProxy要求的lua最低版本(5.3)的要求，因此需要编译安装较新版本的lua环境，然后才能编译安装HAProxy，过程如下：

'''
#当前系统版本
[root@centos7 ~]#lua -v 
Lua 5.1.4  Copyright (C) 1994-2008 Lua.org, PUC-Rio

#安装基础命令及编译依赖环境
[root@centos7 ~]# yum install gcc readline-devel
[root@centos7 ~]# wget http://www.lua.org/ftp/lua-5.3.5.tar.gz
[root@centos7 ~]# tar xvf  lua-5.3.5.tar.gz -C /usr/local/src
[root@centos7 ~]# cd /usr/local/src/lua-5.3.5
[root@centos7 lua-5.3.5]# make linux test

#查看编译安装的版本
[root@centos7 lua-5.3.5]#src/lua -v
Lua 5.3.5  Copyright (C) 1994-2018 Lua.org, PUC-Rio
'''

Ubuntu 基础环境
'''
#安装基础命令及编译依赖环境
# apt  install gcc iproute2  ntpdate  tcpdump telnet traceroute nfs-kernel-server nfs-common  lrzsz tree  openssl libssl-dev libpcre3 libpcre3-dev zlib1g-dev  openssh-server  libreadline-dev libsystemd-dev

# cd /usr/local/src
# wget http://www.lua.org/ftp/lua-5.3.5.tar.gz
# tar xvf  lua-5.3.5.tar.gz
# cd lua-5.3.5
# make linux test

# pwd
/usr/local/src/lua-5.3.5
# ./src/lua -v
Lua 5.3.5  Copyright (C) 1994-2018 Lua.org, PUC-Rio

或安装系统自带的lua
# apt install  lua5.3=5.3.3-1ubuntu0.18.04.1
# lua5.3  -v
Lua 5.3.3  Copyright (C) 1994-2016 Lua.org, PUC-Rio
'''

编译安装HAProxy
'''
#HAProxy  1.8及1.9版本编译参数：
make  ARCH=x86_64 TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 USE_SYSTEMD=1  USE_CPU_AFFINITY=1  PREFIX=/usr/local/haproxy 

#HAProxy 2.0以上版本编译参数：
[root@centos7 ~]#yum -y install gcc openssl-devel pcre-devel systemd-devel 
[root@centos7 ~]#tar xvf haproxy-2.1.3.tar.gz  -C /usr/local/src
[root@centos7 ~]#cd /usr/local/src/haproxy-2.1.3/
[root@centos7 haproxy-2.1.3]#cat README 
[root@centos7 haproxy-2.1.3]#ll Makefile 
-rw-rw-r-- 1 root root 40812 Feb 12 23:18 Makefile
[root@centos7 haproxy-2.1.3]#cat INSTALL

#参考INSTALL文件进行编译安装
[root@centos7 haproxy-2.1.3]#make  ARCH=x86_64 TARGET=linux-glibc  USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1  USE_SYSTEMD=1  USE_LUA=1 LUA_INC=/usr/local/src/lua-5.3.5/src/  LUA_LIB=/usr/local/src/lua-5.3.5/src/ 
[root@centos7 haproxy-2.1.3]# make install PREFIX=/apps/haproxy
[root@centos7 haproxy-2.1.3]#ln -s /apps/haproxy/sbin/haproxy /usr/sbin/

#查看生成的文件
[root@centos7 haproxy-2.1.3]#tree /apps/haproxy/
/apps/haproxy/
├── doc
│   └── haproxy
│       ├── 51Degrees-device-detection.txt
│       ├── architecture.txt
│       ├── close-options.txt
│       ├── configuration.txt
│       ├── cookie-options.txt
│       ├── DeviceAtlas-device-detection.txt
│       ├── intro.txt
│       ├── linux-syn-cookies.txt
│       ├── lua.txt
│       ├── management.txt
│       ├── netscaler-client-ip-insertion-protocol.txt
│       ├── network-namespaces.txt
│       ├── peers.txt
│       ├── peers-v2.0.txt
│       ├── proxy-protocol.txt
│       ├── regression-testing.txt
│       ├── seamless_reload.txt
│       ├── SOCKS4.protocol.txt
│       ├── SPOE.txt
│       └── WURFL-device-detection.txt
├── sbin
│   └── haproxy
└── share
    └── man
        └── man1
            └── haproxy.1

6 directories, 22 files
'''

验证HAProxy版本
'''
#验证HAProxy版本：
[root@centos7 ~]#which haproxy
/usr/sbin/haproxy
[root@centos7 ~]#haproxy  -v
HA-Proxy version 2.1.3 2020/02/12 - https://haproxy.org/
Status: stable branch - will stop receiving fixes around Q1 2021.
Known bugs: http://www.haproxy.org/bugs/bugs-2.1.3.html

[root@centos7 ~]#haproxy  -v
HA-Proxy version 2.0.14 2020/04/02 - https://haproxy.org/
[root@centos7 ~]#haproxy  -V
HA-Proxy version 2.0.14 2020/04/02 - https://haproxy.org/
Usage : haproxy [-f <cfgfile|cfgdir>]* [ -vdVD ] [ -n <maxconn> ] [ -N <maxpconn> ]
        [ -p <pidfile> ] [ -m <max megs> ] [ -C <dir> ] [-- <cfgfile>*]
        -v displays version ; -vv shows known build options.
        -d enters debug mode ; -db only disables background mode.
        -dM[<byte>] poisons memory with <byte> (defaults to 0x50)
        -V enters verbose mode (disables quiet mode)
        -D goes daemon ; -C changes to <dir> before loading files.
        -W master-worker mode.
        -Ws master-worker mode with systemd notify support.
        -q quiet mode : don't display messages
        -c check mode : only check config files and exit
        -n sets the maximum total # of connections (uses ulimit -n)
        -m limits the usable amount of memory (in MB)
        -N sets the default, per-proxy maximum # of connections (0)
        -L set local peer name (default to hostname)
        -p writes pids of all children to this file
        -de disables epoll() usage even when available
        -dp disables poll() usage even when available
        -dS disables splice usage (broken on old kernels)
        -dG disables getaddrinfo() usage
        -dR disables SO_REUSEPORT usage
        -dr ignores server address resolution failures
        -dV disables SSL verify on servers side
        -sf/-st [pid ]* finishes/terminates old pids.
        -x <unix_socket> get listening sockets from a unix socket
        -S <bind>[,<bind options>...] new master CLI

[root@centos7 ~]#haproxy  -vv
HA-Proxy version 2.1.3 2020/02/12 - https://haproxy.org/
Status: stable branch - will stop receiving fixes around Q1 2021.
Known bugs: http://www.haproxy.org/bugs/bugs-2.1.3.html
Build options :
  TARGET  = linux-glibc
  CPU     = generic
  CC      = gcc
  CFLAGS  = -m64 -march=x86-64 -O2 -g -fno-strict-aliasing -Wdeclaration-after-statement -fwrapv -Wno-unused-label -Wno-sign-compare -Wno-unused-parameter -Wno-old-style-declaration -Wno-ignored-qualifiers -Wno-clobbered -Wno-missing-field-initializers -Wtype-limits
  OPTIONS = USE_PCRE=1 USE_OPENSSL=1 USE_LUA=1 USE_ZLIB=1 USE_SYSTEMD=1

Feature list : +EPOLL -KQUEUE -MY_EPOLL -MY_SPLICE +NETFILTER +PCRE -PCRE_JIT -PCRE2 -PCRE2_JIT +POLL -PRIVATE_CACHE +THREAD -PTHREAD_PSHARED -REGPARM -STATIC_PCRE -STATIC_PCRE2 +TPROXY +LINUX_TPROXY +LINUX_SPLICE +LIBCRYPT +CRYPT_H -VSYSCALL +GETADDRINFO +OPENSSL +LUA +FUTEX +ACCEPT4 -MY_ACCEPT4 +ZLIB -SLZ +CPU_AFFINITY +TFO +NS +DL +RT -DEVICEATLAS -51DEGREES -WURFL +SYSTEMD -OBSOLETE_LINKER +PRCTL +THREAD_DUMP -EVPORTS

Default settings :
  bufsize = 16384, maxrewrite = 1024, maxpollevents = 200

Built with multi-threading support (MAX_THREADS=64, default=4).
Built with OpenSSL version : OpenSSL 1.0.2k-fips  26 Jan 2017
Running on OpenSSL version : OpenSSL 1.0.2k-fips  26 Jan 2017
OpenSSL library supports TLS extensions : yes
OpenSSL library supports SNI : yes
OpenSSL library supports : SSLv3 TLSv1.0 TLSv1.1 TLSv1.2
Built with Lua version : Lua 5.3.5
Built with network namespace support.
Built with transparent proxy support using: IP_TRANSPARENT IPV6_TRANSPARENT IP_FREEBIND
Built with PCRE version : 8.32 2012-11-30
Running on PCRE version : 8.32 2012-11-30
PCRE library supports JIT : no (USE_PCRE_JIT not set)
Encrypted password support via crypt(3): yes
Built with zlib version : 1.2.7
Running on zlib version : 1.2.7
Compression algorithms supported : identity("identity"), deflate("deflate"), raw-deflate("deflate"), gzip("gzip")

Available polling systems :
      epoll : pref=300,  test result OK
       poll : pref=200,  test result OK
     select : pref=150,  test result OK
Total: 3 (3 usable), will use epoll.

Available multiplexer protocols :
(protocols marked as <default> cannot be specified using 'proto' keyword)
              h2 : mode=HTTP       side=FE|BE     mux=H2
            fcgi : mode=HTTP       side=BE        mux=FCGI
       <default> : mode=HTTP       side=FE|BE     mux=H1
       <default> : mode=TCP        side=FE|BE     mux=PASS

Available services : none

Available filters :
    [SPOE] spoe
    [CACHE] cache
    [FCGI] fcgi-app
    [TRACE] trace
    [COMP] compression
'''

 
HAProxy启动脚本
'''
[root@centos7 ~]#cat  /usr/lib/systemd/system/haproxy.service
[Unit]
Description=HAProxy Load Balancer
After=syslog.target network.target

[Service]
ExecStartPre=/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg  -c -q
ExecStart=/usr/sbin/haproxy -Ws -f /etc/haproxy/haproxy.cfg -p /var/lib/haproxy/haproxy.pid
ExecReload=/bin/kill -USR2 $MAINPID

[Install]
WantedBy=multi-user.target

#默认缺少配置文件，无法启动
[root@centos7 ~]#systemctl daemon-reload
[root@centos7 ~]#systemctl start haproxy
Job for haproxy.service failed because the control process exited with error code. See "systemctl status haproxy.service" and "journalctl -xe" for details.

[root@centos7 ~]#tail /var/log/messages 
Mar 30 22:28:50 centos7 systemd: haproxy.service: control process exited, code=exited status=1
Mar 30 22:28:50 centos7 systemd: Failed to start HAProxy Load Balancer.
Mar 30 22:28:50 centos7 systemd: Unit haproxy.service entered failed state.
Mar 30 22:28:50 centos7 systemd: haproxy.service failed.
Mar 30 22:28:54 centos7 systemd: Starting HAProxy Load Balancer...
Mar 30 22:28:54 centos7 haproxy: [ALERT] 089/222854 (28223) : Cannot open configuration file/directory /etc/haproxy/haproxy.cfg : No such file or directory
Mar 30 22:28:54 centos7 systemd: haproxy.service: control process exited, code=exited status=1
Mar 30 22:28:54 centos7 systemd: Failed to start HAProxy Load Balancer.
Mar 30 22:28:54 centos7 systemd: Unit haproxy.service entered failed state.
Mar 30 22:28:54 centos7 systemd: haproxy.service failed.
'''

 
配置文件
'''
#查看配置文件范例
[root@centos7 ~]#tree /usr/local/src/haproxy-2.1.3/examples/
/usr/local/src/haproxy-2.1.3/examples/
├── acl-content-sw.cfg
├── content-sw-sample.cfg
├── errorfiles
│   ├── 400.http
│   ├── 403.http
│   ├── 408.http
│   ├── 500.http
│   ├── 502.http
│   ├── 503.http
│   ├── 504.http
│   └── README
├── haproxy.init
├── option-http_proxy.cfg
├── socks4.cfg
├── transparent_proxy.cfg
└── wurfl-example.cfg

1 directory, 15 files

#创建自定义的配置文件
[root@centos7 ~]# mkdir  /etc/haproxy
[root@centos7 ~]# vim /etc/haproxy/haproxy.cfg 
global
    maxconn 100000
    chroot /apps/haproxy
    stats socket /var/lib/haproxy/haproxy.sock mode 600 level admin
    #uid 99
    #gid 99
    user  haproxy
    group haproxy
    daemon
    #nbproc 4
    #cpu-map 1 0
    #cpu-map 2 1
    #cpu-map 3 2
    #cpu-map 4 3
    pidfile /var/lib/haproxy/haproxy.pid
    log 127.0.0.1 local2 info

defaults
    option http-keep-alive
    option  forwardfor
    maxconn 100000
    mode http
    timeout connect 300000ms
    timeout client  300000ms
    timeout server  300000ms

listen stats
    mode http
    bind 0.0.0.0:9999
    stats enable
    log global
    stats uri     /haproxy-status
    stats auth    haadmin:123456

listen  web_port
    bind 10.0.0.7:80
    mode http
    log global
    server web1  127.0.0.1:8080  check inter 3000 fall 2 rise 5
'''

启动haproxy
'''
[root@centos7 ~]# mkdir  /var/lib/haproxy
#[root@centos7 ~]# chown  -R 99.99 /var/lib/haproxy/ 
[root@centos7 ~]# useradd -r -s /sbin/nologin -d /var/lib/haproxy haproxy
[root@centos7 ~]# systemctl  enable --now haproxy
1
2
3
4
[root@centos7 ~]# mkdir  /var/lib/haproxy
#[root@centos7 ~]# chown  -R 99.99 /var/lib/haproxy/ 
[root@centos7 ~]# useradd -r -s /sbin/nologin -d /var/lib/haproxy haproxy
[root@centos7 ~]# systemctl  enable --now haproxy
验证haproxy状态
haproxy.cfg文件中定义了chroot、pidfile、user、group等参数，如果系统没有相应的资源会导致haproxy无法启动，具体参考日志文件 /var/log/messages


[root@centos7 ~]#systemctl status haproxy
● haproxy.service - HAProxy Load Balancer
   Loaded: loaded (/usr/lib/systemd/system/haproxy.service; disabled; vendor preset: disabled)
   Active: active (running) since Mon 2020-03-30 20:45:20 CST; 4min 45s ago
  Process: 1362 ExecStartPre=/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -c -q (code=exited, status=0/SUCCESS)
 Main PID: 1363 (haproxy)
   CGroup: /system.slice/haproxy.service
           ├─1363 /usr/sbin/haproxy -Ws -f /etc/haproxy/haproxy.cfg -p /var/lib/haproxy/haproxy.pid
           └─1366 /usr/sbin/haproxy -Ws -f /etc/haproxy/haproxy.cfg -p /var/lib/haproxy/haproxy.pid

Mar 30 20:45:20 centos7.wangxiaochun.com systemd[1]: Starting HAProxy Load Balancer...
Mar 30 20:45:20 centos7.wangxiaochun.com systemd[1]: Started HAProxy Load Balancer.
Mar 30 20:45:20 centos7.wangxiaochun.com haproxy[1363]: [NOTICE] 089/204520 (1363) : New worker #1 (1366...ked
Mar 30 20:45:20 centos7.wangxiaochun.com haproxy[1363]: [WARNING] 089/204520 (1366) : Server web_port/we...ue.
Mar 30 20:45:20 centos7.wangxiaochun.com haproxy[1363]: [ALERT] 089/204520 (1366) : proxy 'web_port' has...le!
Hint: Some lines were ellipsized, use -l to show in full.

[root@centos7 ~]# pstree -p |grep haproxy
           |-haproxy(28101)---haproxy(28105)
'''

查看haproxy的状态页面

浏览器访问：
http://haproxy-server:9999/haproxy-status

HAProxy-编译安装插图(1)
HAProxy-编译安装插图(2)

---------------------------------------

haproxy - 基础配置详解


配置文件官方帮助文档

Haproxy-基础配置详解插图
Haproxy-基础配置详解插图(1)

官方文档：http://cbonte.github.io/haproxy-dconv/2.1/configuration.html

HAProxy 的配置文件haproxy.cfg由两大部分组成，分别是global和proxies部分

global：全局配置段
'''
进程及安全配置相关的参数
性能调整相关参数
Debug参数
'''

proxies：代理配置段
'''
defaults：为frontend, backend, listen提供默认配置
frontend：前端，相当于nginx中的server {}
backend：后端，相当于nginx中的upstream {}
listen：同时拥有前端和后端配置
'''

global配置
global 配置参数说明
官方文档：http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#3

'''
chroot #锁定运行目录
deamon #以守护进程运行
stats socket /var/lib/haproxy/haproxy.sock mode 600 level admin process 1 #socket文件
user, group, uid, gid  #运行haproxy的用户身份
nbproc    n     #开启的haproxy work 进程数，默认进程数是一个
#nbthread  1    #指定每个haproxy进程开启的线程数，默认为每个进程一个线程,和nbproc互斥（版本有关）
#如果同时启用nbproc和nbthread 会出现以下日志的错误，无法启动服务
Apr  7 14:46:23 haproxy haproxy: [ALERT] 097/144623 (1454) : config : cannot enable multiple processes if multiple threads are configured. Please use either nbproc or nbthread but not both.

cpu-map 1 0     #绑定haproxy 进程至指定CPU，将第一个work进程绑定至0号CPU
maxconn  n      #每个haproxy进程的最大并发连接数
maxsslconn  n   #每个haproxy进程ssl最大连接数,用于haproxy配置了证书的场景下
maxconnrate n   #每个进程每秒创建的最大连接数量
spread-checks n #后端server状态check随机提前或延迟百分比时间，建议2-5(20%-50%)之间，默认值0
pidfile         #指定pid文件路径
log 127.0.0.1  local2 info #定义全局的syslog服务器；日志服务器需要开启UDP协议，最多可以定义两个
'''

多进程和线程
范例：多进程和socket文件

'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
global
maxconn 100000
chroot /apps/haproxy
stats socket /var/lib/haproxy/haproxy.sock1 mode 600 level admin process 1               
stats socket /var/lib/haproxy/haproxy.sock2 mode 600 level admin process 2
uid 99
gid 99
daemon
nbproc 2
[root@centos7 ~]#systemctl restart haproxy
[root@centos7 ~]#pstree -p |grep haproxy
           |-haproxy(2634)-+-haproxy(2637)
           |               `-haproxy(2638)
[root@centos7 ~]#ll /var/lib/haproxy/
total 4
-rw-r--r-- 1 root root 5 Mar 31 18:49 haproxy.pid
srw------- 1 root root 0 Mar 31 18:49 haproxy.sock1
srw------- 1 root root 0 Mar 31 18:49 haproxy.sock2
'''


---------------------

Haproxy - 日志配置

配置HAProxy记录日志到指定日志文件中

HAProxy配置
'''
#在global配置项定义：
log 127.0.0.1  local{1-7} info #基于syslog记录日志到指定设备，级别有(err、warning、info、debug)

listen  web_port
  bind 127.0.0.1:80
  mode http
  log global                                #开启当前web_port的日志功能，默认不记录日志
  server web1  127.0.0.1:8080  check inter 3000 fall 2 rise 5

# systemctl  restart haproxy
'''

Rsyslog配置
'''
vim /etc/rsyslog.conf 
$ModLoad imudp
$UDPServerRun 514
......
local3.*    /var/log/haproxy.log
......

# systemctl  restart rsyslog
'''

验证HAProxy日志
重启syslog服务并访问app页面，然后验证是否生成日志

'''
# tail -f /var/log/haproxy.log 
Aug 14 20:21:06 localhost haproxy[18253]: Connect from 192.168.0.1:3050 to 10.0.0.7:80 (web_host/HTTP)
Aug 14 20:21:06 localhost haproxy[18253]: Connect from 192.168.0.1:3051 to 10.0.0.7:80 (web_host/HTTP)
Aug 14 20:21:06 localhost haproxy[18253]: Connect from 192.168.0.1:3050 to 10.0.0.7:80 (web_host/HTTP)
'''


----------------------------

haproxy 实战案例 - 启动本地和远程日志

启动本地和远程日志
'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg 
log 127.0.0.1 local2 info
log 10.0.0.8 local2 info
[root@centos7 ~]#systemctl restart haproxy

#开启本地日志
[root@centos7 ~]#vim /etc/rsyslog.conf 
$ModLoad imudp
$UDPServerRun 514
......
local3.*                                        /var/log/haproxy.log
[root@centos7 ~]#systemctl restart rsyslog

#开启远程主机日志
[root@centos8 ~]#vim /etc/rsyslog.conf 
module(load="imudp") # needs to be done just once   
input(type="imudp" port="514")
local3.*                   /var/log/haproxy.log 
[root@centos8 ~]#systemctl restart rsyslog

#浏览器访问：http://haproxy-server:9999/haproxy-status,观察本机和远程主机生成的日志
[root@centos7 ~]#tail /var/log/haproxy.log
[root@centos7 ~]#cat /var/log/haproxy.log 
Mar 30 23:42:52 localhost haproxy[28643]: Connect from 10.0.0.1:7820 to 10.0.0.7:9999 (stats/HTTP)
Mar 30 23:42:52 localhost haproxy[28643]: Connect from 10.0.0.1:7821 to 10.0.0.7:9999 (stats/HTTP)
Mar 30 23:42:53 localhost haproxy[28643]: Connect from 10.0.0.1:7822 to 10.0.0.7:9999 (stats/HTTP)

[root@centos8 ~]#tail /var/log/haproxy.log
Mar 30 23:42:53 10.0.0.7 haproxy[28643]: Connect from 10.0.0.1:7824 to 10.0.0.7:9999 (stats/HTTP)
Mar 30 23:42:53 10.0.0.7 haproxy[28643]: Connect from 10.0.0.1:7825 to 10.0.0.7:9999 (stats/HTTP)
Mar 30 23:42:53 10.0.0.7 haproxy[28643]: Connect from 10.0.0.1:7826 to 10.0.0.7:9999 (stats/HTTP)
Mar 30 23:42:53 10.0.0.7 haproxy[28643]: Connect from 10.0.0.1:7827 to 10.0.0.7:9999 (stats/HTTP)
'''


-----------------------------

Haproxy - Proxies 配置

Proxies配置
官方文档：http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#4

'''
defaults [<name>] #默认配置项，针对以下的frontend、backend和listen生效，可以多个name也可以没有name
frontend <name>   #前端servername，类似于Nginx的一个虚拟主机 server和LVS服务集群。
backend  <name>   #后端服务器组，等于nginx的upstream和LVS中的RS服务器
listen   <name>   #将frontend和backend合并在一起配置，相对于frontend和backend配置更简洁，生产常用
'''

注意：name字段只能使用大小写字母，数字，‘-’(dash)，'_‘(underscore)，'.' (dot)和 ':'(colon)，并且严格区分大小写

haproxy-Proxies配置插图

Proxies配置-defaults

defaults 配置参数：

'''
option redispatch       #当server Id对应的服务器挂掉后，强制定向到其他健康的服务器，重新派发
option abortonclose     #当服务器负载很高时，自动结束掉当前队列处理比较久的链接，针对业务情况选择开启
option http-keep-alive  #开启与客户端的会话保持
option  forwardfor      #透传客户端真实IP至后端web服务器
mode http|tcp           #设置默认工作类型,使用TCP服务器性能更好，减少压力
timeout http-keep-alive 120s #session 会话保持超时时间，此时间段内会转发到相同的后端服务器
timeout connect 120s    #客户端请求从haproxy到后端server最长连接等待时间(TCP连接之前)，默认单位ms
timeout server  600s    #客户端请求从haproxy到后端服务端的请求处理超时时长(TCP连接之后)，默认单位ms，如果超时，会出现502错误，此值建议设置较大些，访止502错误
timeout client  600s    #设置haproxy与客户端的最长非活动时间，默认单位ms，建议和timeout server相同
timeout  check   5s     #对后端服务器的默认检测超时时间
default-server inter 1000 weight 3   #指定后端服务器的默认设置
'''

Proxies配置-frontend

frontend 配置参数：

'''
bind：   #指定HAProxy的监听地址，可以是IPV4或IPV6，可以同时监听多个IP或端口，可同时用于listen字段中

#格式：
bind [<address>]:<port_range> [, ...] [param*]

#注意：如果需要绑定在非本机的IP，需要开启内核参数：net.ipv4.ip_nonlocal_bind=1
'''

范例：

'''
listen http_proxy                           #监听http的多个IP的多个端口和sock文件
    bind :80,:443,:8801-8810
    bind 10.0.0.1:10080,10.0.0.1:10443
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy

listen http_https_proxy                     #https监听
    bind :80
    bind :443 ssl crt /etc/haproxy/site.pem #公钥和私钥公共文件

listen http_https_proxy_explicit            #监听ipv6、ipv4和unix sock文件
    bind ipv6@:80
    bind ipv4@public_ssl:443 ssl crt /etc/haproxy/site.pem
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy

listen external_bind_app1                   #监听file descriptor
    bind "fd@${FD_APP1}"
'''

生产示例：

'''
frontend  magedu_web_port               #可以采用后面形式命名：业务-服务-端口号
    bind :80,:8080
    bind 10.0.0.7:10080,:8801-8810,10.0.0.17:9001-9010
    mode  http|tcp              #指定负载协议类型
    use_backend <backend_name>  #调用的后端服务器组名称
'''

Proxies配置-backend
定义一组后端服务器，backend服务器将被frontend进行调用。

'''
mode  http|tcp      #指定负载协议类型,和对应的frontend必须一致
option              #配置选项
server              #定义后端real server
'''

注意：option后面加 httpchk，smtpchk,mysql-check,pgsql-check，ssl-hello-chk方法，可用于实现更多应用层检测功能。

option 配置

'''
check               #对指定real进行健康状态检查，如果不加此设置，默认不开启检查
    addr  <IP>        #可指定的健康状态监测IP，可以是专门的数据网段，减少业务网络的流量
    port  <num>   #指定的健康状态监测端口
    inter <num>   #健康状态检查间隔时间，默认2000 ms
    fall  <num>       #后端服务器从线上转为线下的检查的连续失效次数，默认为3
    rise  <num>       #后端服务器从下线恢复上线的检查的连续有效次数，默认为2
weight  <weight>  #默认为1，最大值为256，0表示不参与负载均衡，但仍接受持久连接
backup              #将后端服务器标记为备份状态,只在所有非备份主机down机时提供服务，类似Sorry Server
disabled            #将后端服务器标记为不可用状态，即维护状态，除了持久模式，将不再接受连接
redirect prefix  http://www.baidu.com/      #将请求临时(302)重定向至其它URL，只适用于http模式
redir http://www.baidu.com                  #将请求临时(302)重定向至其它URL，只适用于http模式
maxconn <maxconn>     #当前后端server的最大并发连接数
backlog <backlog> #当前端服务器的连接数达到上限后的后援队列长度，注意：不支持backend
'''

frontend+backend配置实例

范例1：

'''
frontend magedu-test-http
 bind :80,:8080
 mode tcp
 use_backend magedu-test-http-nodes

backend magedu-test-http-nodes
 mode tcp
 default-server inter 1000 weight 6  
 server web1 10.0.0.17:80 check weight 2 addr 10.0.0.117 port 8080
 server web1 10.0.0.27:80 check
'''

范例2：

'''
#官网业务访问入口
frontend  WEB_PORT_80
    bind 10.0.0.7:80
    mode http
    use_backend  web_prot_http_nodes

backend web_prot_http_nodes
    mode  http
    option forwardfor
    server 10.0.0.17 10.0.0.17:8080   check inter 3000 fall 3 rise 5  
    server 10.0.0.27 10.0.0.27:8080   check inter 3000 fall 3 rise 5
'''

Proxies配置-listen替代frontend+backend
使用listen替换上面的frontend和backend的配置方式，可以简化设置，通常只用于TCP协议的应用

'''
#官网业务访问入口
listen  WEB_PORT_80 
    bind 10.0.0.7:80  
    mode http
    option  forwardfor
    server web1   10.0.0.17:8080   check inter 3000 fall 3 rise 5
    server web2   10.0.0.27:8080   check inter 3000 fall 3 rise 5
'''

使用子配置文件保存配置
当业务众多时，将所有配置都放在一个配置文件中，会造成维护困难。可以考虑按业务分类，将配置信息拆分，放在不同的子配置文件中，从而达到方便维护的目的。

'''
#创建子配置目录
[root@centos7 ~]#mkdir /etc/haproxy/conf.d/

#创建子配置文件，注意：必须为cfg后缀
[root@centos7 ~]#vim   /etc/haproxy/conf.d/test.cfg
listen WEB_PORT_80
    bind 10.0.0.7:80
    mode http
    balance roundrobin
    server web1  10.0.0.17:80  check inter 3000 fall 2 rise 5
    server web2  10.0.0.27:80  check inter 3000 fall 2 rise 5

#添加子配置目录到unit文件中
[root@centos7 ~]#vim  /lib/systemd/system/haproxy.service
[Unit]
Description=HAProxy Load Balancer
After=syslog.target network.target

[Service]
ExecStartPre=/usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d/ -c -q
ExecStart=/usr/sbin/haproxy -Ws -f /etc/haproxy/haproxy.cfg -f /etc/haproxy/conf.d/  -p /var/lib/haproxy/haproxy.pid
ExecReload=/bin/kill -USR2 $MAINPID

[Install]
WantedBy=multi-user.target

[root@centos7 ~]#systemctl daemon-reload 
[root@centos7 ~]#systemctl restart haproxy
'''


----------------------------

haproxy - 调度算法详解

HAProxy调度算法
HAProxy通过固定参数
'''
balance
'''
指明对后端服务器的调度算法，该参数可以配置在listen或backend选项中。

HAProxy的调度算法分为静态和动态调度算法，但是有些算法可以根据参数在静态和动态算法中相互转换。

官方文档：http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#4-balance

静态算法
静态算法：按照事先定义好的规则轮询公平调度，不关心后端服务器的当前负载、链接数和响应速度等，且无法实时修改权重，只能靠重启HAProxy生效。

可以利用 socat工具对服务器动态权重和其它状态的调整，Socat 是 Linux 下的一个多功能的网络工具，名字来由是Socket CAT，Socat 的主要特点就是在两个数据流之间建立通道，且支持众多协议和链接方式。如 IP、TCP、 UDP、IPv6、Socket文件等

范例：利用工具socat 对服务器动态权重调整

'''
[root@centos7 ~]#yum -y install socat

#查看帮助
[root@centos7 ~]#socat -h
[root@centos7 ~]#echo "help" | socat stdio /var/lib/haproxy/haproxy.sock
Unknown command. Please enter one of the following commands only :
  help           : this message
  prompt         : toggle interactive mode with prompt
  quit           : disconnect
  show tls-keys [id|*]: show tls keys references or dump tls ticket keys when id specified
  set ssl tls-key [id|keyfile] <tlskey>: set the next TLS key for the <id> or <keyfile> listener to <tlskey>
  set ssl cert <certfile> <payload> : replace a certificate file
  commit ssl cert <certfile> : commit a certificate file
  abort ssl cert <certfile> : abort a transaction for a certificate file
  show sess [id] : report the list of current sessions or dump this session
  shutdown session : kill a specific session
  shutdown sessions server : kill sessions on a server
  clear counters : clear max statistics counters (add 'all' for all counters)
  show info      : report information about the running process [desc|json|typed]*
  show stat      : report counters for each proxy and server [desc|json|typed]*
  show schema json : report schema used for stats
  disable agent  : disable agent checks (use 'set server' instead)
  disable health : disable health checks (use 'set server' instead)
  disable server : disable a server for maintenance (use 'set server' instead)
  enable agent   : enable agent checks (use 'set server' instead)
  enable health  : enable health checks (use 'set server' instead)
  enable server  : enable a disabled server (use 'set server' instead)
  set maxconn server : change a server's maxconn setting
  set server     : change a server's state, weight or address
  get weight     : report a server's current weight
  set weight     : change a server's weight (deprecated)
  show startup-logs : report logs emitted during HAProxy startup
  show peers [peers section]: dump some information about all the peers or this peers section
  set maxconn global : change the per-process maxconn setting
  set rate-limit : change a rate limiting value
  set severity-output [none|number|string] : set presence of severity level in feedback information
  set timeout    : change a timeout setting
  show env [var] : dump environment variables known to the process
  show cli sockets : dump list of cli sockets
  show cli level   : display the level of the current CLI session
  show fd [num] : dump list of file descriptors in use
  show activity : show per-thread activity stats (for support/developers)
  operator       : lower the level of the current CLI session to operator
  user           : lower the level of the current CLI session to user
  clear table    : remove an entry from a table
  set table [id] : update or create a table entry's data
  show table [id]: report table usage stats or dump this table's contents
  disable frontend : temporarily disable specific frontend
  enable frontend : re-enable specific frontend
  set maxconn frontend : change a frontend's maxconn setting
  show servers state [id]: dump volatile server information (for backend <id>)
  show backend   : list backends in the current running config
  shutdown frontend : stop a specific frontend
  set dynamic-cookie-key backend : change a backend secret key for dynamic cookies
  enable dynamic-cookie backend : enable dynamic cookies on a specific backend
  disable dynamic-cookie backend : disable dynamic cookies on a specific backend
  show errors    : report last request and response errors for each proxy
  show resolvers [id]: dumps counters from all resolvers section and
                     associated name servers
  show cache     : show cache status
  add acl        : add acl entry
  clear acl <id> : clear the content of this acl
  del acl        : delete acl entry
  get acl        : report the patterns matching a sample for an ACL
  show acl [id]  : report available acls or dump an acl's contents
  add map        : add map entry
  clear map <id> : clear the content of this map
  del map        : delete map entry
  get map        : report the keys and values matching a sample for a map
  set map        : modify map entry
  show map [id]  : report available maps or dump a map's contents
  trace <module> [cmd [args...]] : manage live tracing
  show trace [<module>] : show live tracing state
  show threads   : show some threads debugging information
  show pools     : report information about the memory pools usage
  show events [<sink>] : show event sink state
  show profiling : show CPU profiling options
  set  profiling : enable/disable CPU profiling

[root@centos7 ~]#echo "show info" | socat stdio /var/lib/haproxy/haproxy.sock
Name: HAProxy
Version: 2.1.3
Release_date: 2020/02/12
Nbthread: 4
Nbproc: 1
Process_num: 1
Pid: 2279
Uptime: 0d 0h46m07s
Uptime_sec: 2767
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
Ulimit-n: 200041
Maxsock: 200041
Maxconn: 100000
Hard_maxconn: 100000
CurrConns: 0
CumConns: 1
CumReq: 1
MaxSslConns: 0
CurrSslConns: 0
CumSslConns: 0
Maxpipes: 0
PipesUsed: 0
PipesFree: 0
ConnRate: 0
ConnRateLimit: 0
MaxConnRate: 0
SessRate: 0
SessRateLimit: 0
MaxSessRate: 0
SslRate: 0
SslRateLimit: 0
MaxSslRate: 0
SslFrontendKeyRate: 0
SslFrontendMaxKeyRate: 0
SslFrontendSessionReuse_pct: 0
SslBackendKeyRate: 0
SslBackendMaxKeyRate: 0
SslCacheLookups: 0
SslCacheMisses: 0
CompressBpsIn: 0
CompressBpsOut: 0
CompressBpsRateLim: 0
ZlibMemUsage: 0
MaxZlibMemUsage: 0
Tasks: 19
Run_queue: 1
Idle_pct: 100
node: centos7.wangxiaochun.com
Stopping: 0
Jobs: 7
Unstoppable Jobs: 0
Listeners: 6
ActivePeers: 0
ConnectedPeers: 0
DroppedLogs: 0
BusyPolling: 0
FailedResolutions: 0
TotalBytesOut: 0
BytesOutRate: 0
DebugCommandsIssued: 0

[root@centos7 ~]#cat /etc/haproxy/haproxy.cfg
......
listen magedu-test-80
bind :81,:82
mode http
server web1 10.0.0.17:80  check inter 3000 fall 3 rise 5 
server web2 10.0.0.27:80 check weight 3  
......

[root@centos7 ~]#echo "show servers state" | socat stdio /var/lib/haproxy/haproxy.sock
1
# be_id be_name srv_id srv_name srv_addr srv_op_state srv_admin_state srv_uweight srv_iweight srv_time_since_last_change srv_check_status srv_check_result srv_check_health srv_check_state srv_agent_state bk_f_forced_id srv_f_forced_id srv_fqdn srv_port srvrecord
2 magedu-test-80 1 web1 10.0.0.17 2 0 2 1 812 6 3 7 6 0 0 0 - 80 -
2 magedu-test-80 2 web2 10.0.0.27 2 0 2 3 812 6 3 4 6 0 0 0 - 80 -
4 web_port 1 web1 127.0.0.1 0 0 1 1 810 8 2 0 6 0 0 0 - 8080 -

[root@centos7 ~]#echo "get weight magedu-test-80/web2" | socat stdio /var/lib/haproxy/haproxy.sock
3 (initial 3)

#修改weight，注意只针对单进程有效
[root@centos7 ~]#echo "set weight magedu-test-80/web2 2" | socat stdio /var/lib/haproxy/haproxy.sock

[root@centos7 ~]#echo "get weight magedu-test-80/web2" | socat stdio /var/lib/haproxy/haproxy.sock
2 (initial 3)

#将后端服务器禁用，注意只针对单进程有效
[root@centos7 ~]#echo "disable server magedu-test-80/web2" | socat stdio /var/lib/haproxy/haproxy.sock

#将后端服务器软下线，即weight设为0
[root@centos7 ~]#echo "set weight magedu-test-80/web1 0" | socat stdio /var/lib/haproxy/haproxy.sock

#将后端服务器禁用，针对多进程
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
......
stats socket /var/lib/haproxy/haproxy1.sock mode 600 level admin process 1
stats socket /var/lib/haproxy/haproxy2.sock mode 600 level admin process 2               nbproc 2
.....

[root@centos7 ~]#echo "disable server  magedu-test-80/web2" | socat stdio /var/lib/haproxy/haproxy1.sock
[root@centos7 ~]#echo "disable server  magedu-test-80/web2" | socat stdio /var/lib/haproxy/haproxy2.sock

[root@haproxy ~]#for i in {1..2};do echo "set weight magedu-test-80/web$i 10" | socat stdio /var/lib/haproxy/haproxy$i.sock;done

#如果静态算法，如:static-rr，可以更改weight为0或1，但不支持动态更改weight为其它值，否则会提示下面信息
[root@centos7 ~]#echo "set weight magedu-test-80/web1 0" | socat stdio /var/lib/haproxy/haproxy.sock
[root@centos7 ~]#echo "set weight magedu-test-80/web1 1" | socat stdio /var/lib/haproxy/haproxy.sock

[root@centos7 ~]#echo "set weight magedu-test-80/web1 2" | socat stdio /var/lib/haproxy/haproxy.sock
Backend is using a static LB algorithm and only accepts weights '0%' and '100%'.
'''

static-rr
static-rr：基于权重的轮询调度，不支持权重的运行时利用socat进行动态调整及后端服务器慢启动，其后端主机数量没有限制，相当于LVS中的 wrr

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance static-rr
  server web1  10.0.0.17:80 weight 1 check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 2 check inter 3000 fall 2 rise 5
'''

first
first：根据服务器在列表中的位置，自上而下进行调度，但是其只会当第一台服务器的连接数达到上限，新请求才会分配给下一台服务，因此会忽略服务器的权重设置，此方式使用较少

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance first
  server web1  10.0.0.17:80 maxconn 2 weight 1 check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1 check inter 3000 fall 2 rise 5
'''

测试访问效果

'''
#同时运行下面命令，观察结果
# while  true;do  curl http://10.0.0.7/index.html ; sleep 0.1;done
'''

动态算法
动态算法：基于后端服务器状态进行调度适当调整，优先调度至当前负载较低的服务器，且权重可以在haproxy运行时动态调整无需重启。

roundrobin
roundrobin：基于权重的轮询动态调度算法，支持权重的运行时调整，不同于lvs中的rr轮训模式，HAProxy中的roundrobin支持慢启动(新加的服务器会逐渐增加转发数)，其每个后端backend中最多支持4095个real server，支持对real server权重动态调整，roundrobin为默认调度算法

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance roundrobin
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 2  check inter 3000 fall 2 rise 5
'''

支持动态调整权重：

'''
# echo "get weight web_host/web1" | socat stdio /var/lib/haproxy/haproxy.sock 
1 (initial 1)

# echo "set weight web_host/web1 3" | socat stdio /var/lib/haproxy/haproxy.sock 

# echo "get weight web_host/web1" | socat stdio /var/lib/haproxy/haproxy.sock 
3 (initial 1)
'''

leastconn
leastconn加权的最少连接的动态，支持权重的运行时调整和慢启动，即当前后端服务器连接最少的优先调度(新客户端连接)，比较适合长连接的场景使用，比如：MySQL等场景。

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance leastconn
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

random
在1.9版本开始增加一个叫做random的负载平衡算法，其基于随机数作为一致性hash的key，随机负载平衡对于大型服务器场或经常添加或删除服务器非常有用，支持weight的动态调整，weight较大的主机有更大概率获取新请求

random配置实例

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance  random
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

其他算法
其它算法即可作为静态算法，又可以通过选项成为动态算法

source
源地址hash，基于用户源地址hash并将请求转发到后端服务器，后续同一个源地址请求将被转发至同一个后端web服务器。此方式当后端服务器数据量发生变化时，会导致很多用户的请求转发至新的后端服务器，默认为静态方式，但是可以通过hash-type支持的选项更改

这个算法一般是在不插入Cookie的TCP模式下使用，也可给拒绝会话cookie的客户提供最好的会话粘性，适用于session会话保持但不支持cookie和缓存的场景

源地址有两种转发客户端请求到后端服务器的服务器选取计算方式，分别是取模法和一致性hash

map-base取模法
map-based：取模法，对source地址进行hash计算，再基于服务器总权重的取模，最终结果决定将此请求转发至对应的后端服务器。此方法是静态的，即不支持在线调整权重，不支持慢启动，可实现对后端服务器均衡调度。缺点是当服务器的总权重发生变化时，即有服务器上线或下线，都会因总权重发生变化而导致调度结果整体改变，hash-type 指定的默认值为此算法

'''
所谓取模运算，就是计算两个数相除之后的余数，10%7=3, 7%4=3
map-based算法：基于权重取模，hash(source_ip)%所有后端服务器相加的总权重
'''


取模法配置示例：

'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode tcp
  log global
  balance source
  hash-type map-based 
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 3
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 3

[root@haproxy ~]#echo "set weight web_host/10.0.0.27 10" | socat stdio /var/lib/haproxy/haproxy.sock 
Backend is using a static LB algorithm and only accepts weights '0%' and '100%'.

[root@haproxy ~]#echo "set weight web_host/10.0.0.27 0" | socat stdio /var/lib/haproxy/haproxy.sock 

[root@haproxy conf.d]#echo "get weight web_host/10.0.0.27" | socat stdio /var/lib/haproxy/haproxy.sock 
0 (initial 1)
'''

一致性hash
一致性哈希，当服务器的总权重发生变化时，对调度结果影响是局部的，不会引起大的变动，hash（o）mod n ，该hash算法是动态的，支持使用 socat等工具进行在线权重调整，支持慢启动

算法：

'''
1、key1=hash(source_ip)%(2^32)  [0---4294967295]
2、keyA=hash(后端服务器虚拟ip)%(2^32)
3、将key1和keyA都放在hash环上，将用户请求调度到离key1最近的keyA对应的后端服务器
'''

hash环偏斜问题

'''
增加虚拟服务器IP数量，比如：一个后端服务器根据权重为1生成1000个虚拟IP，再hash。而后端服务器权重为2则生成2000的虚拟IP，再bash,最终在hash环上生成3000个节点，从而解决hash环偏斜问题
'''

hash对象
Hash对象到后端服务器的映射关系：

Haproxy-调度算法详解插图

一致性hash示意图
后端服务器在线与离线的调度方式

Haproxy-调度算法详解插图(1)
Haproxy-调度算法详解插图(2)

一致性hash配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode tcp
  log global
  balance source
  hash-type consistent
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

uri
基于对用户请求的URI的左半部分或整个uri做hash，再将hash结果对总权重进行取模后，根据最终结果将请求转发到后端指定服务器，适用于后端是缓存服务器场景，默认是静态，也可以通过hash-type指定map-based和consistent，来定义使用取模法还是一致性hash。

注意：此算法是应用层，所有只支持 mode http ，不支持 mode tcp

'''
<scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<frag>
左半部分：/<path>;<params>
整个uri：/<path>;<params>?<query>#<frag>
'''

Haproxy-调度算法详解插图(3)

uri 取模法配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance uri
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

uri 一致性hash配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance uri
  hash-type consistent
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

访问测试
访问不同的uri，确认可以将用户同样的请求转发至相同的服务器

'''
# curl  http://10.0.0.7/test1.html
# curl  http://10.0.0.7/test2..html
'''

url_param
url_param对用户请求的url中的 params 部分中的一个参数key对应的value值作hash计算，并由服务器总权重相除以后派发至某挑出的服务器；通常用于追踪用户，以确保来自同一个用户的请求始终发往同一个real server，如果无没key，将按roundrobin算法

'''
假设：
url = http://www.magedu.com/foo/bar/index.php?key=value

则：
host = "www.magedu.com"
url_param = "key=value"
'''

url_param取模法配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance url_param  userid     #url_param hash
  server web1 10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2 10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

url_param一致性hash配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance url_param  userid             #对url_param的值取hash
  hash-type consistent
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''


测试访问
'''
# curl  http://10.0.0.7/index.html?userid=<NAME_ID> 
# curl  "http://10.0.0.7/index.html?userid=<NAME_ID>&typeid=<TYPE_ID>" 
'''

hdr
针对用户每个http头部(header)请求中的指定信息做hash，此处由 name 指定的http首部将会被取出并做hash计算，然后由服务器总权重取模以后派发至某挑出的服务器，如无有效的值，则会使用默认的轮询调度。

hdr取模法配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance hdr(User-Agent)
  #balance hdr(host)
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

一致性hash配置示例
'''
listen  web_host
  bind 10.0.0.7:80,:8801-8810,10.0.0.7:9001-9010
  mode http
  log global
  balance hdr(User-Agent)
  hash-type consistent
  server web1  10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2  10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''


测试访问
'''
[root@centos6 ~]#curl -v http://10.0.0.7/index.html
[root@centos6 ~]#curl -vA 'firefox' http://10.0.0.7/index.html
[root@centos6 ~]#curl -vA 'chrome' http://10.0.0.7/index.html
'''

rdp-cookie
rdp-cookie对远windows远程桌面的负载，使用cookie保持会话，默认是静态，也可以通过hash-type指定map-based和consistent，来定义使用取模法还是一致性hash。

rdp-cookie取模法配置示例
'''
listen RDP
  bind 10.0.0.7:3389
  balance rdp-cookie
  mode tcp
  server rdp0 10.0.0.17:3389 check fall 3 rise 5 inter 2000 weight 1
'''


rdp-cookie一致性hash配置示例
'''
[root@haproxy ~]#cat /etc/haproxy/conf.d/windows_rdp.cfg 
listen magedu_RDP_3389
  bind  172.16.0.100:3389
  balance rdp-cookie
  hash-type consistent
  mode tcp
  server rdp0 10.0.0.200:3389 check fall 3 rise 5 inter 2000 weight 1

[root@haproxy ~]#hostname -I
10.0.0.100 172.16.0.100 
'''


Haproxy-调度算法详解插图(4)
Haproxy-调度算法详解插图(5)

基于iptables实现RDP协议转发

必须开启ip转发功能：
'''
net.ipv4.ip_forward = 1
'''

'''
[root@centos8 ~]#sysctl -w net.ipv4.ip_forward=1
#客户端和Windows在不同网段需要下面命令
[root@centos8 ~]#iptables  -t nat -A PREROUTING -d 172.16.0.100 -p tcp --dport 3389 -j DNAT --to-destination 10.0.0.200:3389

#客户端和Windows在同一网段需要再执行下面命令
[root@centos8 ~]#iptables  -t nat -A PREROUTING -d 10.0.0.8 -p tcp --dport 3389 -j DNAT --to-destination 10.0.0.1:3389
[root@centos8 ~]#iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j SNAT --to-source  10.0.0.8
'''

在windows 可以看到以下信息

Haproxy-调度算法详解插图(6)

算法总结
'''
static-rr--------->tcp/http  静态
first------------->tcp/http  静态

roundrobin-------->tcp/http 动态
leastconn--------->tcp/http 动态
random------------>tcp/http 动态

以下静态和动态取决于hash_type是否consistent
source------------>tcp/http
Uri--------------->http
url_param--------->http     
hdr--------------->http
rdp-cookie-------->tcp
'''

各算法使用场景
'''
first       #使用较少

static-rr   #做了session共享的web集群
roundrobin
random

leastconn   #数据库
source      #基于客户端公网IP的会话保持

Uri--------------->http  #缓存服务器，CDN服务商，蓝汛、百度、阿里云、腾讯
url_param--------->http 

hdr         #基于客户端请求报文头部做下一步处理

rdp-cookie  #很少使用
'''


------------------------------

haproxy - 基于 cookie 的会话保持


高级功能及配置
介绍HAProxy高级配置及实用案例

基于cookie的会话保持
cookie value：为当前server指定cookie值，实现基于cookie的会话黏性，相对于基于 source 地址 hash 调度算法对客户端的粒度更精准，但同时也加大了haproxy负载，目前此模式使用较少， 已经被session共享服务器代替

注意：不支持 tcp mode，使用 http mode

配置选项
'''
cookie name  [ rewrite | insert | prefix ][ indirect ] [ nocache ][ postonly ] [ preserve ][ httponly ] [ secure ][ domain ]* [ maxidle <idle> ][ maxlife ]

name：       #cookie 的key名称，用于实现持久连接
insert：     #插入新的cookie,默认不插入cookie
indirect：   #如果客户端已经有cookie,则不会再发送cookie信息
nocache：    #当client和hapoxy之间有缓存服务器（如：CDN）时，不允许中间缓存器缓存cookie，因为这会导致很多经过同一个CDN的请求都发送到同一台后端服务器
'''

配置示例
'''
listen  web_port
 bind 10.0.0.7:80
 balance  roundrobin
 mode http                              #不支持 tcp mode
 log global
 cookie WEBSRV insert nocache indirect
 server web1  10.0.0.17:80 check inter 3000 fall 2 rise 5  cookie web1 
 server web2  10.0.0.27:80 check inter 3000 fall 2 rise 5  cookie web2
'''

验证cookie信息
浏览器验证：

haproxy-基于cookie的会话保持插图
haproxy-基于cookie的会话保持插图(1)

通过命令行验证：

'''
[root@centos6 ~]#curl -i 10.0.0.7
HTTP/1.1 200 OK
date: Thu, 02 Apr 2020 02:26:08 GMT
server: Apache/2.4.6 (CentOS)
last-modified: Thu, 02 Apr 2020 01:44:28 GMT
etag: "a-5a244f0fd5175"
accept-ranges: bytes
content-length: 10
content-type: text/html; charset=UTF-8
set-cookie: WEBSRV=web2; path=/
cache-control: private

10.0.0.27
[root@centos6 ~]#curl -i 10.0.0.7
HTTP/1.1 200 OK
date: Thu, 02 Apr 2020 02:26:15 GMT
server: Apache/2.4.6 (CentOS)
last-modified: Thu, 02 Apr 2020 01:44:13 GMT
etag: "a-5a244f01f8adc"
accept-ranges: bytes
content-length: 10
content-type: text/html; charset=UTF-8
set-cookie: WEBSRV=web1; path=/
cache-control: private

10.0.0.17

[root@centos6 ~]#curl -b  WEBSRV=web1 10.0.0.7
10.0.0.17
[root@centos6 ~]#curl -b  WEBSRV=web2 10.0.0.7
10.0.0.27

[root@centos6 ~]#curl -vb  WEBSRV=web1 10.0.0.7
* About to connect() to 10.0.0.7 port 80 (#0)
*   Trying 10.0.0.7... connected
* Connected to 10.0.0.7 (10.0.0.7) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2
> Host: 10.0.0.7
> Accept: */*
> Cookie: WEBSRV=web1
> 
< HTTP/1.1 200 OK
< date: Thu, 02 Apr 2020 02:27:54 GMT
< server: Apache/2.4.6 (CentOS)
< last-modified: Thu, 02 Apr 2020 01:44:13 GMT
< etag: "a-5a244f01f8adc"
< accept-ranges: bytes
< content-length: 10
< content-type: text/html; charset=UTF-8
< 
10.0.0.17
* Connection #0 to host 10.0.0.7 left intact
* Closing connection #0
[root@centos6 ~]#curl -vb  WEBSRV=web2 10.0.0.7
* About to connect() to 10.0.0.7 port 80 (#0)
*   Trying 10.0.0.7... connected
* Connected to 10.0.0.7 (10.0.0.7) port 80 (#0)
> GET / HTTP/1.1
> User-Agent: curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2
> Host: 10.0.0.7
> Accept: */*
> Cookie: WEBSRV=web2
> 
< HTTP/1.1 200 OK
< date: Thu, 02 Apr 2020 02:27:57 GMT
< server: Apache/2.4.6 (CentOS)
< last-modified: Thu, 02 Apr 2020 01:44:28 GMT
< etag: "a-5a244f0fd5175"
< accept-ranges: bytes
< content-length: 10
< content-type: text/html; charset=UTF-8
< 
10.0.0.27
* Connection #0 to host 10.0.0.7 left intact
* Closing connection #0
'''


HAProxy状态页
通过web界面，显示当前HAProxy的运行状态

官方帮助：

'''
http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#4-stats%20admin
'''

状态页配置项
'''
stats enable                #基于默认的参数启用stats page
stats hide-version          #将状态页中haproxy版本隐藏
stats refresh <delay>         #设定自动刷新时间间隔，默认不自动刷新
stats uri <prefix>        #自定义stats page uri，默认值：/haproxy?stats 
stats realm <realm>       #账户认证时的提示信息，示例：stats realm   HAProxy\ Statistics
stats auth <user>:<passwd>  #认证时的账号和密码，可使用多次，默认：no authentication，可有多行用户
stats admin { if | unless } <cond> #启用stats page中的管理功能
'''

启用状态页
'''
listen stats
  bind :9999
  stats enable
  #stats hide-version 
  stats uri  /haproxy-status
  stats realm HAPorxy\ Stats\ Page
  stats auth haadmin:123456             #两个用户
  stats auth admin:123456
  #stats refresh 30s
  stats admin if TRUE                   #安全原因，不建议打开
'''


登录状态页
'''
pid = 27134 (process #1, nbproc = 1, nbthread = 1) #pid为当前pid号，process为当前进程号，nbproc和nbthread为一共多少进程和每个进程多少个线程
uptime = 0d 0h00m04s #启动了多长时间
system limits: memmax = unlimited; ulimit-n = 200029 #系统资源限制：内存/最大打开文件数/
maxsock = 200029; maxconn = 100000; maxpipes = 0 #最大socket连接数/单进程最大连接数/最大管道数maxpipes
current conns = 2; current pipes = 0/0; conn rate = 2/sec; bit rate = 0.000 kbps #当前连接数/当前管道数/当前连接速率
Running tasks: 1/14; idle = 100 %        #运行的任务/当前空闲率
active UP：                              #在线服务器
backup UP：                              #标记为backup的服务器
active UP, going down：                  #监测未通过正在进入down过程
backup UP, going down：                  #备份服务器正在进入down过程
active DOWN, going up：                  #down的服务器正在进入up过程
backup DOWN, going up：                  #备份服务器正在进入up过程
active or backup DOWN：                  #在线的服务器或者是backup的服务器已经转换成了down状态
not checked：                            #标记为不监测的服务器
active or backup DOWN for maintenance (MAINT) #active或者backup服务器人为下线的
active or backup SOFT STOPPED for maintenance #active或者backup被人为软下线(人为将weight改成0)
'''

haproxy-基于cookie的会话保持插图(2)

backend server信息
'''
session rate(每秒的连接会话信息)：	Errors(错误统计信息)：
cur:每秒的当前会话数量	Req:错误请求量
max:每秒新的最大会话数量	conn:错误链接量
limit:每秒新的会话限制量	Resp:错误响应量
sessions(会话信息)：	Warnings(警告统计信息)：
cur:当前会话量	Retr:重新尝试次数
max:最大会话量	Redis:再次发送次数
limit: 限制会话量	
Total:总共会话量	Server(real server信息)：
LBTot:选中一台服务器所用的总时间	Status:后端机的状态，包括UP和DOWN
Last：和服务器的持续连接时间	LastChk:持续检查后端服务器的时间
Wght:权重	
Bytes(流量统计)：	Act:活动链接数量
In:网络的字节输入总量	Bck:备份的服务器数量
Out:网络的字节输出总量	Chk:心跳检测时间
Dwn:后端服务器连接后都是DOWN的数量	
Denied(拒绝统计信息)：	Dwntme:总的downtime时间
Req:拒绝请求量	Thrtle:server 状态
Resp:拒绝回复量	
'''

利用状态页实现haproxy服务器的健康性检查
范例：通过curl 命令对haproxy的状态页的访问实现健康检查

'''
[root@centos8 ~]#curl -I  http://haadmin:123456@10.0.0.100:9999/haproxy-status
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html

[root@centos8 ~]#curl -I -u haadmin:123456  http://10.0.0.100:9999/haproxy-status
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html

[root@centos8 ~]#echo $?
0

[root@haproxy ~]#systemctl stop haproxy

[root@centos8 ~]#curl -I  http://haadmin:123456@10.0.0.100:9999/haproxy-status
curl: (7) Failed to connect to 10.0.0.100 port 9999: Connection refused
[root@centos8 ~]#echo $?7
'''

---------------------------

haproxy  - IP 透传

web服务器中需要记录客户端的真实IP地址，用于做访问统计、安全防护、行为分析、区域排行等场景。

layer 4 与 layer 7
四层：IP+PORT转发

七层：协议+内容交换

haproxy-IP透传插图

四层负载
在四层负载设备中，把client发送的报文目标地址(原来是负载均衡设备的IP地址)，根据均衡设备设置的选择web服务器的规则选择对应的web服务器IP地址，这样client就可以直接跟此服务器建立TCP连接并发送数据，而四层负载自身不参与建立连接，而和LVS不同，haproxy是伪四层负载均衡，因为haproxy 需要分别和前端客户端及后端服务器建立连接

七层代理
七层负载均衡服务器起了一个反向代理服务器的作用，服务器建立一次TCP连接要三次握手，而client要访问webserver要先与七层负载设备进行三次握手后建立TCP连接，把要访问的报文信息发送给七层负载均衡；然后七层负载均衡再根据设置的均衡规则选择特定的webserver，然后通过三次握手与此台webserver建立TCP连接，然后webserver把需要的数据发送给七层负载均衡设备，负载均衡设备再把数据发送给client；所以，七层负载均衡设备起到了代理服务器的作用，七层代理需要和Client和后端服务器分别建立连接

'''
[root@haproxy ~]#tcpdump  tcp  -i eth0   -nn port ! 22  -w dump-tcp.pcap  -v
[root@haproxy ~]#tcpdump  tcp  -i eth1   -nn port ! 22  -w dump-tcp2.pcap -v
'''

haproxy-IP透传插图(1)
haproxy-IP透传插图(2)

四层IP透传
'''
#haproxy 配置：
listen  web_prot_http_nodes
    bind  172.16.0.100:80
    mode  tcp
    balance roundrobin
    server web1 www.wangxiaochun.com:80  send-proxy  check inter 3000 fall 3 rise 5

#nginx配置：变量$proxy_protocol_addr 记录透传过来的客户端IP
http {
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" "$proxy_protocol_addr"'
       server {
            listen       80 proxy_protocol; #启用此项，将无法直接访问此网站，只能通过四层代理访问
            server_name www.wangxiaochun.com;
......
'''

抓包可以看到
'''
continuation
'''
信息中带有客户端的源IP

haproxy-IP透传插图(3)

'''
#nginx在开启proxy_protocol前
[root@internet ~]#curl 172.16.0.100
<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx</center>
</body>
</html>

[root@VM_0_10_centos ~]# tail -f /apps/nginx/logs/nginx.access.log
111.199.187.69 - - [09/Apr/2020:20:48:51 +0800] "PROXY TCP4 10.0.0.100 58.87.87.99 35948 80" sendfileon
111.199.187.69 - - [09/Apr/2020:20:48:54 +0800] "PROXY TCP4 10.0.0.100 58.87.87.99 35952 80" sendfileon
111.199.187.69 - - [09/Apr/2020:20:48:57 +0800] "PROXY TCP4 10.0.0.100 58.87.87.99 35954 80" sendfileon

#在nginx服务器上开启日志格式和proxy_protocal
[root@VM_0_10_centos ~]# vim /apps/nginx/conf/nginx.conf
http {
.......
log_format  main  '$remote_addr - $remote_user [$time_local] "$request" "$proxy_protocol_addr"'
    sendfile        on;
    keepalive_timeout  65;
    client_max_body_size 100m;
    server {
        listen       80 default_server proxy_protocol ;
......

#nginx在开启proxy_protocol后，可以看客户端真实源IP
[root@VM_0_10_centos ~]# tail -f /apps/nginx/logs/nginx.access.log
111.199.187.69 - - [09/Apr/2020:20:52:52 +0800] "GET / HTTP/1.1" "172.16.0.200"sendfileon
'''


七层IP透传
当haproxy工作在七层的时候，如何透传客户端真实IP至后端服务器

HAProxy配置
在由haproxy发往后端主机的请求报文中添加“X-Forwarded-For”首部，其值为前端客户端的地址；用于向后端主发送真实的客户端IP

'''
option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
[ except <network> ]：请求报请来自此处指定的网络时不予添加此首部，如haproxy自身所在网络
[ header <name> ]：使用自定义的首部名称，而非“X-Forwarded-For”，示例：X-client
[ if-none ]  如果没有首部才添加首部，如果有使用默认值
'''

范例：

'''
#haproxy 配置
defaults

option  forwardfor   #此为默认值,首部字段默为：X-Forwarded-For
#或者自定义首部为X-client：
option forwardfor except 127.0.0.0/8 header X-client 

#listen配置
listen  web_host
  bind 10.0.0.7:80
  mode http
  log global
  balance  random
  server web1 10.0.0.17:80 weight 1  check inter 3000 fall 2 rise 5
  server web2 10.0.0.27:80 weight 1  check inter 3000 fall 2 rise 5
'''

web服务器日志格式配置

配置web服务器，记录负载均衡透传的客户端IP地址

'''
#apache 配置：
LogFormat "%{X-Forwarded-For}i %a  %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

#nginx 日志格式：
$proxy_add_x_forwarded_for：包括客户端IP和中间经过的所有代理的IP
$http_x_forwarded_For：只有客户端IP

log_format  main  '"$proxy_add_x_forwarded_for" - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" $http_x_forwarded_For';

[root@centos8 ~]#tail /var/log/nginx/access.log
"172.16.0.200, 10.0.0.100" 10.0.0.100 - - [09/Apr/2020:19:10:16 +0800] "GET / HTTP/1.1" 200 4057 "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2" "172.16.0.200" 

#tomcat 配置：conf目录下的server.xml
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
   prefix="localhost_access_log" suffix=".txt"
   pattern="%{X-Forwarded-For}i %h %l %u %t "%r" %s %b" />     
'''
  
验证客户端IP地址

apache日志：

'''
[root@centos7 ~]#vim /etc/httpd/conf/httpd.conf 
LogFormat "%{X-Forwarded-For}i %h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
[root@centos7 ~]#systemctl restart httpd

[root@centos6 ~]#hostname -I
10.0.0.6 
[root@centos6 ~]#curl   http://10.0.0.7
10.0.0.17
[root@centos7 ~]#tail -f /var/log/httpd/access_log 
10.0.0.6 10.0.0.7 - - [01/Apr/2020:01:08:31 +0800] "GET / HTTP/1.1" 200 10 "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2"
10.0.0.6 10.0.0.7 - - [01/Apr/2020:01:08:33 +0800] "GET / HTTP/1.1" 200 10 "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2"
'''

--------------------------

haproxy - 报文修改

报文修改
在http模式下，基于实际需求修改客户端的请求报文与响应报文，通过reqadd和reqdel在请求报文添加删除字段，通过rspadd与rspidel在响应报文中添加与删除字段。

注意：此功能的以下相关指令在2.1版本中已经取消

官方文档：参看2.0的帮助文档

'''
http://cbonte.github.io/haproxy-dconv/2.0/configuration.html#4-rspadd
'''

'''
#在向后端服务器转发的请求报文尾部添加指定首部
  reqadd  <string> [{if | unless} <cond>]
  示例：reqadd X-Via:\ HAPorxy

#在向后端服务器转发的请求报文中删除匹配正则表达式的首部
  reqdel  <search> [{if | unless} <cond>]
  reqidel  <search> [{if | unless} <cond>]   #忽略大小写
  示例：reqidel user-agent

#在向前端客户端转发的响应报文尾部添加指定首部
  rspadd <string> [{if | unless} <cond>]        
  示例：
  rspadd X-Via:\ HAPorxy    
  rspadd  Server:\ wanginx

#从向前端客户端转发的响应报文中删除匹配正则表达式的首部
  rspdel  <search> [{if | unless} <cond>]
  rspidel <search> [{if | unless} <cond>]   #忽略大小写
  示例： 
  rspidel  ^server:.*           #从响应报文删除server信息
  rspidel  X-Powered-By:.*      #从响应报文删除X-Powered-By信息,一般此首部字段保存php版本信息
'''

2.1版本以上用下面指令http-request和http-response代替

官方文档：

'''
http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#4-http-request
http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#4-http-response
'''


配置说明：

'''
http-request add-header <name> <fmt> [ { if | unless } <condition> ]
示例：http-request add-header X-Haproxy-Current-Date %T
http-request del-header <name> [ { if | unless } <condition> ]

http-response add-header <name> <fmt> [ { if | unless } <condition> ]
http-response del-header <name>
#示例：
http-response del-header Server 
'''

范例：

'''
#添加向后端报务器发起的请求报文首部
vim haproxy.cfg
frontend main *:80
#       bind *:80
        default_backend websrvs
        reqadd  testheader:\  haporxyserver   加此行,只有一 个空格，并需要转义

#在后端httpd服务器
vim /etc/httpd/conf/httpd.conf
LogFormat "%{testheader}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

#查看日志
tail –f /var/log/httpd/acesss_log 
'''


范例：

'''
#添加响应报文首部
vim haproxy.cfg
frontend main *:80
#       bind *:80
        default_backend websrvs
        rspadd X-Via:\ HAPorxy-1   #加此行
        maxconn         5000

#客户端访问调试模式,查看reponse headers，看到 
Server: Apache/2.2.15 (CentOS) 系统自带显示
X-Via: HAPorxy-1
'''


范例：

'''
#删除响应报文中的server首部
vim haproxy.cfg
frontend main *:80
#       bind *:80
        default_backend websrvs
        rspadd X-Via:\ HAPorxy-1
        rspdel Server  或者 rspidel server    #加此行 ,忽略大小写
        rspidel  X-Powered-By:.*             #删除Php版本
        maxconn         5000

#客户端访问调试模式,查看reponse headers，看到 
Server: Apache/2.2.15 (CentOS)  此行消失
X-Via: HAPorxy-1
'''

范例：

'''
#增加响应报文的首部，实现伪装Server首部
vim haproxy.cfg
frontend main *:80
#       bind *:80
        default_backend websrvs
        rspadd X-Via:\ HAPorxy-1
        rspdel Server  #或者 rspidel server 
        rspadd Server:\   wanginx   #增加此行 

[root@internet ~]#curl  -i   172.16.0.100
HTTP/1.1 200 OK
date: Thu, 09 Apr 2020 08:32:10 GMT
last-modified: Thu, 09 Apr 2020 01:23:18 GMT
etag: "f-5a2d17630635b"
accept-ranges: bytes
content-length: 15
content-type: text/html; charset=UTF-8
server: wanginx

RS1 10.0.0.17 
'''

范例：

'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
listen  web_port
 bind 10.0.0.7:80
 http-request add-header X-Haproxy-Current-Date %T
 http-response del-header server
 mode http 
 log global
 option httpchk
 http-check expect status 200
 server web1  10.0.0.17:80  check inter 3000 fall 2 rise 5 
 server web2  10.0.0.27:80  check inter 3000 fall 2 rise 5 

#查看后端服务器日志
tail –f /var/log/httpd/acesss_log
10.0.0.7 - - [05/Apr/2020:20:13:48 +0800] "GET / HTTP/1.1" 200 10 "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) l
ibcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2" "05/Apr/2020:12:13:48 +0000"
'''


--------------------------------

haproxy - 自定义日志格式

log global 开启日志功能，默认只会在记录下面格式的日志

'''
[root@haproxy ~]#tail /var/log/haproxy.log
Apr  9 19:38:46 localhost haproxy[60049]: Connect from 172.16.0.200:54628 to 172.16.0.100:80 (web_prot_http_nodes/HTTP)
'''


option httplog 可以将http格式记录下，并且可以使用相关指令将特定信息记录在haproxy的日志中

但一般不建议开启，这会加重 HAProxy 负载

配置选项
'''
log global                                  #开启记录日志,默认不开启
option httplog                              #开启记录httplog日志格式选项
capture cookie <name> len <length>          #捕获请求和响应报文中的 cookie并记录日志    
capture request header <name> len <length>  #捕获请求报文中指定的首部内容和长度并记录日志
capture response header <name> len <length> #捕获响应报文中指定的内容和长度首部并记录日志

#示例：
log global  
option httplog
capture request header Host len  256
capture request header User-Agent len 512   
capture request header Referer len 15
capture request header X-Forwarded-For len 15
'''


只开启日志功能log global和option httplog，记录日志格式如下

'''
[root@haproxy ~]#tail /var/log/haproxy.log
Apr  9 19:42:02 localhost haproxy[60236]: 172.16.0.200:54630 [09/Apr/2020:19:42:02.623] web_prot_http_nodes web_prot_http_nodes/web1 0/0/1/1/2 200 4264 - - ---- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
'''


配置示例
'''
listen  web_host
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global                                        #开启日志功能
  option httplog                                    #开启httplog日志格式选项
  capture request header User-Agent len 512         #记录日志信息
  capture request header Host len  256              #记录日志信息
  cookie  SERVER-COOKIE  insert  indirect nocache
  server web1 10.0.0.17:80  cookie web1 check inter 3000 fall 3 rise 5
  server web2 10.0.0.27:80  cookie web2 check inter 3000 fall 3 rise 5
'''


验证日志格式
'''
[root@centos7 ~]#tail -n3 /var/log/haproxy.log
Apr  2 12:44:26 localhost haproxy[27637]: 10.0.0.6:50004 [02/Apr/2020:12:44:26.817] web_port web_port/web1 0/0/0/2/3 200 42484 - - --NI 1/1/0/0/0 0/0 {curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2|10.0.0.7} "GET /test.php HTTP/1.1"
Apr  2 12:44:27 localhost haproxy[27637]: 10.0.0.6:50006 [02/Apr/2020:12:44:27.294] web_port web_port/web2 0/0/0/1/1 404 370 - - --NI 1/1/0/0/0 0/0 {curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2|10.0.0.7} "GET /test.php HTTP/1.1"
Apr  2 12:44:27 localhost haproxy[27637]: 10.0.0.6:50008 [02/Apr/2020:12:44:27.840] web_port web_port/web1 0/0/0/3/4 200 42484 - - --NI 1/1/0/0/0 0/0 {curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2|10.0.0.7} "GET /test.php HTTP/1.1"
'''


-------------------------

haproxy  - 压缩功能

对响应给客户端的报文进行压缩，以节省网络带宽，但是会占用部分CPU性能，建议在后端服务器开启压缩功能，而非在HAProxy上开启压缩

配置选项
'''
compression algo  <algorithm> ...         #启用http协议中的压缩机制，常用算法有gzip，deflate
<algorithm>支持下面类型：
  identity                                  #debug调试使用的压缩方式
  gzip                                      #常用的压缩方式，与各浏览器兼容较好
  deflate                                   #有些浏览器不支持
  raw-deflate                               #新式的压缩方式

compression type <mime type> ...          #要压缩的文件类型

#示例：
compression algo gzip deflate
compression type text/html text/csstext/plain 
'''


配置示例
'''
listen  web_host
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
  compression algo gzip deflate
  compression type compression type text/plain text/html text/css text/xml text/javascript application/javascript
  server web1 10.0.0.17:80  cookie web1 check inter 3000 fall 3 rise 5
  server web2 10.0.0.27:80  cookie web2 check inter 3000 fall 3 rise 5

#后端服务器准备一个文本文件
[root@centos7 ~]#ll /var/www/html/m.txt  -h
-rwxr-xr-x 1 root root 772K Apr  2 12:56 /var/www/html/m.txt
'''

 
验证压缩功能
'''
[root@centos6 ~]#curl  -is --compressed   10.0.0.7/m.txt|less
HTTP/1.1 200 OK
date: Thu, 02 Apr 2020 05:00:26 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
last-modified: Thu, 02 Apr 2020 04:56:25 GMT
etag: W/"c0ef6-5a2479f7aee68"
accept-ranges: bytes
content-type: text/plain; charset=UTF-8
set-cookie: WEBSRV=web1; path=/
cache-control: private
content-encoding: deflate
transfer-encoding: chunked
vary: Accept-Encoding

Feb  2 18:49:27 centos7 journal: Runtime journal is using 6.0M (max allowed 48.6M, trying to leave 72.9M free of 480.1M available → current limit 48.6M).
Feb  2 18:49:27 centos7 kernel: Initializing cgroup subsys cpuset
Feb  2 18:49:27 centos7 kernel: Initializing cgroup subsys cpu
Feb  2 18:49:27 centos7 kernel: Initializing cgroup subsys cpuacct
......
'''

haproxy-压缩功能插图
haproxy-压缩功能插图(1)


-----------------------------------

haproxy - web服务器状态监测


三种状态监测方式
'''
基于四层的传输端口做状态监测，此为默认方式
基于指定 URI 做状态监测
基于指定 URI 的request请求头部内容做状态监测，建议使用此方式
'''

基于应用层http协议进行健康性检测

基于应用层http协议，采有不同的监测方式，对后端real server进行状态监测

'''
option httpchk          #启用七层健康性检测，对tcp 和 http 模式都支持，默认为：OPTIONS / HTTP/1.0
option httpchk <uri>
option httpchk <method> <uri>
option httpchk <method> <uri> <version>

#期望以上检查得到的响应码
http-check expect [!] <match> <pattern>
#示例：
http-check expect status 200
http-check expect ! rstatus ^5

<version> is the optional HTTP version string. It defaults to "HTTP/1.0"
          but some servers might behave incorrectly in HTTP 1.0, so turning
          it to HTTP/1.1 may sometimes help. Note that the Host field is
          mandatory in HTTP/1.1, and as a trick, it is possible to pass it
          after "\r\n" following the version string.
'''


配置示例
'''
listen  web_host
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  #option httpchk GET /monitor/check.html               #默认HTTP/1.0
  #option httpchk GET /monitor/check.html HTTP/1.0
  #option httpchk GET /monitor/check.html HTTP/1.1      #注意：HTTP/1.1强制要求必须有Host字段
  option httpchk HEAD  /monitor/check.html HTTP/1.1\r\nHost:\ 10.0.0.7 #使用HEAD减少网络流量
  cookie  SERVER-COOKIE  insert  indirect nocache
  server web1 10.0.0.17:80  cookie web1 check inter 3000 fall 3 rise 5
  server web2 10.0.0.27:80  cookie web2 check inter 3000 fall 3 rise 5

#在所有后端服务建立检测页面
[root@backend ~]#mkdir /var/www/html/monitor/
[root@backend ~]#echo  monitor > /var/www/html/monitor/check.html

#关闭一台Backend服务器
[root@backend1 ~]#systemctl stop httpd
'''


验证http监测

查看到状态页，可以看到启了七层检测功能：LastChk字段：L7

haproxy-web服务器状态监测插图

'''
#后端服务器查看访问日志
[root@backend ~]#tail /var/log/httpd/access_log
10.0.0.7 - - [02/Apr/2020:14:25:22 +0800] "HEAD /monitor/check.html HTTP/1.1" 200 - "-" "-"
10.0.0.7 - - [02/Apr/2020:14:25:25 +0800] "HEAD /monitor/check.html HTTP/1.1" 200 - "-" "-"
10.0.0.7 - - [02/Apr/2020:14:25:28 +0800] "HEAD /monitor/check.html HTTP/1.1" 200 - "-" "-"
'''

---------------------------

haproxy - ACL 基础介绍

访问控制列表（ACL，Access Control Lists）是一种基于包过滤的访问控制技术，它可以根据设定的条件对经过服务器传输的数据包进行过滤(条件匹配)，即对接收到的报文进行匹配和过滤，基于请求报文头部中的源地址、源端口、目标地址、目标端口、请求方法、URL、文件后缀等信息内容进行匹配并执行进一步操作，比如允许其通过或丢弃。

官方帮助：

'''
http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#7
http://cbonte.github.io/haproxy-dconv/2.0/configuration.html#7
'''

ACL配置选项
'''
acl   <aclname>  <criterion>   [flags]     [operator]    [<value>]
acl      名称      匹配规范      匹配模式     具体操作符     操作对象类型
'''

ACL-Name
'''
acl   image_service hdr_dom(host)   -i   img.magedu.com

#ACL名称，可以使用大字母A-Z、小写字母a-z、数字0-9、冒号：、点.、中横线和下划线，并且严格区分大小写，比如Image_site和image_site就是两个完全不同的acl
'''

ACL-criterion
定义ACL匹配规范，即：判断条件

'''
hdr string，提取在一个HTTP请求报文的首部
hdr（[<name> [，<occ>]]）：完全匹配字符串,header的指定信息，<occ> 表示在多值中使用的值的出现次数
hdr_beg（[<name> [，<occ>]]）：前缀匹配，header中指定匹配内容的begin
hdr_end（[<name> [，<occ>]]）：后缀匹配，header中指定匹配内容end
hdr_dom（[<name> [，<occ>]]）：域匹配，header中的domain name
hdr_dir（[<name> [，<occ>]]）：路径匹配，header的uri路径
hdr_len（[<name> [，<occ>]]）：长度匹配，header的长度匹配
hdr_reg（[<name> [，<occ>]]）：正则表达式匹配，自定义表达式(regex)模糊匹配
hdr_sub（[<name> [，<occ>]]）：子串匹配，header中的uri模糊匹配

#示例：
hdr(<string>)     用于测试请求头部首部指定内容
hdr_dom(host)   请求的host名称，如 www.magedu.com
hdr_beg(host)   请求的host开头，如 www.   img.   video.   download.   ftp.
hdr_end(host)   请求的host结尾，如 .com   .net   .cn 

#示例：
acl bad_agent hdr_sub(User-Agent) -i curl wget
block if bad_agent

#有些功能是类似的，比如以下几个都是匹配用户请求报文中host的开头是不是www：
acl short_form  hdr_beg(host)        www.
acl alternate1  hdr_beg(host) -m beg www.
acl alternate2  hdr_dom(host) -m beg www.
acl alternate3  hdr(host)     -m beg www.

base : string
#返回第一个主机头和请求的路径部分的连接，该请求从第一个斜杠开始，并在问号之前结束,对虚拟主机有用
<scheme>://<user>:<password>@#<host>:<port>/<path>;<params>#?<query>#<frag>
    base     : exact string match
    base_beg : prefix match
    base_dir : subdir match
    base_dom : domain match
    base_end : suffix match
    base_len : length match
    base_reg : regex match
    base_sub : substring match

path : string
#提取请求的URL路径，该路径从第一个斜杠开始，并在问号之前结束（无主机部分）
<scheme>://<user>:<password>@<host>:<port>#/<path>;<params>#?<query>#<frag>
    path     : exact string match
    path_beg : prefix match  #请求的URL开头，如/static、/images、/img、/css
    path_end : suffix match  #请求的URL中资源的结尾，如 .gif  .png  .css  .js  .jpg  .jpeg
    path_dom : domain match
    path_dir : subdir match
    path_len : length match
    path_reg : regex match
    path_sub : substring match

#示例：
    path_beg -i /haproxy-status/ 
    path_end .jpg .jpeg .png .gif 
    path_reg ^/images.*\.jpeg$ 
    path_sub image  
    path_dir jpegs 
    path_dom magedu

url : string
#提取请求中的URL。一个典型的应用是具有预取能力的缓存，以及需要从数据库聚合多个信息并将它们保存在缓存中的网页门户入口，推荐使用path
    url  ：exact string match
    url_beg : prefix match
    url_dir : subdir match
    url_dom : domain match
    url_end : suffix match
    url_len : length match
    url_reg : regex match
    url_sub : substring match

dst         #目标IP
dst_port    #目标PORT

src         #源IP
src_port    #源PORT

#示例：
acl invalid_src src 10.0.0.100 192.168.1.0/24
acl invalid_port src_port 0:1023

status : integer
#返回在响应报文中的状态码   

#七层协议
acl valid_method method GET HEAD
http-request deny if ! valid_method
'''


ACL-flags
ACL匹配模式

'''
-i 不区分大小写
-m 使用指定的pattern匹配方法
-n 不做DNS解析
-u 禁止acl重名，否则多个同名ACL匹配或关系
'''

ACL-operator
ACL 操作符

'''
整数比较：eq、ge、gt、le、lt
字符比较：
- exact match     (-m str) :字符串必须完全匹配模式
- substring match (-m sub) :在提取的字符串中查找模式，如果其中任何一个被发现，ACL将匹配
- prefix match    (-m beg) :在提取的字符串首部中查找模式，如果其中任何一个被发现，ACL将匹配
- suffix match    (-m end) :将模式与提取字符串的尾部进行比较，如果其中任何一个匹配，则ACL进行匹配
- subdir match    (-m dir) :查看提取出来的用斜线分隔（“/”）的字符串，如其中任一个匹配，则ACL进行匹配
- domain match    (-m dom) :查找提取的用点（“.”）分隔字符串，如果其中任何一个匹配，则ACL进行匹配
'''


ACL-value
value的类型

'''
The ACL engine can match these types against patterns of the following types :
- Boolean                       #布尔值
- integer or integer range      #整数或整数范围，比如用于匹配端口范围
- IP address / network          #IP地址或IP范围, 192.168.0.1 ,192.168.0.1/24
- string--> www.magedu.com
  exact –精确比较
  substring—子串
  suffix-后缀比较
  prefix-前缀比较
  subdir-路径， /wp-includes/js/jquery/jquery.js
  domain-域名，www.magedu.com
- regular expression            #正则表达式
- hex block                     #16进制
'''

ACL调用方式
ACL调用方式：

'''
与：隐式（默认）使用
或：使用“or” 或 “||”表示
否定：使用 "!" 表示  

#示例：
if valid_src valid_port         #与关系，A和B都要满足为true，默认为与
if invalid_src || invalid_port  #或，A或者B满足一个为true
if ! invalid_src                #非，取反，A和B哪个也不满足为true
'''


-------------------------

haproxy  - ACL案例

http://www.yunweipai.com/35302.html

ACL示例-域名匹配
'''
[root@centos7 ~]#cat /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog

###################### acl setting ###############################
  acl pc_domain  hdr_dom(host)      -i www.magedu.org
  acl mobile_domain hdr_dom(host)   -i mobile.magedu.org

###################### acl hosts #################################
  use_backend  pc_hosts         if   pc_domain
  use_backend  mobile_hosts     if   mobile_domain
  default_backend pc_hosts 

###################### backend hosts #############################
backend mobile_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5
'''

测试结果：

'''
[root@centos6 ~]#cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 centos6.localdomain
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.0.0.7 mobile.magedu.org  www.magedu.org magedu.org 

[root@centos6 ~]#curl www.magedu.org
10.0.0.27
[root@centos6 ~]#curl mobile.magedu.org
10.0.0.17
[root@centos6 ~]#curl magedu.org
10.0.0.27
'''

ACL示例-基于源IP或子网调度访问

将指定的源地址调度至指定的web服务器组。

'''
root@centos7 ~]#cat /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog

###################### acl setting ###############################
  acl pc_domain  hdr_dom(host)      -i www.magedu.org
  acl mobile_domain hdr_dom(host)   -i mobile.magedu.org
  acl ip_range_test src 172.18.0.0/16 10.0.0.6

###################### acl hosts #################################
  use_backend  pc_hosts         if  ip_range_test   #放在第一行优先生效
  use_backend  pc_hosts         if   pc_domain
  use_backend  mobile_hosts     if   mobile_domain
  default_backend pc_hosts 

###################### backend hosts #############################
backend mobile_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5 
'''


测试结果

'''
[root@centos6 ~]#hostname -I
10.0.0.6 
[root@centos6 ~]#curl www.magedu.org
10.0.0.27
[root@internet ~]#curl -H "HOST: www.magedu.org" 10.0.0.7
10.0.0.27
[root@centos6 ~]#curl mobile.magedu.org
10.0.0.27
[root@centos6 ~]#curl magedu.org
10.0.0.27
[root@centos8 ~]#curl mobile.magedu.org
10.0.0.17
[root@centos8 ~]#curl www.magedu.org
10.0.0.27
[root@centos8 ~]#curl magedu.org
10.0.0.27
'''

 
ACL示例-基于源地址的访问控制
拒绝指定IP或者IP范围访问

'''
listen  web_host
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog

###################### acl setting ###############################
  acl acl_deny_src src 10.0.0.6 192.168.0.0/24

###################### acl hosts #################################
  #block  if  acl_deny_src
  http-request deny  if acl_deny_src  #2.1版本后，不再支持block
  #http-request allow
  default_backend default_web
###################### backend hosts #############################
backend magedu_host
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend default_web
  mode http
  server web1 10.0.0.27:80 check inter 2000 fall 3 rise 5
'''


测试：

'''
[root@centos6 ~]#curl www.magedu.org
<html><body><h1>403 Forbidden</h1>
Request forbidden by administrative rules.
</body></html>
'''

ACL示例-匹配浏览器类型

匹配客户端浏览器，将不同类型的浏览器调动至不同的服务器组

'''
[root@centos7 ~]#cat /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################
  acl acl_user_agent    hdr_sub(User-Agent)  -i curl wget
  acl acl_user_agent_ab hdr_sub(User-Agent)  -i ApacheBench

###################### acl hosts #################################
  redirect prefix   http://10.0.0.8 if acl_user_agent               #301临时重定向至新URL
  http-request deny                 if acl_user_agent_ab            #拒绝ab
  default_backend pc_hosts 
###################### backend hosts #############################
backend mobile_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5
'''


范例：

'''
[root@centos6 ~]#curl -I 10.0.0.7
HTTP/1.1 302 Found
content-length: 0
location: http://10.0.0.8/
cache-control: no-cache

[root@centos6 ~]#curl -L 10.0.0.7
10.0.0.8
[root@centos6 ~]#wget -O -  -q http://10.0.0.7
10.0.0.8
[root@centos6 ~]#curl -A chrome http://10.0.0.7
10.0.0.27

#模拟ab
[root@centos6 ~]#curl -A ApacheBench 10.0.0.7
<html><body><h1>403 Forbidden</h1>
Request forbidden by administrative rules.
</body></html>

[root@centos6 ~]#ab  -n1 -c 1 http://10.0.0.7/
This is ApacheBench, Version 2.3 <$Revision: 655654 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 10.0.0.7 (be patient).....done

Server Software:        
Server Hostname:        10.0.0.7
Server Port:            80

Document Path:          /
Document Length:        93 bytes

Concurrency Level:      1
Time taken for tests:   0.001 seconds
Complete requests:      1
Failed requests:        0
Write errors:           0
Non-2xx responses:      1                   #提示出现非200的响应
Total transferred:      208 bytes
HTML transferred:       93 bytes
Requests per second:    939.85 [#/sec] (mean)
Time per request:       1.064 [ms] (mean)
Time per request:       1.064 [ms] (mean, across all concurrent requests)
Transfer rate:          190.91 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        1    1   0.0      1       1
Processing:     1    1   0.0      1       1
Waiting:        0    0   0.0      0       0
Total:          1    1   0.0      1       1

#haproxy日志提示403
[root@centos7 ~]#tail /var/log/haproxy.log
Apr  4 08:16:29 localhost haproxy[1483]: 10.0.0.6:56470 [04/Apr/2020:08:16:29.977] magedu_http_port magedu_http_port/<NOSRV> 0/-1/-1/-1/0 403 212 - - PR-- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
'''


ACL示例-基于文件后缀名实现动静分离
'''
[root@centos7 ~]#cat /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################
  acl acl_static path_end -i .jpg .jpeg .png .gif .css .js
  acl acl_php   path_end -i .php
###################### acl hosts #################################
  use_backend  mobile_hosts if acl_static
  use_backend  app_hosts if acl_php
  default_backend pc_hosts 
###################### backend hosts #############################
backend mobile_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5

backend app_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5

#分别在后端两台主机准备相关文件
[root@centos17 ~]#ls /var/www/html
index.html  wang.jpg

[root@centos27 ~]#cat /var/www/html/test.php
<?php
echo "<h1>http://10.0.0.27/test.php</h1>\n";
?>
'''


haproxy-ACL案例插图
haproxy-ACL案例插图(1)

ACL-匹配访问路径实现动静分离
'''
[root@centos7 ~]#cat /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################
  acl  acl_static  path_beg  -i  /static /images /javascript
  acl  acl_static  path_end  -i .jpg .jpeg .png .gif .css.js

###################### acl hosts #################################
  use_backend static_hosts if acl_static
  default_backend app_hosts 
###################### backend hosts #############################
backend static_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend app_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5

#创建相关文件
[root@centos17 ~]#mkdir /var/www/html/static
[root@centos17 ~]#echo 10.0.0.17 >  /var/www/html/static/test.html

#测试访问
[root@centos6 ~]#curl 10.0.0.7/static/test.html
10.0.0.17
'''


ACL示例-预定义ACL使用
官方帮助文档：http://cbonte.github.io/haproxy-dconv/2.1/configuration.html#7.4
'''
预定义ACL
ACL name	Equivalent to	Usage
FALSE	always_false	never match
HTTP	req_proto_http	match if protocol is valid HTTP
HTTP_1.0	req_ver 1.0	match HTTP version 1.0
HTTP_1.1	req_ver 1.1	match HTTP version 1.1
HTTP_CONTENT	hdr_val(content-length) gt 0	match an existing content-length
HTTP_URL_ABS	url_reg ^[^/:]*://	match absolute URL with scheme
HTTP_URL_SLASH	url_beg /	match URL beginning with "/"
HTTP_URL_STAR	url *	match URL equal to "*"
LOCALHOST	src 127.0.0.1/8	match connection from local host
METH_CONNECT	method CONNECT	match HTTP CONNECT method
METH_DELETE	method DELETE	match HTTP DELETE method
METH_GET	method GET HEAD	match HTTP GET or HEAD method
METH_HEAD	method HEAD	match HTTP HEAD method
METH_OPTIONS	method OPTIONS	match HTTP OPTIONS method
METH_POST	method POST	match HTTP POST method
METH_PUT	method PUT	match HTTP PUT method
METH_TRACE	method TRACE	match HTTP TRACE method
RDP_COOKIE	req_rdp_cookie_cnt gt 0	match presence of an RDP cookie
REQ_CONTENT	req_len gt 0	match data in the request buffer
TRUE	always_true	always match
WAIT_END	wait_end	wait for end of content analysis
'''

预定义ACL使用
'''
[root@centos6 ~]#curl -I -XTRACE 10.0.0.7/static/test.html
HTTP/1.1 200 OK
date: Sat, 04 Apr 2020 02:04:01 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
transfer-encoding: chunked
content-type: message/http

[root@centos7 ~]#cat  /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################
  acl  acl_static_path  path_beg  -i  /static /images /javascript
###################### acl hosts #################################
  use_backend static_path_hosts
  http-request deny if METH_TRACE  HTTP_1.1  #引用预定义的ACL，与关系
  default_backend pc_hosts 
################### backend hosts ################################
backend static_path_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend mobile_hosts
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5

[root@centos6 ~]#curl -I -XTRACE 10.0.0.7/static/test.html
HTTP/1.1 403 Forbidden
content-length: 93
cache-control: no-cache
content-type: text/html
connection: close

[root@centos6 ~]#curl -I -0 -XTRACE 10.0.0.7/static/test.html
HTTP/1.1 200 OK
date: Sat, 04 Apr 2020 02:10:13 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
content-type: message/http
connection: close

#查看日志，观察协议版本
[root@centos17 ~]#tail /var/log/httpd/access_log 
10.0.0.7 - - [04/Apr/2020:10:11:41 +0800] "TRACE /static/test.html HTTP/1.0" 200 230 "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2"

[root@centos6 ~]#curl  -i 10.0.0.7/static/test.html
HTTP/1.1 200 OK
date: Sat, 04 Apr 2020 02:07:58 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
last-modified: Sat, 04 Apr 2020 01:27:45 GMT
etag: "a-5a26cf0ed4913"
accept-ranges: bytes
content-length: 10
content-type: text/html; charset=UTF-8
10.0.0.17
'''

----------------------------

haproxy - 自定义 HA Proxy页面

自定义HAProxy错误界面

对指定的报错进行重定向，进行优雅的显示错误页面

haproxy-自定义HAProxy页面插图

默认情况下，所有后端服务器都down机后，会显示下面页面

haproxy-自定义HAProxy页面插图(1)

基于错误页面文件
使用errorfile和errorloc指令，可以自定义各种错误页面

'''
#自定义错误页 
errorfile <code> <file> 
<code> #HTTP status code.支持200, 400, 403, 405, 408, 425, 429, 500, 502，503,504
<file> #包含完整HTTP响应的错误页文件的绝对路径。 建议后缀“ .http”，以和一般的html文件相区分
#示例：
    errorfile 400 /etc/haproxy/errorfiles/400badreq.http
    errorfile 403 /etc/haproxy/errorfiles/403forbid.http
    errorfile 503 /etc/haproxy/errorfiles/503sorry.http 

#错误页面重定向
errorloc <code> <url>
#相当于errorloc302 <code> <url>，利用302重定向至指URL

#示例：
errorloc 503 http://www.magedu.com/error_pages/503.html
'''

范例：

'''
defaults
#option  forwardfor
#no option http-use-htx  此设置和版本有关，2.1不支持
#...... 
#加下面行

errorfile 500  /usr/local/haproxy/html/500.http
errorfile 502  /usr/local/haproxy/html/502.http
errorfile 503  /usr/local/haproxy/html/503.http
'''


范例：

'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
defaults
option http-keep-alive
option  forwardfor
maxconn 100000
mode http
timeout connect 300000ms
timeout client  300000ms
timeout server  300000ms
errorfile 503 /apps/haproxy/html/503.http  

listen
.......

[root@centos7 ~]#vim /apps/haproxy/html/503.http 
HTTP/1.1 503 Service Unavailable
Content-Type:text/html;charset=utf-8

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>报错页面</title>
</head>
<body>
<center><h1>网站维护中......请稍侯再试</h1></center>
<center><h2>联系电话：400-123-4567</h2></center>
<center><h3>503 Service Unavailable</h3></center>
</body>

[root@centos7 ~]#systemctl restart haproxy
#将后端服务器down，可以观察到以下页面
'''


haproxy-自定义HAProxy页面插图(2)

5.9.2：基于http重定向
'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
defaults
#option http-keep-alive
#option  forwardfor
#no option http-use-htx
#...... 加以下一行
#errorfile 503 /apps/haproxy/html/503.http
errorloc 503 http://10.0.0.8/error_page/503.html

[root@centos8 ~]#cat /var/www/html/error_page/503.html
<!DOCTYPE html>
<html lang="en">
<head>
<title>报错页面</title>
</head>
<body>
<center><h1>网站维护中......请稍侯再试</h1></center>
<center><h2>联系电话：400-123-4567</h2></center>
<center><h3>503 Service Unavailable</h3></center>
</body>

#浏览器访问http://haproxy/ 302自动跳转至下面页面
'''

haproxy-自定义HAProxy页面插图(3)

本文链接：http://www.yunweipai.com/35306.html


---------------------------------

Haproxy  -  实现四层负载

针对有特殊访问写完的应用场景

'''
MySQL
Redis
Memcache
RabbitMQ
'''

四层负载示例
注意：如果使用frontend和backend，一定在frontend和backedn段中都指定mode tcp

'''
listen redis-port
    bind 10.0.0.7:6379
    mode tcp
    balance leastconn
    server server1 10.0.0.17:6379 check
    server server1 10.0.0.27:6379 check backup
'''

范例：对 MySQL 服务实现四层负载

'''
[root@centos7 ~]#vim /etc/haproxy/haproxy.cfg
listen magedu_mysql
    bind 10.0.0.7:3306
    mode tcp
    balance leastconn
    server mysql1 10.0.0.17:3306 check  
    server mysql2 10.0.0.27 check           #不写端口号，可以转发，但无法check状态

#或者使用frontend和backend实现
frontend mysql
        bind :3306
        mode tcp                            #必须指定tcp模式
        default_backend mysqlsrvs
backend mysqlsrvs
        mode tcp                            #必须指定tcp模式
        balance leastconn
        server mysql1 10.0.0.17:3306
        server mysql2 10.0.0.27:3306

[root@centos7 ~]#systemctl restart haproxy

#在后端服务器安装和配置mariadb服务
[root@centos7 ~]#yum -y install mariadb-server
[root@centos7 ~]#mysql -e "grant all on *.* to test@'10.0.0.%' identified by '123456'"
[root@centos7 ~]#vim /etc/my.cnf
[mysqld]
server-id=17 #在另一台主机为27
[root@centos7 ~]#systemctl start mariadb

#测试
[root@centos6 ~]#mysql -utest -p123456 -e "show variables like 'hostname'"
+---------------+--------------------------+
| Variable_name | Value                    |
+---------------+--------------------------+
| hostname      | centos17.wangxiaochu.com |
+---------------+--------------------------+
[root@centos6 ~]#mysql -utest -p123456 -e "show variables like 'hostname'"
+---------------+--------------------------+
| Variable_name | Value                    |
+---------------+--------------------------+
| hostname      | centos27.wangxiaochu.com |
+---------------+--------------------------+

[root@centos6 ~]#mysql -utest -p123456 -h10.0.0.7 -e 'select @@server_id'
+-------------+
| @@server_id |
+-------------+
|          17 |
+-------------+
[root@centos6 ~]#mysql -utest -p123456 -h10.0.0.7 -e 'select @@server_id'
+-------------+
| @@server_id |
+-------------+
|          27 |
+-------------+
'''


HAProxy-实现四层负载插图

ACL示例-四层访问控制
'''
frontend  web_host
  bind 10.0.0.7:80
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################  
  acl static_path  path_beg  -i  /static /images /javascript
  acl invalid_src src 192.168.1.0/24 10.0.0.8
###################### acl hosts #################################
  use_backend static_path_host if  HTTP_1.1 TRUE static_path
  tcp-request connection reject if invalid_src     #四层ACL控制  
  default_backend default_web 
################### backend hosts ################################
backend php_server_host
  mode http
  server web1 10.0.0.17 check inter 2000 fall 3 rise 5

backend static_path_host
  mode http
  server web1 10.0.0.27 check inter 2000 fall 3 rise 5

backend default_web
  mode http
  server web1 10.0.0.37:80 check inter 2000 fall 3 rise 5
'''

本文链接：http://www.yunweipai.com/35312.html


--------------------------------------

HA Proxy  https  实现

HAProxy https实现
'''
#配置HAProxy支持https协议，支持ssl会话；
    bind *:443 ssl crt /PATH/TO/SOME_PEM_FILE   

#crt 后证书文件为PEM格式，且同时包含证书和所有私钥   
        cat  demo.crt demo.key > demo.pem 

#把80端口的请求重向定443
    bind *:80
    redirect scheme https if !{ ssl_fc }    

#向后端传递用户请求的协议和端口（frontend或backend）
    http_request set-header X-Forwarded-Port %[dst_port]
    http_request add-header X-Forwared-Proto https if { ssl_fc }
'''


证书制作
'''
#方法1
[root@centos7 ~]mkdir /etc/haproxy/certs/
[root@centos7 ~]cd /etc/haproxy/certs/
[root@centos7 certs]#openssl  genrsa -out haproxy.key 2048
[root@centos7 certs]#openssl  req -new -x509 -key haproxy.key  -out haproxy.crt -subj "/CN=www.magedu.org"
#或者用下一条命令实现
[root@centos7 certs]#openssl req  -x509 -newkey rsa:2048 -subj "/CN=www.magedu.org" -keyout haproxy.key -nodes -days 365 -out haproxy.crt

[root@centos7 certs]#cat haproxy.key  haproxy.crt  > haproxy.pem
[root@centos7 certs]#openssl  x509 -in  haproxy.pem -noout -text        #查看证书

#方法2
[root@centos7 ~]#mkdir /etc/haproxy/certs/
[root@centos7 ~]#cd /etc/pki/tls/certs
[root@centos7 certs]#make /etc/haproxy/certs/haproxy.pem 
umask 77 ; \
PEM1=<code>/bin/mktemp /tmp/openssl.XXXXXX</code> ; \
PEM2=<code>/bin/mktemp /tmp/openssl.XXXXXX</code> ; \
/usr/bin/openssl req -utf8 -newkey rsa:2048 -keyout $PEM1 -nodes -x509 -days 365 -out $PEM2  ; \
cat $PEM1 >  /etc/haproxy/certs/haproxy.pem ; \
echo ""    >> /etc/haproxy/certs/haproxy.pem ; \
cat $PEM2 >> /etc/haproxy/certs/haproxy.pem ; \
rm -f $PEM1 $PEM2
Generating a 2048 bit RSA private key
.+++
..............................................+++
writing new private key to '/tmp/openssl.x8hOA8'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:beijing
Locality Name (eg, city) [Default City]:beijing
Organization Name (eg, company) [Default Company Ltd]:magedu
Organizational Unit Name (eg, section) []:it
Common Name (eg, your name or your server's hostname) []:www.magedu.org
Email Address []:
[root@centos7 certs]#ll /etc/haproxy/certs/
total 4
-rw------- 1 root root 3027 Apr  4 10:35 haproxy.pem
'''


https配置示例
'''
[root@centos7 ~]#cat  /etc/haproxy/conf.d/test.cfg
frontend  magedu_http_port
  bind 10.0.0.7:80
  bind 10.0.0.7:443 ssl crt /etc/haproxy/certs/haproxy.pem
  redirect scheme https if !{ ssl_fc }        # 注意{ }内的空格
  http-request  set-header  X-forwarded-Port   %[dst_port]
  http-request  add-header  X-forwarded-Proto  https if { ssl_fc } 
  mode http
  balance  roundrobin
  log global
  option httplog
###################### acl setting ###############################
  acl mobile_domain hdr_dom(host)   -i mobile.magedu.org
###################### acl hosts #################################
  default_backend pc_hosts 
################### backend hosts #################################
backend mobile_hosts
  mode http
  server web1 10.0.0.17:80 check inter 2000 fall 3 rise 5

backend pc_hosts
  mode http
  #http-request  set-header  X-forwarded-Port   %[dst_port] 也可加在此处
  #http-request  add-header  X-forwarded-Proto  https if { ssl_fc } 
  server web2 10.0.0.27:80 check inter 2000 fall 3 rise 5

[root@centos7 ~]#ss -ntl
State      Recv-Q Send-Q          Local Address:Port   Peer Address:Port              
LISTEN     0      100                 127.0.0.1:25                 *:*                  
LISTEN     0      128                  10.0.0.7:443                *:*                  
LISTEN     0      128                         *:9999               *:*                  
LISTEN     0      128                  10.0.0.7:80                 *:*                  
LISTEN     0      128                         *:22                 *:*                  
LISTEN     0      128                      [::]:22                 [::]:*   
'''


修改后端服务器的日志格式
'''
[root@centos27 ~]#vim /etc/httpd/conf/httpd.conf 
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{X-Forwarded-Port}i\" \"%{X-Forwarded-Proto}i\"" combined  
'''


验证https
'''
[root@centos6 ~]#curl -IkL  http://www.magedu.org
HTTP/1.1 302 Found
content-length: 0
location: https://www.magedu.org/
cache-control: no-cache

HTTP/1.1 200 OK
date: Sat, 04 Apr 2020 02:31:31 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
last-modified: Thu, 02 Apr 2020 01:44:13 GMT
etag: "a-5a244f01f8adc"
accept-ranges: bytes
content-length: 10
content-type: text/html; charset=UTF-8

[root@centos6 ~]#curl -Ik  https://www.magedu.org
HTTP/1.1 200 OK
date: Sat, 04 Apr 2020 02:31:50 GMT
server: Apache/2.4.6 (CentOS) PHP/5.4.16
last-modified: Thu, 02 Apr 2020 01:44:28 GMT
etag: "a-5a244f0fd5175"
accept-ranges: bytes
content-length: 10
content-type: text/html; charset=UTF-8

#查看后端服务器的访问日志
[root@centos27 ~]#tail /var/log/httpd/access_log
10.0.0.7 - - [04/Apr/2020:10:40:17 +0800] "HEAD / HTTP/1.1" 200 - "-" "curl/7.19.7 (x86_64-redhat-linux-gnu) libcurl/7.19.7 NSS/3.27.1 zlib/1.2.3 libidn/1.18 libssh2/1.4.2" "443" "https"
'''


HAProxy- https实现插图
HAProxy- https实现插图(1)
HAProxy- https实现插图(2)

本文链接：http://www.yunweipai.com/35315.html


------------------------

https://space.bilibili.com/601631547/video
找到相关的视频资料。









本机测试

下载安装介质：
 http://download.openpkg.org/components/cache/haproxy

可选的安装介质为：
haproxy-1.8.5.tar.gz   
......
haproxy-1.8.15.tar.gz
haproxy-1.9.0.tar.gz
......
haproxy-1.9.8.tar.gz
haproxy-2.0.0.tar.gz
......
haproxy-2.0.9.tar.gz
haproxy-2.1.0.tar.gz
......
haproxy-2.1.7.tar.gz
haproxy-2.2.0.tar.gz
haproxy-2.2.2.tar.gz


下载最新版本 haproxy 安装介质：
wget  http://download.openpkg.org/components/cache/haproxy/haproxy-2.2.2.tar.gz




--------------------


今天下午参加阿里云的内部会议，这次会议主要是针对阿里云国际站的海外客户，有几个与我们相关的重点：

1 为解决RDS主实例升级、迁移、跨region等RDS主库变动的问题，阿里云也建议对于APP和RDS数据库之间，增加一层中间件，是业务程序与数据库解耦合，目前使用的技术是 MaxScale，对mysql RDS支持较好，后续会支持 posgresql RDS；
对应中间件的说明文档为：
https://help.aliyun.com/document_detail/85143.html

2 对于阿里云对于多云平台的支持，主要是通过 DTS数据同步服务 和 DBS数据备份 实现数据同步、数据备份、异地灾备等功能，这些服务可以在阿里云RDS之间进行，也可以在 阿里云RDS与其他云平台数据之间进行，也可以只在其云平台之间进行；
只要网络上能够 DTS，DBS 服务联通就可以；

3 由于国内数据库市场，还是以mysql数据库生态居多，所以RDS功能优先以 mysql RDS为主，然后成熟后应用到其他数据库；目前阿里云内部已经将原来不同数据库团队各自独立的情况，调整为基础服务一个统一团队实现，
比如DAS，监控等服务后续在mysql RDS看到的，和在 PostgreSQL RDS上看到的就是一致的，各种日常运维所需功能，也都会保持一致；

4 阿里云数据库的发展方向是主推云原生数据库 PolarDB ，主要是采用存储计算分离，可以弹性扩展，支持海量存储的功能；现在这个基础上，添加了水平扩展中间件形成 PloarDB-X 云原生分布式数据库，实现云原生+分布式的无限扩展能力。

5 阿里云针对全球业务，准备发布全球跨VPC的统一DNS功能，即全球不同地点的VPC可以访问同一个数据库域名地址，数据库域名地址底层为一主两从，一个主库进行数据写入，其他节点进行数据读取，不同region可以按照数据中心位置，就近读取。
这个功能的支持，会在 PloarDB, postgresql RDS上都支持，这个架构与我们现在做都全球replication架构有类似之处，后续可以对比一下。

6 阿里云推出 云数据库专属集群 MyBase，相比RDS释放了更多可以操作的权限。相关说明为：
https://help.aliyun.com/product/156215.html?spm=a2c4g.11186623.6.540.e36b66efbndjA6

7 阿里云现在整体硬件成本的缩减已经到一定瓶颈了，后续主要会在虚拟化、容器化上作为主要方向，以k8s为中心的云原生技术，扩展了很多技术内容，后续会整合很多产品，应用在阿里云多个方面。
阿里云根据自己的已有了经验，编写了一本《云原生架构白皮书》，我也领了一本，大家感兴趣的话，也可以看一看。


另外对于阿里云上的 ECS vitual IP 的情况确认如下：

1 阿里云前几年支持过一段时间的 HAVIP，可以申请几个ECS上的虚拟漂移IP，现在已经不支持了。
2 对于类似 virtual IP 漂移的功能，阿里云推荐使用 云解析 PrivateZone 实现：
云解析 PrivateZone
https://www.aliyun.com/product/pvtz?spm=5176.10695662.1395782.1.305e1061sG9JXQ
但这种DNS解析，只包括域名地址，不包含port端口。
3 如果临时短时间使用，可以用 ESC端口转发，这种方式和我们前面迁移Account Service数据，可以短时间临时使用下，由于没有高可用机制，不建议长期这样跑。

对于 Google GCP 上不同VM的 virtual IP，目前确认的支持方案如下：

Best Practices for Floating IP Addresses
https://cloud.google.com/solutions/best-practices-floating-ip-addresses#comparing_option_3_to_option_1_internal_tcpudp_load_balancing

这里的option 3和option 4大概就是vip想实现的网络的配置的东西，主要是增加vpc 静态路由。




