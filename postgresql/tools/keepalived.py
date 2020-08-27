
# Keepalived

---------------------------------

高可用集群
集群类型
-LB：Load Balance 负载均衡
​ LVS/HAProxy/nginx（http/upstream, stream/upstream）

-HA：High Availability 高可用集群
​ 数据库、Zookeeper、Redis
​ SPoF: Single Point of Failure，解决单点故障

-HPC：High Performance Computing 高性能集群
​ https://www.top500.org

系统可用性
SLA：Service-Level Agreement

A = MTBF / (MTBF+MTTR）

95%=(602430)*(1-0.9995)

指标 ：99.9%, ..., 99.999%，99.9999%


系统故障
硬件故障：设计缺陷、wear out（损耗）、自然灾害……
软件故障：设计缺陷 bug

实现高可用
提升系统高用性的解决方案：降低MTTR- Mean Time To Repair(平均故障时间)

解决方案：建立冗余机制

active/passive 主/备
active/active 双主
active --> HEARTBEAT --> passive
active <--> HEARTBEAT <--> active


高可用相关技术
HA service：
资源：组成一个高可用服务的“组件”，比如：vip，service process，shared storage

(1) passive node的数量
(2) 资源切换

shared storage：
NAS(Network Attached Storage)：网络附加存储，基于网络的共享文件系统。
SAN(Storage Area Network)：存储区域网络，基于网络的块级别的共享

Network partition 网络分区

quorum 法定人数
with quorum： > total/2
without quorum: <= total/2

隔离设备 fence
node：STONITH = Shooting The Other Node In The Head(强制下线/断电)

参考资料:

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/high_availability_add-on_reference/s1-unfence-haar

双节点集群(TWO nodes Cluster)

辅助设备：ping node, quorum disk(仲裁设备)
Failover：故障切换，即某资源的主节点故障时，将资源转移至其它节点的操作
Failback：故障移回，即某资源的主节点故障后重新修改上线后，将之前已转移至其它节点的资源重新切回的过程

HA Cluster实现方案:
AIS：Applicaiton Interface Specification 应用程序接口规范
RHCS：Red Hat Cluster Suite红帽集群套件
参考资料：https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/5/html/cluster_suite_overview/ch.gfscs.cluster-overview-cso

高可用集群介绍入门以及实现技术插图

heartbeat：基于心跳监测实现服务高可用
pacemaker+corosync：资源管理与故障转移

vrrp：Virtual Router Redundancy Protocol
虚拟路由冗余协议,解决静态网关单点风险

-软件层—keepalived
-物理层—路由器、三层交换机

本文链接：http://www.yunweipai.com/35350.html





----------------------------------------------

VRRP  原理介绍

VRRP
VRRP 网络层硬件实现

VRRP 原理介绍插图

VRRP相关术语
-虚拟路由器：Virtual Router
-虚拟路由器标识：VRID(0-255)，唯一标识虚拟路由器
-VIP：Virtual IP
-VMAC：Virutal MAC (00-00-5e-00-01-VRID)

-物理路由器：
master：主设备
backup：备用设备
priority：优先级

VRRP相关技术
通告：心跳，优先级等；周期性
工作方式：抢占式，非抢占式

安全认证：
无认证
简单字符认证：预共享密钥
MD5

工作模式：
主/备：单虚拟路径器
主/主：主/备（虚拟路由器1），备/主（虚拟路由器2）

本文链接：http://www.yunweipai.com/35357.html





----------------------------------------------

Keepalived 经典入门教程

Keepalived 初步

Keepalived 经典入门教程插图

keepalived 介绍
vrrp协议的软件实现，原生设计目的为了高可用ipvs服务

官网：http://keepalived.org/

功能：
-基于vrrp协议完成地址流动
-为vip地址所在的节点生成ipvs规则(在配置文件中预先定义)
-为ipvs集群的各RS做健康状态检测
-基于脚本调用接口完成脚本中定义的功能，进而影响集群事务，以此支持nginx、haproxy等服务

Keepalived 架构
官方文档：

https://keepalived.org/doc/

http://keepalived.org/documentation.html

Keepalived 经典入门教程插图(1)

-用户空间核心组件：

vrrp stack：VIP消息通告
checkers：监测real server
system call：标记real server权重
SMTP：邮件组件
ipvs wrapper：生成IPVS规则
Netlink Reflector：网络接口
WatchDog：监控进程

-控制组件：配置文件解析器

-IO复用器

-内存管理组件


Keepalived进程树

'''
Keepalived  <-- Parent process monitoring children
\_ Keepalived   <-- VRRP child
\_ Keepalived   <-- Healthchecking child
'''


Keepalived 环境准备
各节点时间必须同步：ntp, chrony
关闭防火墙及SELinux
各节点之间可通过主机名互相通信：非必须
建议使用/etc/hosts文件实现：非必须
各节点之间的root用户可以基于密钥认证的ssh服务完成互相通信：非必须
Keepalived 相关文件
软件包名：keepalived
主程序文件：/usr/sbin/keepalived
主配置文件：/etc/keepalived/keepalived.conf
配置文件示例：/usr/share/doc/keepalived
Unit File：/lib/systemd/system/keepalived.service
Unit File的环境配置文件：
/etc/sysconfig/keepalived CentOS
/etc/default/keepalived Ubuntu

注意：CentOS 7 上有 bug，可能有下面情况出现
'''
systemctl restart keepalived    可能不会新配置生效
systemctl stop keepalived       无法停止进程，需要kill 停止
'''

本文链接：http://www.yunweipai.com/35361.html



----------------------------------------------

Keepalived  安装详解

Keepalived 安装
包安装
'''
#CentOS
[root@centos ~]#yum install keepalived 

#ubuntu
[root@ubuntu1804 ~]#apt -y install keepalived 
'''


CentOS 8 安装 keepalived
'''
[root@centos8 ~]#dnf -y install keepalived
[root@centos8 ~]#dnf info keepalived
Last metadata expiration check: 0:00:24 ago on Thu 26 Mar 2020 07:28:36 PM CST.
Installed Packages
Name         : keepalived
Version      : 2.0.10
Release      : 4.el8_0.2
Architecture : x86_64
Size         : 1.4 M
Source       : keepalived-2.0.10-4.el8_0.2.src.rpm
Repository   : @System
From repo    : AppStream
Summary      : High Availability monitor built upon LVS, VRRP and service pollers
URL          : http://www.keepalived.org/
License      : GPLv2+
Description  : Keepalived provides simple and robust facilities for load balancing
             : and high availability to Linux system and Linux based infrastructures.
             : The load balancing framework relies on well-known and widely used
             : Linux Virtual Server (IPVS) kernel module providing Layer4 load
             : balancing. Keepalived implements a set of checkers to dynamically and
             : adaptively maintain and manage load-balanced server pool according
             : their health. High availability is achieved by VRRP protocol. VRRP is
             : a fundamental brick for router failover. In addition, keepalived
             : implements a set of hooks to the VRRP finite state machine providing
             : low-level and high-speed protocol interactions. Keepalived frameworks
             : can be used independently or all together to provide resilient
             : infrastructures.

[root@centos8 ~]#systemctl start keepalived.service 
[root@centos8 ~]#ps auxf |grep keepalived
root      12864  0.0  0.1  12108  1100 pts/0    S+   19:25   0:00          |   \_ grep --color=auto keepalive
root      12835  0.0  0.3  91444  2484 ?        Ss   19:24   0:00 /usr/sbin/keepalived -D
root      12836  0.0  0.5  91576  4212 ?        S    19:24   0:00  \_ /usr/sbin/keepalived -D
root      12837  0.0  0.5  91444  4620 ?        S    19:24   0:00  \_ /usr/sbin/keepalived -D

[root@centos8 ~]#pstree -p
......
           ├─keepalived(12835)─┬─keepalived(12836)
           │                   └─keepalived(12837)
......
'''

Ubuntu 安装 keepalived
'''
[root@ubuntu1804 ~]#apt install keepalived -y
[root@ubuntu1804 ~]#dpkg -s keepalived
Package: keepalived
Status: install ok installed
Priority: extra
Section: admin
Installed-Size: 824
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Architecture: amd64
Version: 1:1.3.9-1ubuntu0.18.04.2
Depends: iproute2, libc6 (>= 2.27), libglib2.0-0 (>= 2.26.0), libip4tc0 (>= 1.6.0+snapshot20161117), libip6tc0 (>= 1.6.0+snapshot20161117), libnl-3-200 (>= 3.2.27), libnl-genl-3-200 (>= 3.2.7), libnl-route-3-200 (>= 3.2.7), libsnmp30 (>= 5.7.3+dfsg-1.8ubuntu3.1~dfsg), libssl1.1 (>= 1.1.0), libxtables12 (>= 1.6.0+snapshot20161117)
Recommends: ipvsadm
Conffiles:
 /etc/dbus-1/system.d/org.keepalived.Vrrp1.conf 6b020ff46c6425d3a9cfa179814d7253
 /etc/default/keepalived 6b2e3432e4ae31b444058ba2b0d1f06a
 /etc/init.d/keepalived 0312972e0718331b4c90b3b98e623624
Description: Failover and monitoring daemon for LVS clusters
 keepalived is used for monitoring real servers within a Linux
 Virtual Server (LVS) cluster.  keepalived can be configured to
 remove real servers from the cluster pool if it stops responding,
 as well as send a notification email to make the admin aware of
 the service failure.
 .
 In addition, keepalived implements an independent Virtual Router
 Redundancy Protocol (VRRPv2; see rfc2338 for additional info)
 framework for director failover.
 .
 You need a kernel >= 2.4.28 or >= 2.6.11 for keepalived.
 See README.Debian for more information.
Homepage: http://keepalived.org
Original-Maintainer: Alexander Wirt <formorer@debian.org>

[root@ubuntu1804 ~]#dpkg -L keepalived
/.
/etc
/etc/dbus-1
/etc/dbus-1/system.d
/etc/dbus-1/system.d/org.keepalived.Vrrp1.conf
/etc/default
/etc/default/keepalived
/etc/init.d
/etc/init.d/keepalived
/etc/keepalived
/lib
/lib/systemd
/lib/systemd/system
/lib/systemd/system/keepalived.service
/usr
/usr/bin
/usr/bin/genhash
/usr/sbin
/usr/sbin/keepalived
/usr/share
/usr/share/dbus-1
/usr/share/dbus-1/interfaces
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Instance.xml
/usr/share/dbus-1/interfaces/org.keepalived.Vrrp1.Vrrp.xml
/usr/share/doc
/usr/share/doc/keepalived
/usr/share/doc/keepalived/AUTHOR
/usr/share/doc/keepalived/CONTRIBUTORS
/usr/share/doc/keepalived/README
/usr/share/doc/keepalived/TODO
/usr/share/doc/keepalived/changelog.Debian.gz
/usr/share/doc/keepalived/copyright
/usr/share/doc/keepalived/keepalived.conf.SYNOPSIS.gz
/usr/share/doc/keepalived/samples
/usr/share/doc/keepalived/samples/client.pem
/usr/share/doc/keepalived/samples/dh1024.pem
/usr/share/doc/keepalived/samples/keepalived.conf.HTTP_GET.port
/usr/share/doc/keepalived/samples/keepalived.conf.IPv6
/usr/share/doc/keepalived/samples/keepalived.conf.SMTP_CHECK
/usr/share/doc/keepalived/samples/keepalived.conf.SSL_GET
/usr/share/doc/keepalived/samples/keepalived.conf.fwmark
/usr/share/doc/keepalived/samples/keepalived.conf.inhibit
/usr/share/doc/keepalived/samples/keepalived.conf.misc_check
/usr/share/doc/keepalived/samples/keepalived.conf.misc_check_arg
/usr/share/doc/keepalived/samples/keepalived.conf.quorum
/usr/share/doc/keepalived/samples/keepalived.conf.sample
/usr/share/doc/keepalived/samples/keepalived.conf.status_code
/usr/share/doc/keepalived/samples/keepalived.conf.track_interface
/usr/share/doc/keepalived/samples/keepalived.conf.virtual_server_group
/usr/share/doc/keepalived/samples/keepalived.conf.virtualhost
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.localcheck
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.lvs_syncd
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.routes
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.rules
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.scripts
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.static_ipaddress
/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.sync
/usr/share/doc/keepalived/samples/root.pem
/usr/share/doc/keepalived/samples/sample.misccheck.smbcheck.sh
/usr/share/doc/keepalived/samples/sample_notify_fifo.sh
/usr/share/man
/usr/share/man/man1
/usr/share/man/man1/genhash.1.gz
/usr/share/man/man5
/usr/share/man/man5/keepalived.conf.5.gz
/usr/share/man/man8
/usr/share/man/man8/keepalived.8.gz
/usr/share/snmp
/usr/share/snmp/mibs
/usr/share/snmp/mibs/KEEPALIVED-MIB.txt
/usr/share/snmp/mibs/VRRP-MIB.txt
/usr/share/snmp/mibs/VRRPv3-MIB.txt
[root@ubuntu1804 ~]#cp /usr/share/doc/keepalived/samples/keepalived.conf.sample /etc/keepalived/keepalived.conf
[root@ubuntu1804 ~]#systemctl start keepalived.service
[root@ubuntu1804 ~]#systemctl status keepalived.service 
● keepalived.service - Keepalive Daemon (LVS and VRRP)
   Loaded: loaded (/lib/systemd/system/keepalived.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-03-26 19:33:48 CST; 1min 9s ago
  Process: 3208 ExecStart=/usr/sbin/keepalived $DAEMON_ARGS (code=exited, status=0/SUCCESS)
 Main PID: 3209 (keepalived)
    Tasks: 3 (limit: 1084)
   CGroup: /system.slice/keepalived.service
           ├─3209 /usr/sbin/keepalived
           ├─3210 /usr/sbin/keepalived
           └─3211 /usr/sbin/keepalived

Mar 26 19:34:04 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Timeout connecting server [192.168.200.2]:tcp:1358.
Mar 26 19:34:10 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Timeout connecting server [192.168.200.2]:tcp:1358.
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Timeout connecting server [192.168.200.2]:tcp:1358.
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Check on service [192.168.200.2]:tcp:1358 failed after 3 retry.
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Removing service [192.168.200.2]:tcp:1358 to VS [10.10.10.2]:tc
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Lost quorum 1-0=1 > 0 for VS [10.10.10.2]:tcp:1358
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Adding sorry server [192.168.200.200]:tcp:1358 to VS [10.10.10.
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Removing alive servers from the pool for VS [10.10.10.2]:tcp:13
Mar 26 19:34:16 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Remote SMTP server [192.168.200.1]:25 connected.
Mar 26 19:34:37 ubuntu1804.magedu.org Keepalived_healthcheckers[3210]: Error reading data from remote SMTP server [192.168.200.1]:25.
[root@ubuntu1804 ~]#ps auxf |grep keepalived
root       3224  0.0  0.1  14428  1040 pts/0    S+   19:34   0:00      |   \_ grep --color=auto keepalived
root       3209  0.0  0.3  91812  2996 ?        Ss   19:33   0:00 /usr/sbin/keepalived
root       3210  0.0  0.5  96100  5276 ?        S    19:33   0:00  \_ /usr/sbin/keepalived
root       3211  0.0  0.5  96152  5420 ?        S    19:33   0:00  \_ /usr/sbin/keepalived
'''

编译安装
'''
[root@centos7 ~]#yum install  gcc curl openssl-devel libnl3-devel net-snmp-devel
[root@centos7 ~]#wget https://keepalived.org/software/keepalived-2.0.20.tar.gz
[root@centos7 ~]#tar xvf keepalived-2.0.20.tar.gz  -C /usr/local/src
[root@centos7 ~]#cd /usr/local/src/keepalived-2.0.20/
[root@centos7 keepalived-2.0.20]#./configure --prefix=/usr/local/keepalived 
[root@centos7 keepalived-2.0.20]#make && make install
[root@centos7 keepalived-2.0.20]#cd
[root@centos7 ~]#/usr/local/keepalived/sbin/keepalived -v
Keepalived v2.0.20 (01/22,2020)

Copyright(C) 2001-2020 Alexandre Cassen, <acassen@gmail.com>

Built with kernel headers for Linux 3.10.0
Running on Linux 3.10.0-1062.el7.x86_64 #1 SMP Wed Aug 7 18:08:02 UTC 2019

configure options: --prefix=/usr/local/keepalived

Config options:  LVS VRRP VRRP_AUTH OLD_CHKSUM_COMPAT FIB_ROUTING

System options:  PIPE2 SIGNALFD INOTIFY_INIT1 VSYSLOG EPOLL_CREATE1 IPV6_ADVANCED_API LIBNL3 RTA_ENCAP RTA_EXPIRES RTA_PREF FRA_SUPPRESS_PREFIXLEN FRA_TUN_ID RTAX_CC_ALGO RTAX_QUICKACK FRA_OIFNAME IFA_FLAGS IP_MULTICAST_ALL NET_LINUX_IF_H_COLLISION LIBIPTC_LINUX_NET_IF_H_COLLISION LIBIPVS_NETLINK VRRP_VMAC IFLA_LINK_NETNSID CN_PROC SOCK_NONBLOCK SOCK_CLOEXEC O_PATH GLOB_BRACE INET6_ADDR_GEN_MODE SO_MARK SCHED_RESET_ON_FORK

#自动生成unit文件
[root@centos7 ~]#cat /usr/lib/systemd/system/keepalived.service
[Unit]
Description=LVS and VRRP High Availability Monitor
After=network-online.target syslog.target 
Wants=network-online.target 

[Service]
Type=forking
PIDFile=/run/keepalived.pid
KillMode=process
EnvironmentFile=-/usr/local/keepalived/etc/sysconfig/keepalived
ExecStart=/usr/local/keepalived/sbin/keepalived $KEEPALIVED_OPTIONS
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
[root@centos7 ~]#cat /usr/local/keepalived/etc/sysconfig/keepalived
# Options for keepalived. See `keepalived --help' output and keepalived(8) and
# keepalived.conf(5) man pages for a list of all options. Here are the most
# common ones :
#
# --vrrp               -P    Only run with VRRP subsystem.
# --check              -C    Only run with Health-checker subsystem.
# --dont-release-vrrp  -V    Dont remove VRRP VIPs & VROUTEs on daemon stop.
# --dont-release-ipvs  -I    Dont remove IPVS topology on daemon stop.
# --dump-conf          -d    Dump the configuration data.
# --log-detail         -D    Detailed log messages.
# --log-facility       -S    0-7 Set local syslog facility (default=LOG_DAEMON)
#

KEEPALIVED_OPTIONS="-D"

#默认无法启动
[root@centos7 ~]#systemctl start keepalived.service 
Job for keepalived.service failed because the control process exited with error code. See "systemctl status keepalived.service" and "journalctl -xe" for details.

#查看日志，可以看到是因为缺少配置文件导致无法启动
[root@centos7 ~]#journalctl -xe
-- Subject: Unit keepalived.service has begun start-up
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit keepalived.service has begun starting up.
Mar 29 00:38:17 centos7.magedu.org Keepalived[1123]: Starting Keepalived v2.0.20 (01/22,2020)
Mar 29 00:38:17 centos7.magedu.org Keepalived[1123]: Running on Linux 3.10.0-1062.el7.x86_64 #1 SMP Wed Aug 7 
Mar 29 00:38:17 centos7.magedu.org Keepalived[1123]: Command line: '/usr/local/keepalived/sbin/keepalived' '-D
Mar 29 00:38:17 centos7.magedu.org Keepalived[1123]: Unable to find configuration file /etc/keepalived/keepali
Mar 29 00:38:17 centos7.magedu.org Keepalived[1123]: Stopped Keepalived v2.0.20 (01/22,2020)
Mar 29 00:38:17 centos7.magedu.org systemd[1]: keepalived.service: control process exited, code=exited status=
Mar 29 00:38:17 centos7.magedu.org systemd[1]: Failed to start LVS and VRRP High Availability Monitor.
-- Subject: Unit keepalived.service has failed
-- Defined-By: systemd
-- Support: http://lists.freedesktop.org/mailman/listinfo/systemd-devel
-- 
-- Unit keepalived.service has failed.
-- 
-- The result is failed.
Mar 29 00:38:17 centos7.magedu.org systemd[1]: Unit keepalived.service entered failed state.
Mar 29 00:38:17 centos7.magedu.org systemd[1]: keepalived.service failed.
Mar 29 00:38:17 centos7.magedu.org polkitd[565]: Unregistered Authentication Agent for unix-process:1117:11546

#创建配置文件
[root@centos7 ~]#mkdir /etc/keepalived
[root@centos7 ~]#cp /usr/local/keepalived/etc/keepalived/keepalived.conf  /etc/keepalived

#再次启动成功
[root@centos7 ~]#systemctl enable --now  keepalived.service 
Created symlink from /etc/systemd/system/multi-user.target.wants/keepalived.service to /usr/lib/systemd/system/keepalived.service.

[root@centos7 ~]#systemctl status keepalived.service 
● keepalived.service - LVS and VRRP High Availability Monitor
   Loaded: loaded (/usr/lib/systemd/system/keepalived.service; disabled; vendor preset: disabled)
   Active: active (running) since Sun 2020-03-29 00:44:33 CST; 4s ago
  Process: 1191 ExecStart=/usr/local/keepalived/sbin/keepalived $KEEPALIVED_OPTIONS (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/keepalived.service
           ├─1192 /usr/local/keepalived/sbin/keepalived -D
           ├─1193 /usr/local/keepalived/sbin/keepalived -D
           └─1194 /usr/local/keepalived/sbin/keepalived -D

Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.18
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.16
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.17
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.18
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.16
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.17
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.18
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.16
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.17
Mar 29 00:44:37 centos7.magedu.org Keepalived_vrrp[1194]: Sending gratuitous ARP on eth0 for 192.168.200.18
[root@centos7 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:32:80:38 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.7/24 brd 10.0.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.16/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.17/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.18/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe32:8038/64 scope link 
       valid_lft forever preferred_lft forever

[root@centos7 ~]#hostname -I
10.0.0.7 192.168.200.16 192.168.200.17 192.168.200.18 
[root@centos7 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
ping: sendmsg: Operation not permitted
ping: sendmsg: Operation not permitted
^C
--- 192.168.200.16 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1000ms

[root@centos7 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 860 packets, 46129 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.18      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.17      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.16      

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 1737 packets, 1188K bytes)
 pkts bytes target     prot opt in     out     source               destination         
    4   336 DROP       all  --  *      *       192.168.200.18       0.0.0.0/0           
    0     0 DROP       all  --  *      *       192.168.200.17       0.0.0.0/0           
    0     0 DROP       all  --  *      *       192.168.200.16       0.0.0.0/0  

[root@centos7 ~]#vim /etc/keepalived/keepalived.conf
#注释下面一行
#vrrp_strict

#重启动不生效，有bug
[root@centos7 ~]#systemctl restart keepalived.service 
[root@centos7 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
ping: sendmsg: Operation not permitted
ping: sendmsg: Operation not permitted
^C
--- 192.168.200.16 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 999ms

[root@centos7 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 1219 packets, 67647 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.18      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.17      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.16      

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 2282 packets, 1233K bytes)
 pkts bytes target     prot opt in     out     source               destination         
    4   336 DROP       all  --  *      *       192.168.200.18       0.0.0.0/0           
    0     0 DROP       all  --  *      *       192.168.200.17       0.0.0.0/0           
    4   336 DROP       all  --  *      *       192.168.200.16       0.0.0.0/0    

#无法关闭进程
[root@centos7 ~]#systemctl stop keepalived.service 
[root@centos7 ~]#ps aux|grep keepalived
root       1383  0.0  0.1  69672  1020 ?        Ss   00:57   0:00 /usr/local/keepalived/sbin/keepalived -D
root       1384  0.0  0.2  69804  2308 ?        S    00:57   0:00 /usr/local/keepalived/sbin/keepalived -D
root       1385  0.0  0.1  69672  1308 ?        S    00:57   0:00 /usr/local/keepalived/sbin/keepalived -D
root       1392  0.0  0.0 112712   964 pts/0    R+   00:59   0:00 grep --color=auto keepalived

[root@centos7 ~]#killall  keepalived
[root@centos7 ~]#systemctl start keepalived.service 
[root@centos7 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
64 bytes from 192.168.200.16: icmp_seq=1 ttl=64 time=0.093 ms
^C
--- 192.168.200.16 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.093/0.093/0.093/0.000 ms
[root@centos7 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 125 packets, 8493 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 135 packets, 20190 bytes)
 pkts bytes target     prot opt in     out     source               destination 
'''

KeepAlived 配置说明

配置文件组成部分
'''
/etc/keepalived/keepalived.conf
'''
配置组成
'''
-GLOBAL CONFIGURATION
    Global definitions：定义邮件配置，route_id，vrrp配置，多播地址等

-VRRP CONFIGURATION 
    VRRP instance(s)：定义每个vrrp虚拟路由器

-LVS CONFIGURATION
    Virtual server group(s)
    Virtual server(s)：LVS集群的VS和RS
'''

配置语法说明

全局配置
''''
#/etc/keepalived/keepalived.conf 
global_defs {
  notification_email {
  root@localhost #keepalived 发生故障切换时邮件发送的目标邮箱，可以按行区分写多个
  root@wangxiaochun.com 
  29308620@qq.com 
  }
  notification_email_from keepalived@localhost  #发邮件的地址
  smtp_server 127.0.0.1     #邮件服务器地址
  smtp_connect_timeout 30   #邮件服务器连接timeout
  router_id ha1.example.com #每个keepalived主机唯一标识，建议使用当前主机名，但多节点重名不影响
  vrrp_skip_check_adv_addr  #对所有通告报文都检查，会比较消耗性能，启用此配置后，如果收到的通告报文和上一个报文是同一个路由器，则跳过检查，默认值为全检查
  vrrp_strict #严格遵守VRRP协议,禁止以下状况:1.无VIP地址 2.配置了单播邻居 3.在VRRP版本2中有IPv6地址，开启动此项会自动开启iptables防火墙规则，建议关闭此项配置,
  vrrp_garp_interval 0 #gratuitous ARP messages报文发送延迟，0表示不延迟
  vrrp_gna_interval 0  #unsolicited NA messages （不请自来）消息发送延迟
  vrrp_mcast_group4 224.0.0.18 #指定组播IP地址，默认值：224.0.0.18 范围：224.0.0.0到239.255.255.255
  vrrp_iptables        #开启此项，当vrrp_strict开启时，不添加防火墙规则，否则VIP无法访问
}
'''


配置虚拟路由器
'''
vrrp_instance <STRING> {
    配置参数
    ......
 }

#配置参数： 
state MASTER|BACKUP#当前节点在此虚拟路由器上的初始状态，状态为MASTER或者BACKUP
interface IFACE_NAME #绑定为当前虚拟路由器使用的物理接口，如：ens32,eth0,bond0,br0
virtual_router_id VRID #每个虚拟路由器惟一标识，范围：0-255，每个虚拟路由器此值必须唯一，否则服务无法启动，同属一个虚拟路由器的多个keepalived节点必须相同
priority 100    #当前物理节点在此虚拟路由器的优先级，范围：1-254，每个keepalived主机节点此值不同
advert_int 1    #vrrp通告的时间间隔，默认1s
authentication { #认证机制
auth_type AH|PASS
auth_pass <PASSWORD> #预共享密钥，仅前8位有效，同一个虚拟路由器的多个keepalived节点必须一样
}
virtual_ipaddress { #虚拟IP
    <IPADDR>/<MASK> brd <IPADDR> dev <STRING> scope <SCOPE> label <LABEL>
    192.168.200.100         #指定VIP，不指定网卡，默认为eth0,注意：不指定/prefix,默认为/32
    192.168.200.101/24 dev eth1                 #指定VIP的网卡
    192.168.200.102/24 dev eth2 label eth2:1    #指定VIP的网卡label 
}
track_interface { #配置监控网络接口，一旦出现故障，则转为FAULT状态实现地址转移
    eth0
    eth1
    …
} 
'''


范例：
'''
[root@centos7 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id LVS_DEVEL
   vrrp_skip_check_adv_addr
   vrrp_strict                  #开启限制，会自动生效防火墙设置，导致无访问VIP
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 80 #修改此行
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.200.16
        192.168.200.17
        192.168.200.18
    }
}
[root@centos7 ~]#systemctl start keepalived.service 
[root@centos7 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:33:b4:1a brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.17/24 brd 10.0.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.16/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.17/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.18/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe33:b41a/64 scope link 
       valid_lft forever preferred_lft forever

[root@centos7 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 59 packets, 3372 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.16      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.17      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.18      

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 33 packets, 6940 bytes)
 pkts bytes target     prot opt in     out     source               destination  

[root@centos7 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
^C
--- 192.168.200.16 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5002ms

[root@centos7 ~]#

# 如果是CentOS 8 ，会显示以下warning 
[root@centos8 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
# Warning: iptables-legacy tables present, use iptables-legacy to see them

#无法访问VIP
[root@centos8 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
^C
--- 192.168.200.16 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 143ms
'''


实现独立子配置文件

当生产环境复杂时，
'''
/etc/keepalived/keepalived.conf
'''

文件中内容过多，不易管理，可以将不同集群的配置，比如：不同集群的VIP配置放在独立的子配置文件中
'''
[root@ka1-centos8 ~]#mkdir /etc/keepalived/conf.d/
[root@ka1-centos8 ~]#tail -n1 /etc/keepalived/keepalived.conf
include /etc/keepalived/conf.d/*.conf
[root@ka1-centos8 ~]#vim /etc/keepalived/conf.d/cluster1.conf
'''


本文链接：http://www.yunweipai.com/35366.html



----------------------------------------------

Keepalived - 配置虚拟路由器

配置虚拟路由器
'''
vrrp_instance <STRING> {
    配置参数
    ......
 }

#配置参数： 
state MASTER|BACKUP#当前节点在此虚拟路由器上的初始状态，状态为MASTER或者BACKUP
interface IFACE_NAME #绑定为当前虚拟路由器使用的物理接口，如：ens32,eth0,bond0,br0
virtual_router_id VRID #每个虚拟路由器惟一标识，范围：0-255，每个虚拟路由器此值必须唯一，否则服务无法启动，同属一个虚拟路由器的多个keepalived节点必须相同
priority 100    #当前物理节点在此虚拟路由器的优先级，范围：1-254，每个keepalived主机节点此值不同
advert_int 1    #vrrp通告的时间间隔，默认1s
authentication { #认证机制
auth_type AH|PASS
auth_pass <PASSWORD> #预共享密钥，仅前8位有效，同一个虚拟路由器的多个keepalived节点必须一样
}
virtual_ipaddress { #虚拟IP
    <IPADDR>/<MASK> brd <IPADDR> dev <STRING> scope <SCOPE> label <LABEL>
    192.168.200.100         #指定VIP，不指定网卡，默认为eth0,注意：不指定/prefix,默认为/32
    192.168.200.101/24 dev eth1                 #指定VIP的网卡
    192.168.200.102/24 dev eth2 label eth2:1    #指定VIP的网卡label 
}
track_interface { #配置监控网络接口，一旦出现故障，则转为FAULT状态实现地址转移
    eth0
    eth1
    …
} 
'''


范例：

'''
[root@centos7 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id LVS_DEVEL
   vrrp_skip_check_adv_addr
   vrrp_strict                  #开启限制，会自动生效防火墙设置，导致无访问VIP
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 80 #修改此行
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.200.16
        192.168.200.17
        192.168.200.18
    }
}
[root@centos7 ~]#systemctl start keepalived.service 
[root@centos7 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:33:b4:1a brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.17/24 brd 10.0.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.16/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.17/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.200.18/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe33:b41a/64 scope link 
       valid_lft forever preferred_lft forever

[root@centos7 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 59 packets, 3372 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.16      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.17      
    0     0 DROP       all  --  *      *       0.0.0.0/0            192.168.200.18      

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 33 packets, 6940 bytes)
 pkts bytes target     prot opt in     out     source               destination  

[root@centos7 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
^C
--- 192.168.200.16 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5002ms

[root@centos7 ~]#

# 如果是CentOS 8 ，会显示以下warning 
[root@centos8 ~]#iptables -vnL
Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
# Warning: iptables-legacy tables present, use iptables-legacy to see them

#无法访问VIP
[root@centos8 ~]#ping 192.168.200.16
PING 192.168.200.16 (192.168.200.16) 56(84) bytes of data.
^C
--- 192.168.200.16 ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 143ms
'''


本文链接：http://www.yunweipai.com/35369.html

----------------------------------------------

Keepalived  实现 master/slave 的单主架构

实现master/slave的Keepalived 单主架构

MASTER配置
'''
[root@ka1-centos8 ~]#vim /etc/keepalived/keepalived.conf 
global_defs {
  notification_email {
  root@localhost #keepalived 发生故障切换时邮件发送的对象，可以按行区分写多个
  }
  notification_email_from keepalived@localhost
  smtp_server 127.0.0.1
  smtp_connect_timeout 30
  router_id ka1.example.com
  vrrp_skip_check_adv_addr #所有报文都检查比较消耗性能，此配置为如果收到的报文和上一个报文是同一个路由器则跳过检查报文中的源地址
  #vrrp_strict #严格遵守VRRP协议,禁止状况:1.无VIP地址,2.配置了单播邻居,3.在VRRP版本2中有IPv6地址
  vrrp_garp_interval 0 #ARP报文发送延迟
  vrrp_gna_interval 0 #消息发送延迟
  vrrp_mcast_group4 224.0.0.18 #默认组播IP地址，224.0.0.0到239.255.255.255
 }
vrrp_instance VI_1 {
  state MASTER           #在另一个结点上为BACKUP
  interface eth0
  virtual_router_id 66   #每个虚拟路由器必须唯一，同属一个虚拟路由器的多个keepalived节点必须相同
  priority 100           #在另一个结点上为80
  advert_int 1
  authentication {
    auth_type PASS       #预共享密钥认证，同一个虚拟路由器的keepalived节点必须一样
    auth_pass 12345678
  }
  virtual_ipaddress {
    10.0.0.10 dev eth0 label eth0:0
  }
}
'''


BACKUP配置
'''
#配置文件和master基本一致，只需修改三行
[root@ka2-centos8 ~]#vim /etc/keepalived/keepalived.conf 
global_defs {
  notification_email {
  root@localhost
  }
  notification_email_from keepalived@localhost
  smtp_server 127.0.0.1
  smtp_connect_timeout 30
  router_id ka2.example.com         #修改此行
  vrrp_skip_check_adv_addr 
  #vrrp_strict          
  vrrp_garp_interval 0 
  vrrp_gna_interval 0
  vrrp_mcast_group4 224.0.0.18
}
vrrp_instance VI_1 {
  state BACKUP               #修改此行
  interface eth0
  virtual_router_id 66       
  priority 80               #修改此行
  advert_int 1
  authentication {
    auth_type PASS
    auth_pass 12345678
  }
  virtual_ipaddress {
    10.0.0.10 dev eth0 label eth0:0
  }
}
'''


 
抓包观察
'''
tcpdump -i eth0 -nn host 224.0.0.18
'''


抢占模式和非抢占模式
非抢占模式
默认为抢占模式，即当高优先级的主机恢复在线后，会抢占低先级的主机的master角色，造成网络抖动，建议设置为非抢占模式 nopreempt ，即高优级主机恢复后，并不会抢占低优先级主机的master角色

注意：要关闭 VIP抢占，必须将各 keepalived 服务器state配置为BACKUP

'''
#ha1主机配置
vrrp_instance VI_1 {
  state BACKUP     #都为BACKUP
  interface eth0
  virtual_router_id 66
  priority 100    #优先级高
  advert_int 1
  nopreempt         #添加此行，都为nopreempt

#ha2主机配置
vrrp_instance VI_1 {
  state BACKUP         #都为BACKUP
  interface eth0
  virtual_router_id 66
  priority 80       #优先级低
  advert_int 1
  nopreempt     #添加此行，都为nopreempt
'''


抢占延迟模式

抢占延迟模式，即优先级高的主机恢复后，不会立即抢回VIP，而是延迟一段时间（默认300s）再抢回 VIP

preempt_delay #s 指定抢占延迟时间为#s，默认延迟300s

注意：需要各keepalived服务器state为BACKUP

范例：
'''
#ha1主机配置
vrrp_instance VI_1 {
  state BACKUP     #都为BACKUP
  interface eth0
  virtual_router_id 66
  priority 100
  advert_int 1
  preempt_delay 60s #抢占延迟模式，默认延迟300s

#ha2主机配置
vrrp_instance VI_1 {
  state BACKUP              #都为BACKUP
  interface eth0
  virtual_router_id 66
  priority 80
  advert_int 1
'''


VIP单播配置
默认keepalived主机之间利用多播相互通告消息，会造成网络拥塞，可以替换成单播，减少网络流量

注意：启用单播，不能启用 vrrp_strict
'''
#分别在各个keepalived 节点设置对方主机的IP，建议设置为专用于对应心跳线网络的地址，而非使用业务网络
unicast_src_ip <IPADDR>  #指定单播的源IP
unicast_peer {
    <IPADDR>     # #指定单播的对方目标主机IP
    ......
}
'''


范例：
'''
#master 主机配置
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id ka1.magedu.org
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.8
    unicast_peer{
        10.0.0.18
    }
}

[root@ha1-centos8 ~]#hostname -I
10.0.0.8 10.0.0.10 

#slave 主机配置
[root@ka2-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id ka2.magedu.org
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

vrrp_instance VI_1 {
    state SLAVE
    interface eth0
    virtual_router_id 66
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.18
    unicast_peer {
    10.0.0.8 
    }
}
[root@ka2-centos8 ~]#hostname -I
10.0.0.18 
'''


抓包
'''
root@centos6 ~]#tcpdump  -i eth0 -nn host 10.0.0.8 and host 10.0.0.18
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
23:37:48.069158 IP 10.0.0.8 > 10.0.0.18: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
23:37:49.070013 IP 10.0.0.8 > 10.0.0.18: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
23:37:50.071144 IP 10.0.0.8 > 10.0.0.18: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
'''

本文链接：http://www.yunweipai.com/35371.html



----------------------------------------------

实战案例：实现Keepalived 状态切换的通知脚本
'''
#在所有keepalived节点配置如下
[root@ka1-centos8 ~]#cat /etc/keepalived/notify.sh 
#!/bin/bash
#
contact='root@wangxiaochun.com'
notify() {
    mailsubject="$(hostname) to be $1, vip floating"
    mailbody="$(date +'%F %T'): vrrp transition, $(hostname) changed to be $1"
    echo "$mailbody" | mail -s "$mailsubject" $contact
}
case $1 in
master)
    notify master
    ;;
backup)
    notify backup
    ;;
fault)
    notify fault
    ;;
*)
    echo "Usage: $(basename $0) {master|backup|fault}"
    exit 1
    ;;
esac

[root@ka1-centos8 ~]#chmod a+x /etc/keepalived/notify.sh 

[root@ka1-centos8 ~]#vim /etc/keepalived/keepalived.conf
vrrp_instance VI_1 {
    ......
    virtual_ipaddress {
    10.0.0.10 dev eth0 label eth0:1
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}

#模拟master故障
[root@ka1-centos8 ~]#killall keepalived
'''


查看邮箱收到邮件如下：

实战案例: 实现Keepalived 状态切换的通知脚本插图

本文链接：http://www.yunweipai.com/35373.html



----------------------------------------------

实战案例： 实现 master / master 的keepalived双主架构

实现master/master的Keepalivde 双主架构
master/slave的单主架构，同一时间只有一个Keepalived对外提供服务，此主机繁忙，而另一台主机却很空闲，利用率低下，可以使用master/master的双主架构，解决此问题。

master/master的双主架构：

即将两个或以上VIP分别运行在不同的keepalived服务器，以实现服务器并行提供web访问的目的，提高服务器资源利用率
'''
#ha1主机配置
[root@ka1-centos8 ~]#vim /etc/keepalived/keepalived.conf        
! Configuration File for keepalived
global_defs {
    notification_email {
        root@wangxiaochun.com
    }
    notification_email_from keepalived@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org
    vrrp_mcast_group4 224.0.100.100
}

vrrp_instance VI_1 {
    state MASTER            #在另一个主机上为BACKUP
    interface eth0
    virtual_router_id 66    #每个vrrp_instance唯一
    priority 100            #在另一个主机上为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 12345678
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1 #指定vrrp_instance各自的VIP
    }
}
vrrp_instance VI_2 {            #添加 VI_2 实例
    state BACKUP                #在另一个主机上为MASTER
    interface eth0
    virtual_router_id 88        #每个vrrp_instance唯一
    priority 80                 #在另一个主机上为100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 12345678
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:1  #指定vrrp_instance各自的VIP
    }
}

#ka2主机配置,和ka1配置只需五行不同
[root@ka2-centos8 ~]#vim /etc/keepalived/keepalived.conf        
! Configuration File for keepalived
global_defs {
    notification_email {
        root@wangxiaochun.com
    }
    notification_email_from keepalived@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka2.magedu.org        #修改此行
    vrrp_mcast_group4 224.0.100.100
}

vrrp_instance VI_1 {
    state BACKUP            #此修改行为BACKUP
    interface eth0
    virtual_router_id 66    
    priority 80             #此修改行为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 12345678
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
}
vrrp_instance VI_2 {
    state MASTER            #修改此行为MASTER
    interface eth0
    virtual_router_id 88        
    priority 100                #修改此行为100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 12345678
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:1  
    }
}
'''

实战案例：利用子配置文件实现master/master的Keepalived双主架构

'''
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id ha1.magedu.org
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0

}

include /etc/keepalived/conf.d/*.conf

[root@ka1-centos8 ~]#mkdir /etc/keepalived/conf.d/
[root@ka1-centos8 ~]#cat /etc/keepalived/conf.d/cluster1.conf 
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.8
    unicast_peer{
        10.0.0.18
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}

[root@ka1-centos8 ~]#cat /etc/keepalived/conf.d/cluster2.conf 
vrrp_instance VI_2 {
    state BACKUP
    interface eth0
    virtual_router_id 88
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.8
    unicast_peer{
        10.0.0.18
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}

[root@ka1-centos8 ~]#tree /etc/keepalived/
/etc/keepalived/
├── conf.d
│   ├── cluster1.conf
│   └── cluster2.conf
├── keepalived.conf
├── keepalived.conf.bak
└── notify.sh

1 directory, 5 files
[root@ka1-centos8 ~]#

#ka2主机的配置
[root@ka2-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived

global_defs {
   notification_email {
     acassen@firewall.loc
     failover@firewall.loc
     sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   smtp_server 192.168.200.1
   smtp_connect_timeout 30
   router_id ha2.magedu.org
   vrrp_skip_check_adv_addr
   #vrrp_strict
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

include /etc/keepalived/conf.d/*.conf

[root@ka2-centos8 ~]#cat /etc/keepalived/conf.d/cluster1.conf 
vrrp_instance VI_1 {
    state BACKUP 
    interface eth0
    virtual_router_id 66
    priority 80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.18
    unicast_peer {
    10.0.0.8 
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}
[root@ka2-centos8 ~]#cat /etc/keepalived/conf.d/cluster2.conf 
vrrp_instance VI_2 {
    state MASTER
    interface eth0
    virtual_router_id 88
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:1
    }
    unicast_src_ip 10.0.0.18
    unicast_peer{
        10.0.0.8
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}

[root@ka2-centos8 ~]#

#查看IP
[root@ka1-centos8 ~]#hostname -I
10.0.0.8 10.0.0.10 
[root@ka2-centos8 ~]#hostname -I
10.0.0.18 10.0.0.20

#ka1主机故障，测试VIP漂移至ka2主机
[root@ka1-centos8 ~]#killall keepalived
[root@ka1-centos8 ~]#hostname -I
10.0.0.8 

[root@ka2-centos8 ~]#hostname -I
10.0.0.18 10.0.0.20 10.0.0.10 

#恢复ka1主机
[root@ka1-centos8 ~]#systemctl start keepalived.service 
[root@ka1-centos8 ~]#hostname -I
10.0.0.8 10.0.0.10 
[root@ka2-centos8 ~]#hostname -I
10.0.0.18 10.0.0.20 
'''


实战案例：三个节点的多主架构实现
'''
第一个节点ka1配置：
Vrrp instance 1：MASTER，优先级100
Vrrp instance 2：BACKUP，优先级80
Vrrp instance 3：BACKUP，优先级60

第二个节点ka2配置：
Vrrp instance 1：BACKUP，优先级60
Vrrp instance 2：MASTER，优先级100
Vrrp instance 3：BACKUP，优先级80

第三个节点ka3配置：
Vrrp instance 1：BACKUP，优先级80
Vrrp instance 2：BACKUP，优先级60
Vrrp instance 3：MASTER，优先级100
'''


本文链接：http://www.yunweipai.com/35376.html



----------------------------------------------

实战案例： 实现 IPVS 的高可用性

实现IPVS的高可用性

IPVS相关配置
虚拟服务器配置结构
'''
 virtual_server IP port  {
 ...
 real_server {
 ...
 }
  …
}
'''


virtual server （虚拟服务器）的定义格式
'''
virtual_server IP port      #定义虚拟主机IP地址及其端口
virtual_server fwmark int   #ipvs的防火墙打标，实现基于防火墙的负载均衡集群
virtual_server group string #使用虚拟服务器组
'''


虚拟服务器组
将多个虚拟服务器定义成一个组，统一对外服务，如：http和https定义成一个虚拟服务器组
'''
virtual_server_group <STRING> {
           # Virtual IP Address and Port
           <IPADDR> <PORT>
           <IPADDR> <PORT>
           ...
           # <IPADDR RANGE> has the form
           # XXX.YYY.ZZZ.WWW-VVV eg 192.168.200.1-10
           # range includes both .1 and .10 address
           <IPADDR RANGE> <PORT># VIP range VPORT
           <IPADDR RANGE> <PORT>
           ...
           # Firewall Mark (fwmark)
           fwmark <INTEGER>
           fwmark <INTEGER>
           ...
}
'''


虚拟服务器配置
'''
virtual_server IP port  {               #VIP和PORT
delay_loop <INT>                          #检查后端服务器的时间间隔
lb_algo rr|wrr|lc|wlc|lblc|sh|dh        #定义调度方法
lb_kind NAT|DR|TUN                      #集群的类型,注意要大写
persistence_timeout <INT>             #持久连接时长
protocol TCP|UDP|SCTP                   #指定服务协议
sorry_server <IPADDR> <PORT>            #所有RS故障时，备用服务器地址
real_server <IPADDR> <PORT>  {          #RS的IP和PORT
    weight <INT>                          #RS权重
    notify_up <STRING>|<QUOTED-STRING>  #RS上线通知脚本
    notify_down <STRING>|<QUOTED-STRING> #RS下线通知脚本
    HTTP_GET|SSL_GET|TCP_CHECK|SMTP_CHECK|MISC_CHECK { ... } #定义当前主机的健康状态检测方法
 }
}
'''


应用层监测

应用层检测：HTTP_GET|SSL_GET
'''
HTTP_GET|SSL_GET {
    url {
        path <URL_PATH>       #定义要监控的URL
        status_code <INT>         #判断上述检测机制为健康状态的响应码，一般为 200
    }
    connect_timeout <INTEGER>     #客户端请求的超时时长, 相当于haproxy的timeout server
    nb_get_retry <INT>            #重试次数
    delay_before_retry <INT>  #重试之前的延迟时长
    connect_ip <IP ADDRESS>       #向当前RS哪个IP地址发起健康状态检测请求
    connect_port <PORT>           #向当前RS的哪个PORT发起健康状态检测请求
    bindto <IP ADDRESS>           #向当前RS发出健康状态检测请求时使用的源地址
    bind_port <PORT>          #向当前RS发出健康状态检测请求时使用的源端口
}
'''


范例：
'''
virtual_server 10.0.0.10 80 {
        delay_loop 3
        lb_algo rr
        lb_kind DR
        protocol TCP
        sorry_server 127.0.0.1 80
        real_server 10.0.0.7 80 {
            weight 1
            HTTP_GET {
                url {
                    path /
                    status_code 200
                }
                connect_timeout 1
                nb_get_retry 3
                delay_before_retry 1
            }
        }
        real_server 10.0.0.17 80 {
            weight 1
            HTTP_GET {
                url {
                    path /
                    status_code 200
                }
                connect_timeout 1
                nb_get_retry 3
                delay_before_retry 1
            }
        }
}
'''


TCP监测

传输层检测：TCP_CHECK
'''
TCP_CHECK {
 connect_ip <IP ADDRESS>  #向当前RS的哪个IP地址发起健康状态检测请求
 connect_port <PORT>      #向当前RS的哪个PORT发起健康状态检测请求
 bindto <IP ADDRESS>      #发出健康状态检测请求时使用的源地址
 bind_port <PORT>         #发出健康状态检测请求时使用的源端口
 connect_timeout <INTEGER>    #客户端请求的超时时长, 等于haproxy的timeout server   
}
'''


范例：
'''
virtual_server 10.0.0.10 80 {
    delay_loop 6
    lb_algo wrr
    lb_kind DR
    #persistence_timeout 120    #会话保持时间
    protocol TCP
    sorry_server 127.0.0.1 80
    real_server 10.0.0.7 80 {
        weight 1
        TCP_CHECK {
            connect_timeout 5
            nb_get_retry 3
            delay_before_retry 3
            connect_port 80
        }
    }
    real_server 10.0.0.17 80 {
        weight 1
        TCP_CHECK {
            connect_timeout 5
            nb_get_retry 3
            delay_before_retry 3
            connect_port 80
        } 
    } 
}
'''

本文链接：http://www.yunweipai.com/35378.html

----------------------------------------------

实战案例： 实现单主的 LVS-DR 模式

实战案例

实战案例1：实现单主的LVS-DR模式
准备web服务器并使用脚本绑定VIP至web服务器lo网卡

'''
#准备两台后端RS主机
[root@rs1 ~]#cat lvs_dr_rs.sh
#!/bin/bash
#Author:wangxiaochun
#Date:2017-08-13
vip=10.0.0.10
mask='255.255.255.255'
dev=lo:1
rpm -q httpd &> /dev/null || yum -y install httpd &>/dev/null
service httpd start &> /dev/null && echo "The httpd Server is Ready!"
echo "<h1><code>hostname</code></h1>" > /var/www/html/index.html

case $1 in
start)
    echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore
    echo 1 > /proc/sys/net/ipv4/conf/lo/arp_ignore
    echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce
    echo 2 > /proc/sys/net/ipv4/conf/lo/arp_announce
    ifconfig $dev $vip netmask $mask #broadcast $vip up
    #route add -host $vip dev $dev
    echo "The RS Server is Ready!"
    ;;
stop)
    ifconfig $dev down
    echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore
    echo 0 > /proc/sys/net/ipv4/conf/lo/arp_ignore
    echo 0 > /proc/sys/net/ipv4/conf/all/arp_announce
    echo 0 > /proc/sys/net/ipv4/conf/lo/arp_announce
    echo "The RS Server is Canceled!"
    ;;
*) 
    echo "Usage: $(basename $0) start|stop"
    exit 1
    ;;
esac

[root@rs1 ~]#bash lvs_dr_rs.sh start 
The httpd Server is Ready!
The RS Server is Ready!
[root@rs1 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.0.0.10/32 scope global lo:1
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:32:80:38 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.7/24 brd 10.0.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe32:8038/64 scope link 
       valid_lft forever preferred_lft forever

[root@rs2 ~]#bash lvs_dr_rs.sh start 
The httpd Server is Ready!
The RS Server is Ready!

[root@rs2 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.0.0.10/32 scope global lo:1
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:33:b4:1a brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.17/24 brd 10.0.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fe33:b41a/64 scope link 
       valid_lft forever preferred_lft forever

#测试访问两台RS
[root@centos6 ~]#curl 10.0.0.7
<h1>rs1.magedu.org</h1>
[root@centos6 ~]#curl 10.0.0.17
<h1>rs2.magedu.org</h1>
'''


配置keepalived
'''
#ka1节点的配置
[root@ka1-centos8 ~]#cat    /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
            root@localhost
        }
        notification_email_from keepalived@localhost
        smtp_server 127.0.0.1
        smtp_connect_timeout 30
        router_id ka1.magedu.org
        vrrp_mcast_group4 224.0.100.10
    }
vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 66
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    }
virtual_server 10.0.0.10 80 {
        delay_loop 3
        lb_algo rr
        lb_kind DR
        protocol TCP
        sorry_server 127.0.0.1 80
        real_server 10.0.0.7 80 {
            weight 1
            HTTP_GET {               #应用层检测
                url {
                    path /
                    status_code 200
                }
                connect_timeout 1
                nb_get_retry 3
                delay_before_retry 1
            }
        }
        real_server 10.0.0.17 80 {
            weight 1 
            TCP_CHECK {              #另一台主机使用TCP检测
                connect_timeout 5
                nb_get_retry 3
                delay_before_retry 3
                connect_port 80
            }
        }
}

#ka2节点的配置，配置和ka1基本相同，只需修改三行
[root@ka2-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
            root@localhost
        }
        notification_email_from keepalived@localhost
        smtp_server 127.0.0.1
        smtp_connect_timeout 30
        router_id ka1.magedu.org             #修改此行
        vrrp_mcast_group4 224.0.100.10
    }
vrrp_instance VI_1 {
    state BACKUP                            #修改此行
    interface eth0
    virtual_router_id 66
    priority 80                             #修改此行
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    }
virtual_server 10.0.0.10 80 {
        delay_loop 3
        lb_algo rr
        lb_kind DR
        protocol TCP
        sorry_server 127.0.0.1 80
        real_server 10.0.0.7 80 {
            weight 1
            HTTP_GET {
                url {
                    path /
                    status_code 200
                }
                connect_timeout 1
                nb_get_retry 3
                delay_before_retry 1
            }
        }
        real_server 10.0.0.17 80 {
            weight 1
            TCP_CHECK {
                connect_timeout 5
                nb_get_retry 3
                delay_before_retry 3
                connect_port 80
            }
        }
}
'''


访问测试结果
'''
[root@centos6 ~]#curl 10.0.0.10
<h1>rs1.magedu.org</h1>
[root@centos6 ~]#curl 10.0.0.10
<h1>rs2.magedu.org</h1>

[root@ka1-centos8 ~]#dnf -y install ipvsadm
[root@ka1-centos8 ~]#ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  10.0.0.10:80 rr
  -> 10.0.0.7:80                  Route   1      0          0         
  -> 10.0.0.17:80                 Route   1      0          0   
'''


模拟故障
'''
#第一台RS1故障，自动切换至RS2
[root@rs1 ~]#chmod 0 /var/www/html/index.html 

[root@centos6 ~]#curl 10.0.0.10
<h1>rs2.magedu.org</h1>
[root@centos6 ~]#curl 10.0.0.10
<h1>rs2.magedu.org</h1>

[root@ka1-centos8 ~]#dnf -y install ipvsadm
[root@ka1-centos8 ~]#ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  10.0.0.10:80 rr
  -> 10.0.0.17:80                 Route   1      0          3  

#后端RS服务器都故障，启动Sorry Server
[root@rs2 ~]#systemctl stop httpd
[root@centos6 ~]#curl 10.0.0.10
Sorry Server on ka1
[root@ka1-centos8 ~]#ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  10.0.0.10:80 rr
  -> 127.0.0.1:80                 Route   1      0          0  

#ka1故障，自动切换至ka2
[root@ka1-centos8 ~]#killall keepalived
[root@centos6 ~]#curl 10.0.0.10
Sorry Server on ka2

#恢复都有后端 RS
[root@rs1 ~]#chmod 644 /var/www/html/index.html
[root@rs2 ~]#systemctl start httpd
[root@centos6 ~]#curl 10.0.0.10
<h1>rs1.magedu.org</h1>
[root@centos6 ~]#curl 10.0.0.10
<h1>rs2.magedu.org</h1>
[root@ka1-centos8 ~]#hostname -I
10.0.0.8 
[root@ka2-centos8 ~]#hostname -I
10.0.0.18 10.0.0.10 

#恢复ka1服务器，又抢占回原来的VIP
[root@ka1-centos8 ~]#systemctl start keepalived.service 
[root@ka1-centos8 ~]#hostname -I
10.0.0.8 10.0.0.10 
[root@ka2-centos8 ~]#hostname -I
10.0.0.18 
[root@centos6 ~]#curl 10.0.0.10
<h1>rs1.magedu.org</h1>
[root@centos6 ~]#curl 10.0.0.10
<h1>rs2.magedu.org</h1>
'''
 
本文链接：http://www.yunweipai.com/35380.html

----------------------------------------------

实战案例： 实现双主的 LVS-DR 模式

实战案例2：实现双主的LVS-DR模式
'''
[root@ka1-centos8 ~]#vim /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
            root@localhost
        }
        notification_email_from keepalived@localhost
        smtp_server 127.0.0.1
        smtp_connect_timeout 30
        router_id ka1.magedu.org                #另一个节点为ka2.magedu.org
        vrrp_mcast_group4 224.0.100.10
    }

vrrp_instance VI_1 {
    state MASTER                                #在另一个结点上为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                                #在另一个结点上为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1      #指定VIP
    }
}

vrrp_instance VI_2 {
    state BACKUP                                #在另一个结点上为MASTER
    interface eth0
    virtual_router_id  88
    priority 80                                 #在另一个结点上为100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:2      #指定VIP2
    }
}
virtual_server 10.0.0.10 80 {  
    delay_loop 6
    lb_algo rr
    lb_kind DR
    protocol TCP
    sorry_server 127.0.0.1 80
    real_server 10.0.0.7 80 {  #指定RS1地址
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }

    }
    real_server 10.0.0.17 80 {                  #指定RS2地址
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }

    }   

}

virtual_server 10.0.0.20 80 {                       #指定VIP2
    delay_loop 6
    lb_algo rr
    lb_kind DR
    protocol TCP
    sorry_server 127.0.0.1 80
    real_server 10.0.0.27 80 {                      #指定RS3地址
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }

    }
    real_server 10.0.0.37 80 {                      #指定RS4地址
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 3
            nb_get_retry 3
            delay_before_retry 3
        }
    }   
}
'''

本文链接：http://www.yunweipai.com/35382.html



----------------------------------------------

实战案例： 实现双主的，LVS-DR 模式利用FWM绑定成一个双主集群服务

实战案例3：实现双主的LVS-DR模式，利用FWM绑定成一个双主集群服务
'''
[root@ka1-centos8 ~]#vim  /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.100.100.100
    }

vrrp_instance VI_1 {
    state MASTER                #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}
vrrp_instance VI_2 {
    state BACKUP                    #在另一个节点为MASTER
    interface eth0
    virtual_router_id 88
    priority 80                     #在另一个节点为100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:2
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
}

virtual_server fwmark 6 {   #指定FWM为6 
    delay_loop 2
    lb_algo rr
    lb_kind DR
    nat_mask 255.255.255.0
    protocol TCP
    sorry_server 127.0.0.1 80
    real_server 10.0.0.7 80 {
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 2
            nb_get_retry 3
            delay_before_retry 3
        }
    }
    real_server 10.0.0.17 80 {
        weight 1
        HTTP_GET {
            url {
                path /
                status_code 200
            }
            connect_timeout 2
            nb_get_retry 3
            delay_before_retry 3
        }
    }
}

#两个节点都执行以下操作
[root@ka1-centos8 ~]#iptables -t mangle -A PREROUTING -d 10.0.0.10,10.0.0.20  -p tcp --dport 80 -j MARK --set-mark 6
[root@ka2-centos8 ~]#iptables -t mangle -A PREROUTING -d 10.0.0.10,10.0.0.20  -p tcp --dport 80 -j MARK --set-mark 6

#在RS1和RS2运行下面脚本
[root@rs1 ~]#cat lvs_dr_rs.sh 
#!/bin/bash
#Author:wangxiaochun
#Date:2017-08-13
vip=10.0.0.10
vip2=10.0.0.20
mask='255.255.255.255'
dev=lo:1
dev2=lo:2
rpm -q httpd &> /dev/null || yum -y install httpd &>/dev/null
service httpd start &> /dev/null && echo "The httpd Server is Ready!"
echo "<h1><code>hostname</code></h1>" > /var/www/html/index.html

case $1 in
start)
    echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore
    echo 1 > /proc/sys/net/ipv4/conf/lo/arp_ignore
    echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce
    echo 2 > /proc/sys/net/ipv4/conf/lo/arp_announce
    ifconfig $dev $vip netmask $mask #broadcast $vip up
    ifconfig $dev2 $vip2 netmask $mask #broadcast $vip up
    #route add -host $vip dev $dev
    echo "The RS Server is Ready!"
    ;;
stop)
    ifconfig $dev down
    ifconfig $dev2 down
    echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore
    echo 0 > /proc/sys/net/ipv4/conf/lo/arp_ignore
    echo 0 > /proc/sys/net/ipv4/conf/all/arp_announce
    echo 0 > /proc/sys/net/ipv4/conf/lo/arp_announce
    echo "The RS Server is Canceled!"
    ;;
*) 
    echo "Usage: $(basename $0) start|stop"
    exit 1
    ;;
esac
[root@rs1 ~]#bash lvs_dr_rs.sh  start
[root@rs2 ~]#bash lvs_dr_rs.sh  start

#访问测试
[root@centos6 ~]#curl 10.0.0.10;curl 10.0.0.20
<h1>rs1.magedu.org</h1>
<h1>rs2.magedu.org</h1>
'''


同步组

LVS NAT 模型VIP和DIP需要同步，需要同步组

'''
vrrp_sync_group VG_1 {
 group {
    VI_1  # name of vrrp_instance (below)
    VI_2  # One for each moveable IP
   }
  }
 vrrp_instance VI_1 {
    eth0
    vip
  }
vrrp_instance VI_2 {
    eth1
    dip
  }
'''


本文链接：http://www.yunweipai.com/35384.html




----------------------------------------------

实战案例： 实现其他应用的高可用性

实现其它应用的高可用性 VRRP Script
keepalived利用 VRRP Script 技术，可以调用外部的辅助脚本进行资源监控，并根据监控的结果实现优先动态调整，从而实现其它应用的高可用性功能

VRRP Script 配置

分两步实现：

-定义脚本

vrrp_script：自定义资源监控脚本，vrrp实例根据脚本返回值，公共定义，可被多个实例调用，定义在vrrp实例之外的独立配置块，一般放在global_defs设置块之后。

通常此脚本用于监控指定应用的状态。一旦发现应用的状态异常，则触发对MASTER节点的权重减至低于SLAVE节点，从而实现 VIP 切换到 SLAVE 节点

'''
  vrrp_script <SCRIPT_NAME> {
    script <STRING>|<QUOTED-STRING>   #此脚本返回值为非0时，会触发下面OPTIONS执行
    OPTIONS 
  }
'''


-调用脚本

track_script：调用vrrp_script定义的脚本去监控资源，定义在实例之内，调用事先定义的vrrp_script
'''
  track_script {
    SCRIPT_NAME_1
    SCRIPT_NAME_2
  }
'''

3.7.1.1 定义 VRRP script
'''
vrrp_script <SCRIPT_NAME> {               #定义一个检测脚本，在global_defs 之外配置
      script <STRING>|<QUOTED-STRING>       #shell命令或脚本路径
      interval <INTEGER>                  #间隔时间，单位为秒，默认1秒
      timeout <INTEGER>                   #超时时间
      weight <INTEGER:-254..254> #此值为负数，表示fall（（脚本返回值为非0）时，会将此值与本节点权重相加可以降低本节点权重，如果是正数，表示 rise （脚本返回值为0）成功后，会将此值与本节点权重相加可以提高本节点权重，通常使用负值较多
      fall <INTEGER>                          #脚本几次失败转换为失败，建议设为2以上
      rise <INTEGER>                          #脚本连续监测成功后，把服务器从失败标记为成功的次数
      user USERNAME [GROUPNAME]             #执行监测脚本的用户或组      
      init_fail                             #设置默认标记为失败状态，监测成功之后再转换为成功状态
}
'''


调用 VRRP script
'''
vrrp_instance VI_1 {
    …
    track_script {
        chk_down
  }
}
'''

本文链接：http://www.yunweipai.com/35386.html




----------------------------------------------

实战案例： 实现 VIP 高可用性

实战案例：实现 VIP高可用
'''
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.0.100.100
}

vrrp_script check_down {
    script "[ ! -f /etc/keepalived/down ]" #/etc/keepalived/down存在时返回非0，触发权重-30
    interval 1
    weight -30
    fall 3
    rise 2
    timeout 2
}

vrrp_instance VI_1 {
    state MASTER                #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
       check_down           #调用前面定义的脚本
   }
}

[root@ka1-centos8 ~]#touch /etc/keepalived/down
[root@ka1-centos8 ~]#tail -f /var/log/messages 
Mar 28 19:47:03 ka1-centos8 Keepalived_vrrp[7200]: Script <code>check_down</code> now returning 1
Mar 28 19:47:05 ka1-centos8 Keepalived_vrrp[7200]: VRRP_Script(chk_down) failed (exited with status 1)
Mar 28 19:47:05 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Changing effective priority from 100 to 70
Mar 28 19:47:07 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Master received advert from 10.0.0.18 with higher priority 80, ours 70
Mar 28 19:47:07 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Entering BACKUP STATE
Mar 28 19:47:07 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) removing VIPs.
[root@rs1 ~]#tcpdump -i eth0 -nn 224.0.100.100
19:42:09.578203 IP 10.0.0.8 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
19:42:10.579304 IP 10.0.0.8 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 70, authtype simple, intvl 1s, length 20

[root@ka1-centos8 ~]#rm -f  /etc/keepalived/down
[root@ka1-centos8 ~]#tail -f /var/log/messages 
Mar 28 19:47:45 ka1-centos8 Keepalived_vrrp[7200]: Script <code>check_down</code> now returning 0
Mar 28 19:47:46 ka1-centos8 Keepalived_vrrp[7200]: VRRP_Script(check_down) succeeded
Mar 28 19:47:46 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Changing effective priority from 70 to 100
Mar 28 19:47:46 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) received lower priority (80) advert from 10.0.0.18 - discarding
Mar 28 19:47:47 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) received lower priority (80) advert from 10.0.0.18 - discarding
Mar 28 19:47:48 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) received lower priority (80) advert from 10.0.0.18 - discarding
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Receive advertisement timeout
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Entering MASTER STATE
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) setting VIPs.
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: Sending gratuitous ARP on eth0 for 10.0.0.10
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: (VI_1) Sending/queueing gratuitous ARPs on eth0 for 10.0.0.10
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: Sending gratuitous ARP on eth0 for 10.0.0.10
Mar 28 19:47:49 ka1-centos8 Keepalived_vrrp[7200]: Sending gratuitous ARP on eth0 for 10.0.0.10
[root@rs1 ~]#tcpdump -i eth0 -nn 224.0.100.100
19:49:16.199462 IP 10.0.0.18 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 80, authtype simple, intvl 1s, length 20
19:49:17.199897 IP 10.0.0.18 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 80, authtype simple, intvl 1s, length 20
19:49:17.810376 IP 10.0.0.8 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
19:49:18.811048 IP 10.0.0.8 > 224.0.100.100: VRRPv2, Advertisement, vrid 66, prio 100, authtype simple, intvl 1s, length 20
'''

本文链接：http://www.yunweipai.com/35389.html



----------------------------------------------

实战案例： 实现单主模式的 Nginx 反向代理的高可用

实战案例：实现单主模式的Nginx反向代理的高可用
'''
#在两个节点都配置nginx反向代理
[root@ka1-centos8 ~]#vim /etc/nginx/nginx.conf
http {
    upstream websrvs {
        server 10.0.0.7:80 weight=1;
        server 10.0.0.17:80 weight=1;
    }
    server {
        listen 80;
        location /{
            proxy_pass http://websrvs/;
        }
    }
}

#在两个节点都配置实现nginx反向代理高可用
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.0.100.100
}
vrrp_script check_nginx {
    script "/etc/keepalived/check_nginx.sh"
    #script "/usr/bin/killall -0 nginx"
    interval 1
    weight -30
    fall 3
    rise 5
   timeout 2
}

vrrp_instance VI_1 {
    state MASTER                #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
        chk_nginx
    }
}

[root@ka1-centos8 ~]# yum install psmisc -y
[root@ka1-centos8 ~]# cat /etc/keepalived/check_nginx.sh
#!/bin/bash
/usr/bin/killall -0 nginx
[root@ka1-centos8 ~]# chmod a+x /etc/keepalived/check_nginx.sh 
'''


本文链接：http://www.yunweipai.com/35391.html



----------------------------------------------

实战案例： 实现双主模式 Nginx 反向代理的高可用

实战案例：实现双主模式Nginx反向代理的高可用
'''
#在两个节点都配置nginx反向代理
[root@ka1-centos8 ~]vim /etc/nginx/nginx.conf
http {
    upstream websrvs {
        server 10.0.0.7:80 weight=1;
        server 10.0.0.17:80 weight-1;
    }
    upstream websrvs2 {
        server 10.0.0.27:80 weight=1;
        server 10.0.0.37:80 weight-1;
    }

    server {
        listen 80;
        server_name www.a.com;
        location /{
            proxy_pass http://webservs/;
        }
    }
    server {
        listen 80;
        server_name www.b.com;
        location /{
            proxy_pass http://webservs2/;
        }
    }

}

#在两个节点都配置实现双主模式的nginx反向代理高可用
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.100.100.100
}
vrrp_script check_nginx {
    script "/etc/keepalived/check_nginx.sh"
    #script "/usr/bin/killall -0 nginx"
    interval 1
    weight -30
    fall 3
    rise 5
   timeout 2
}

vrrp_instance VI_1 {
    state MASTER                            #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                            #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
        chk_nginx
    }
}

vrrp_instance VI_2 {
    state BACKUP                        #在另一个节点为MASTER
    interface eth0
    virtual_router_id 88
    priority 80                         #在另一个节点为100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.20/24 dev eth0 label eth0:2
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
        chk_nginx
    }
}
[root@ka1-centos8 ~]# yum install psmisc -y
[root@ka1-centos8 ~]# cat /etc/keepalived/check_nginx.sh
#!/bin/bash
/usr/bin/killall -0 nginx
[root@ka1-centos8 ~]# chmod a+x /etc/keepalived/check_nginx.sh 
'''


本文链接：http://www.yunweipai.com/35393.html



----------------------------------------------

实战案例： 实现 HAProxy 高可用

实战案例：实现HAProxy高可用
'''
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.0.100.100
}
vrrp_script chk_haproxy {               #定义脚本
    script "/etc/keepalived/check_haproxy.sh"
    interval 1
    weight -30
    fall 3
    rise 2
    timeout 2
}

vrrp_instance VI_1 {
    state MASTER                #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
        chk_haproxy                     #调用上面定义的脚本
    }
}
[root@ka1-centos8 ~]# yum install psmisc -y
[root@ka1-centos8 ~]# cat /etc/keepalived/check_haproxy.sh
#!/bin/bash
/usr/bin/killall -0 haproxy
[root@ka1-centos8 ~]# chmod a+x /etc/keepalived/check_haproxy.sh 
'''


本文链接：http://www.yunweipai.com/35395.html




----------------------------------------------

实战案例： 实现 mysql 双主模式的高可用

实战案例：实现MySQL双主模式的高可用
实战案例:实现MySQL双主模式的高可用插图

'''
#先实现MySQL的双主架构

#在ka2第二个节点创建连接MySQL查看同步状态的授权用户
[root@ka2-centos8 ~]#mysql -uroot -p123456
MariaDB [(none)]> grant all on *.* to root@'10.0.0.%'  identified by '123456';

#实现MySQL的健康性检测脚本
[root@ka1-centos8 ~]#vi /etc/keepalived/check_mysql.sh
#!/bin/bash
slave_is=( $(mysql -uroot -p123456 -h10.0.0.18 -e "show slave status\G" | grep "Slave_.*_Running:" | awk '{print $2}') )
if [ "${slave_is[0]}" = "Yes" -a "${slave_is[1]}" = "Yes" ];then
    exit 0
else
    exit 1
fi

#配置keepalived调用上面脚本
[root@ka1-centos8 ~]#cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
    global_defs {
        notification_email {
        root@localhost
        }
    notification_email_from kaadmin@localhost
    smtp_server 127.0.0.1
    smtp_connect_timeout 30
    router_id ka1.magedu.org            #在另一个节点为ka2.magedu.org
    vrrp_mcast_group4 224.0.100.100
}
vrrp_script check_mysql {                   #只需在第一个节点上实现脚本
    script "/etc/keepalived/check_mysql.sh"
    interval 1
    weight -30
    fall 3
    rise 2
    timeout 2
}

vrrp_instance VI_1 {
    state MASTER                #在另一个节点为BACKUP
    interface eth0
    virtual_router_id 66
    priority 100                #在另一个节点为80
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        10.0.0.10/24 dev eth0 label eth0:1
    }
    track_interface {
        eth0
    }
    notify_master "/etc/keepalived/notify.sh master"
    notify_backup "/etc/keepalived/notify.sh backup"
    notify_fault "/etc/keepalived/notify.sh fault"
    track_script {
       check_mysql                      #只需在第一个节点上实现脚本
   }
}
'''

本文链接：http://www.yunweipai.com/35397.html


----------------------------------------------



----------------------------------------------



----------------------------------------------
