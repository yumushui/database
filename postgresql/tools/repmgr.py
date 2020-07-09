#/usr/bin/env python
# conding:utf-8

'''
PostgreSQL高可用目前主要应用是基于流复制（同步/异步）是实例级别的数据同步方案
它是基于WAL流传输的物理复制，可以复制磁盘二进制数据本身中的更改；大型索引构建会创建大量WAL条目，可能会成为流复制的瓶颈。
另一种是逻辑复制，也是基于WAL流传输的复制方式，多了对WAL日志的解析，然后会基于发布订阅的方式进行表级别的数据同步；可以实现在线PG版本升级；但流复制相对更健壮，支持范围更广、更易于使用。

以上两种是PG提供的原生高可用功能，都是非共享存储的方式，流复制通常会配合第三方集群管理或监控组件来实现节点的自动监控、健康检测和自动主备切换、恢复，譬如轻量级的Repmgr、etcd+partroni等，值得提及的是Repmgr 国内有产品厂商进行了优化完善，并已经开源。参考链接：https://pgfans.cn/a?id=430

PG其它高可用方案包括：文件系统（块设备）复制DRBD、基于语句的复制中间件Pgpool-II、基于触发器的主备复制Slony-I、异步多主控机复制Bucardo

PG的分布式再实现负载均衡的同时，也会实现节点（分片）冗余高可用，其中包括GP、PGXL、Citus、Tbase，其整体架构也会融合流复制。
'''

'''
https://pgfans.cn/a?id=430

最近了解到PG分会主要企业成员瀚高软件在官网分享了完善PG研发的代码，其中包括之前推荐的Repmgr优化后的高可用方案。

有兴趣的网友可以去下载使用:)



相关链接：

http://www.highgo.com/content.php?catid=197



Repmgr优化内容：

1. 对浮动virtual IP的管理

注册Primary节点时，会绑定Virtual IP；

failover或switchover时，Virtual IP会随着主节点漂移



2. 集群切换后，节点自动重归集群功能

当集群主备节点切换后，原主节点的daemon进程将自动尝试rejoin操作重归集群



3. 新增node startup命令

节点断电重启后可以由该命令统一启动数据库和repmgrd服务。

该命令将自动判断当前集群中节点的主备状态，防止在启动时形成双主和脑裂



4. 脑裂（双主）的检查与自动恢复功能

本功能主要针对可能的对集群误操作导致的脑裂双主情况进行自动恢复

新增了可以检查集群是否存在双主情况，如果发现集群双主（脑裂）将

选择其中一个节点做rejoin操作，使其作为备节点重归集群。



5. 对硬盘可写的检测

daemon进程会对数据库data目录所在分区是否可写进行监控



6. 对同步流复制转异步的灵活控制

在数据库处于同步流复制下，备节点停库将导致主节点等待，造成业务中断

新增了逻辑控制，可通过配置项控制这种情形下是否将主节点临时改为异步流复制，

待备节点恢复后再改回同步流复制。这样增加了灵活性。



7. 改进了cluster show的信息

在cluster show时增加了对流复制LSN的显示和主备之间LSN差值的显示，用来提示当前流复制的状态


'''

