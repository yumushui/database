
# pgpool-II 

## 一、 pgpool-II Concept

pgpool-II wiki  主页
http://wwww.pgpool.net/mediawiki/index.php/Main_Page

pgpool-II 用户手册
http://www.pgpool.net/docs/latest/pgpool-en.html

FAQ
http://www.pgpool.net/mediawiki/index.php/FAQ

pgpoolAdmin 图形界面管理工具
http://pgpool.projects.pgfoundry.org/pgpoolAdmin/doc/index_en.html



Harry HUANG - Dev  2:45 PM
https://severalnines.com/resources/database-management-tutorials/postgresql-load-balancing-haproxy
SeveralninesSeveralnines
PostgreSQL Load Balancing with HAProxy
Read about deployment, configuration, monitoring, ongoing maintenance, health check methods, read-write splitting, redundancy with VIP and Keepalived, and even more, in this PostgreSQL Load Balancing Tutorial
Jun 6th
2:46
haproxy doesn't do read/write segregation
2:46
this article suggested to use pgpool


### 1.1 pgpool-II 定义

pgpool-II 是一个位于 PostgreSQL服务器 和 PostgreSQL客户端之间的中间价，它可以提供如下功能：
1 连接池： 保持已经连接到 PostgreSQL服务器到连接，使用相同参数时，重用连接；
2 复制： pgpool-II可以管理多个PostgreSQL服务器，复制功能能实现PostgreSQL的高可用，如果其中一台节点失效，服务可以不中断，继续运行。
3 负载均衡： 如果数据库进行了复制，则在任何一台服务器中执行select，都应该返回相同都结果。pgpool-II可以将查询分发到多个可用服务器，提升系统整体吞吐量。
4 限制超过限度的连接： pg会有最大连接数限制，pgpool-II也可以限制连接数，但如果达到最大连接数，会将超过的连接放入队列，而不是直接返回错误。
5 并行查询：使用并行查询时，数据库可以分割到多台服务器上，一个查询在多台服务器上同时执行，以减少总体执行时间。
但需要注意， pgpool-II 虽然具有并行查询功能，但目前该功能还不完善，所以如果想再在 PostgreSQL中做水平拆分，通常使用 postgres-XC 或 PL/proxy 的方案，若以后pgpool功能完善了，也可以放到生产上。

### 1.2 pgpool-II 架构

pgpool-II 完全实现了PostgreSQL的连接协议，客户端连接到 pgpool-II 上，就和连接到pg数据库上完全一样。
pgpool-II 复制是同步的，如果发一个DML语句，将并发得在后端所有数据库上执行，保证了所有数据库的一致性。

一个 pgpool-II 的常见架构图为：
client_01 client_02 client_03 client_04 client_05 client_06

                   pgpool-II
postgres   postgres   postgres   postgres

pgpool-II 是一个多进程的架构，其工作原理为：

pcp进程     pgpool-II父进程        worker进程  - 复制延时检查
管理者                  - 健康检查     PostgreSQL
 
用户 - 查询  pgpool-II子进程  - 查询  - PostgreSQL

一些进程说如下：
pcp 进程： pcp是一个管理工具，用户可以使用这个管理工具向 pgpool-II 发送管理命令。
pgpool-II 父进程： pgpool-II父进程负责检查各个底层数据库的健康状态。
pgpool-II 子进程： 负责接收用户发过来的SQL请求，然后根据规则发送到底层数据库上。
worker 进程： 这是 pgpool-II 3 之后才增加的进程，负责检查底层数据库之间的延时。

### 1.3 pgpool-II 的工作模式

pgpool有连接池、复制、负载均衡等功能，使用这些功能，需要把 pgpool配置在不同的工作模式下，可选工作模式有：

1 原始模式
    原始模式，只实现一个故障切换的功能，可以配置多个后端数据库，打给你第一个后端数据库不能工作时，pgpool-II 会切换到第二个后端数据库，如果第二个后端数据库也不能工作切换到第三个后端数据库。
2 连接池模式
    连接池模式，除了原始模式的功能外，还能实现连接池的功能。
3 复制模式
    复制模式，实现了同步复制的功能，实际就是把修改数据库的操作分发到后端所有数据库上处理，而只读查询则发送给任意一台数据库。此模式可以实现负载均衡功能。
4 主/备模式
    主备模式，使用其他软件（非pgpool自身）完成实际的数据复制，如使用 slony-I或流复制，中间件层使用 pgpool-II，pgpool-II主要提供高可用和连接池的功能。
    在主备模式中，DDL和DML在主节点上执行，select可以在主备节点执行，当然可以强制在主节点执行，需要在select前添加 /*NO LOAD BALANCE*/ 注释
5 并行查询模式
    并行查询模式，实现了查询的并行执行，表可以被分割，数据分布在每个节点中。而且复制和负载均衡功能也可以同时使用。并行模式与主备模式不能同步使用。

在 主备 模式下，还有两种子模式：
    配合 Slony-I 的主备模式
    配置 流复制 的主备模式 

工作模式与功能对应表

复制模式与主备模式给有优缺点，这两种模式的对比为：
-- 复制模式
优点为：
    复制是同步的，不存在最终一致性的问题。
    自动failover。
    读可以负载均衡。
    可以在先恢复，不需要停止 pgpool-II，就可以在线修复或增加一个后端数据库节点。
    容易配置。
缺点为：
    写性能不是很好，有 30% 的写性能下降。
    不支持部分查询。如一些随机函数、序列号，直接在不同的后端数据库执行SQL，将产生不同的结果，所以不能使用这些函数及序列号。

-- 主备模式
优点为：
    写性能较好，只有 10%-20%的性能下降。
    自动 failover。
    可以做读的负载均衡。

缺点为：
    复制是异步的，对应用的使用有限制。
    对于使用 slony-I 实现的主备模式，不能实现DDL的复制，不支持大对象的复制。
    配置复杂。


在 pgpool-II 3.0 之后，支持配合使用 流复制+standby 的主备模式，这是一个很好的读写分离的方式，现在使用这种方式配置的越来越多了。

--  流复制 + 主备模式
优点为：
    智能的读写查询分发。pgpool-II 能区分读写查询，只读查询会负载均衡到各个节点上，写查询只会发送到主库上，这样就解决了 standby智能接受只读到问题。
    智能的负载均衡。 pgpool-II 能检测备库和主库的延时。如果备库到主库延迟超过一定值，读查询会只发到主库上，这样就能保证读到数据的延迟在一定的可控范围内。
    增加 standby 时，不需要停止 pgpool-II .






### 1.4 pgpool-II 的程序模块

pgpool-II 的主程序只有一个，名为 pgpool,还有一些命令行管理工具，都是以 pcp_ 开头的，如下：
pcp_attach_node
pcp_node_count
pcp_pool_status
pcp_proc_info
pcp_recovery_node
pcp_systemdb_info
pcp_detach_node
pcp_node_info
pcp_proc_count
pcp_promote_node
pcp_stop_pgpool
pcp_watchdog_info

这些命令行工具，有的用于在线恢复，有的用于查询信息。

pgpool-II 还提供了一个生成 md5 值的小工具 pg_md5，用于配置pgpool的密码文件，pgpool-II的密码文件存放的密码都是 md5 值，所以配置时需要使用这个工具。

pgpool-II 提供了一个PHP写的 web管理工具，叫 pgpoolAdmin，这个web管理工具可以以web界面的方式实现 pgpool-II 的配置。


## 二、 pgpool-II 的安装方法

### 2.1 源码安装
从 source 源码包安装 pgpool-II ，步骤为

下载安装介质，从 http://www.pgpool.net/mediawiki/index.php/Main_Page  找到下载地址，下载介质
wget http://www.pgpool.net/download.php?f=pgpool-II-3.3.3.tar.gz  pgpool-II-3.3.3.tar.gz

解压：
tar xvf pgpool-II-3.3.3.tar.gz

编译安装：
./configure --prefix=/home/osdba/ 
make
make install

编译是 prefix 指定安装位置，可以根据实际情况更改，如果不指定，默认会安装到 /usr/local 目录

### 2.2 安装 pgpool_regclass
如果使用 pg 8.0 之后，推荐在需要的后端 PostgreSQL中安装 pgpool_regclass 函数，因为它被 pgpool-II 内部使用，否则在不同 schema中处理相同名称的非临时表就会有问题。
pgpool_regclass的安装方法为：
cd pgpool-II-x.x.x/sql/pgpool-pgpool_regclass
make 
make install
pgsql -f pgpool-regclasss.sql  template1


### 2.3 建立 insert_lock 表
如果复制模式中使用了 insert_lock，推荐建立 pgpool_catalog.insert_lock 表，用于解决互斥问题。如果没有 insert_locak表，insert_lock也能工作，但这种情况下，pgpool-II需要锁定插入的目标表，而表锁与VACUUM冲突
所以 insert 会等待很长时间。
建表锁的方法是：
cd pgpool-II-x.x.x/sql
psql -f insert_lock.sql  template1

### 2.4 安装C语言函数
如果一个节点损坏，要在线把失败的节点，再添加回集群。这是需要在所有后端数据库节点的 template1 数据库中安装一些 pgpool-II提供的C语言函数。
C语言函数安装方法为：
cd pgpool-II-x.x.x/sql/pgpool-recovery/
make install
psql -f pgpool-recovery.sql  template1




## 三、 pgpool-II 配置

pgpool-II 的模式比较多，配置也比较复杂，厦门通过几个示例讲解 pgpool-II 是如何配置的。

### 3.1 pgpool-II 的配置文件 及 启停方法

pgpool的配置文件主要有两个
$INSTALL_PATH/etc/pgpool.conf
$INSTALL_PATH/etc/pcp.conf

其中 $INSTALL_PATH 代表安装目录，与编译安装时的 prefix 路径一致，如果不指定默认安装在 /usr/local/ 目录下。

pgpool.conf 的配置项很多，安装完成后会有一个模板文件 pgpool.conf.sample，一般在配置时，先拷贝模板文件，然后配置：
cd /home/osddba/pgpool/etc 
cp pgpool.conf.sample  pgpool.conf
cp pcp.conf.sample  pcp.conf

默认pgpool的端口为本地端口9999，如果需要其他主机连接，可以进行修改：
listen_addresses = '*'
port = 9999

创建默认的 pid 文件：
mkdir -p /home/osdba/pgpool/run 
pid_file_name = '/home/postgres/pgpool/run/pgpool.pid'

pgpool 有一个管理接口，叫 PCP，可以通过网络获取数据库的节点信息，关闭 pgpool-II 等。
这个接口登陆，需要单独的 pgpool 用户名和密码，密码采用 md5 加密，信息配置到 pcp.conf 文件
计算密码 pg123456 对应的 md5 值：
pg_md5 pg123456

在配置文件 pcp.conf 中配置一行内容：
postgres:md5_value

在 pgpool.conf 中最重要的一项是，后端数据库的配置：
backend_hostname0 = ''
backend_port0 = ''
backend_weight0 = ''
backend_hostname1 = ''
backend_port1 = ''
backend_weight1 = ''

可以看到，pgpool中的后端数据库配置为：
backend_hostname${number}
backend_port${number}
backend_weight${number}
其中 ${number} 就是多个主机的序号， 0, 1, 2, ...
pgpool.conf 文件中，还有很多与 pgpool-II 工作模式有关的配置项，在具体工作模式中再介绍。

一般使用 hba 的方式进行登陆认证，所以要在 pgpool.conf 中打开选项：
enable_pool_hba = on 

通常会将访问 pgpool 的用户名和密码的md5值记录在 /home/postgres/pgpool/etc/pool_passwd 中：
pg_md5 -m -p -u postgres pool_passwd

这样就生成了 pool_passwd 文件，查看文件内容：
cat pool_passwd 

-- 启动 pgpool
以上配置完成后，就可以启动 pgpool：
pgpool
这样 pgpool 就会变成一个后台的 daemon  运行，如果想让pgpool前台运行，可以增加 -n 参数：
pgpool -n
这样会将日志打印到终端，如果日志打印到一个文件，可以使用命令：
pgpool -n > /tmp/pgpool.log 2>&1 &

-- 停止 pgpool
pgpool stop 
这种停止方式，如果还有客户端连接，pgpool-II 会一直等待客户端会话断开连接，才能运行结束。
如果想要强制关闭会话，停止 pgpool,命令为：
pgpool -m fast stop

pgpool.conf  中的全部参数


pgpool.conf

# CONNECTIONS
- pgpool Connection Settings -
- pgpool Communication Manager Connection Settings -
- Backend Connection Settings -
- Authentication -
- SSL Connections -

# POOLS
- Concurrent session and pool size -
- Life time -

# LOGs
- Where to log -
- What to log -
- Syslog specific -
- Debug -

# File Locations

# Connection Pooling

# Replication Mode
- Degenerate handling -

# Load Balancing Mode

# Master/Slave Mode
- Streaming -
- Special commands -

# Health Check Global parameters
# Health Check Per Node Parameters (Optional)

# Failover and Failback

# Online Recovery

# WatchDog
- Enabling -
- Connection to up stream servers -
- Watchdog Communication Settings -
- Virtual IP control Settings -
- Behaivor on escalation Setting -
- Watchdog consensus settings for failover -
- LifeCheck Setting -
  -- common --
  -- heartbeat mode --
  -- query mode --
- Other pgpool Connection Settings -

# Others

# In Memory Query Memory Cache




### 3.2 复制和负载均衡的示例

建一个最简单的示例，环境表格为：

pgpool-II 复制和负载均衡的示例环境

主机名    IP地址       角色          数据库名称    数据目录
proxy01  10.0.3.201  安装pgpool    N/A          N/A
data01   10.0.3.212  后端数据节点   datadb       /home/postgres/pgdata
data02   10.0.3.213  后端数据节点   datadb       /home/postgres/pgdata  

这个数据库实例是在操作系统用户 Postgres 下的， pgpool 安装在 /home/postgres/pgdata 目录下

生成配置文件：
cd /home/osdba/pgpool/etc 
cp pgpool.conf.sample  pgpool.conf
cp pcp.conf.sample  pcp.conf

pcp.conf 文件中的配置为：
postgres:{md5_value}

因为要使用 复制 和 负载均衡，需要在 pgpool.conf 中打开下面两个开关：
replication_mode = true 
load_balance_mode = true 

pgpool.conf 中后端数据库的配置如下：
backend_hostname0 = '10.0.3.212'
backend_port0 = 5432
backend_weight0 = 1
backend_hostname1 = '10.0.3.213'
backend_port1 = 5432
backend_weight1 = 1

启动 pgpool 的命令：
pgpool -f /home/postgres/etc/pgpool.conf

在 proxy01 机器上连接 pgpool 的端口 9999，然后建表，并插入两条记录：
psql -h 10.0.3.201 -Upostgres datadb
\d 
create table test01(id int, note text);
insert into test01 values(1, 1);
insert into test01 values(2, 2);

在后端两个数据库上，分别确认表和数据是否都已经存在了：
在主机 data01 上执行：
psql datadb
\d test01
select * from test01;

在 主机 data02 上执行：
psql datadb
\d test01
select * from test01;


### 3.3 使用流复制的主备模式的示例

使用流复制主备模式，环境为：

pgpool-II 复制和负载均衡的示例环境

主机名    IP地址       角色          数据库名称    数据目录
proxy01  10.0.3.201  安装pgpool    N/A          N/A
data01   10.0.3.212  后端数据节点   datadb       /home/postgres/pgdata
data02   10.0.3.213  后端数据节点   datadb       /home/postgres/pgdata  

这个数据库实例是在操作系统用户 Postgres 下的， pgpool 安装在 /home/postgres/pgdata 目录下
主数据库和从数据库之间使用异步的流复制。

生成配置文件：
cd /home/osdba/pgpool/etc 
cp pgpool.conf.sample  pgpool.conf
cp pcp.conf.sample  pcp.conf

在主备模式下，配置文件 pgpool.conf 中的参数 replicaiton_mode 必须为 false，参数 master_slave_mode 必须设置为 true，这表示为主备模式；
将参数 master_slave_sub_mode 设置为 stream ，表示使用的流复制的主备模式；
将参数 load_balance_mode 设置为  on ， 表示在主备模式下，可以使用负载均衡。
这样在 pgpool.conf 中的配置如下：

listen_address = '*'
port = 9999
socket_dir = '/tmp'
pcp_port = 9998
pcp_socket_dir = '/tmp/'
enable_pool_hba = on 
pool_passwd = 'pool_passwd'
pid_file_name = '/home/postgres/pgpool/run/pgpool.pid'
logdir = '/tmp'

backend_hostname0 = '10.0.3.212'
backend_port0 = 5432
backend_weight0 = 1
backend_hostname1 = '10.0.3.213'
backend_port1 = 5432
backend_weight1 = 1

replicaiton_mode = off
master_slave_mode = on 
master_slave_sub_mode = 'stream'
load_balance_mode = on 

不在上面命令行中的参数，保持 pgpool.conf 文件中已有的配置即可。



### 3.4 show 命令

show 在PostgreSQL中是一个真正的 SQL 命令，但 pgpool-II 扩展了此命令。
连接到 pgpool-II 后可以使用 show 命令查看 pgpool-II 的信息，这些命令说明如下：
pool_status ： 获得 pgpool-II 的配置信息。
pool_nodes ： 获得后端各节点的状态信息，如后端这些数据库是否在线。
pool_processes ： 显示 pgpool-II 的进程信息。
pool_pools： 显示 pgpool-II 连接池中的各个连接信息。
pool_version： 显示 pgpool-II 的版本信息

查看 pgpool-II 的配置信息，命令为：
show pool_status；

查看后端数据库节点的信息，命令为：
show pool_nodes；

这个节点信息中，status列出一个数字表示各个后端数据库节点的状态，这些数字的意思如下：
    0 show 命令不会显示这个状态，因为这个状态仅仅在初始化的过程中使用。
    1 节点已经启动，但没有连接。
    2 节点已经启动，有连接。
    3 节点down。

查看 pgpool 的各个进程信息，命令如下：
show pool_processes

查看 连接池中各个连接情况，命令为：
show pool_pools;

查看 pgpool-II 的版本，命令为：
show pool_version;




## 四、 pgpool-II 高可用配置方法

pgpool-II 提供了完善的高可用机制，配置了高可用后，当后端的一个节点出现故障时，pgpool-II会把请求需求切换到另一个节点，而且不会影响前端的服务，这称为 “failover”。
但一个节故障，系统会降级节点来提供服务，这相当于高可用降级，如果剩下的节点再故障，服务就会停止。
所以高可用降级后，要尽快恢复失败的节点，让集群恢复到原先的高可用状态，这个过程叫 failback.
pgpool-II 可以实现在线的 failback ，即不需要停止服务的 failback.

pgpool-II 高可用的机制及配置方法如下：

### 4.1  pgpool-II 高可用切换及恢复的原理
后端数据库执行请求失败了，或配置主动检查后发现后端数据库出现故障，pgpool-II 就会把后端数据库状态记录为 “detached”，新的请求将不再发到这些故障节点上，从而实现高可用。
这对于复制模式下的数据库，是没有问题的，但对于主备模式，就存在问题了： 因为在主备模式下，备库通常是只读的，如果 pgpool-II 只是简单地把强求发送到备节点，显然DML会失败，这时需要将备节点激活成主节点，让其能够接受写操作。
pgpool-II 给用户提供了配置项，可以配置一个脚本程序，当发生故障切换是，pgpool-II 调用用户提供的脚本程序，从而实现备库激活的功能。

当一个节点故障时，pgpool-II 发生了切换，但这个故障的节点如何加回集群，让集群恢复成高可用状态呢？这里最难解决的是同步。
因为原来的节点临时故障，它的数据不再与另外的节点同步，所以加回集群提供服务前，必须完成数据的同步。
最简单的方法是，停止对外服务，然后同步数据，同步完成后，再对外提供服务。但该方案回导致服务停止的时间太长，这对于生产系统来说是不能接受的，所以 pgpool-II 提供了一个基本不停止或停止很短的 failback 的方法。

pgpool-II 的 failback 方法简单描述为：
第一过程： 对数据库进行全量北方，并将其热备份到出故障的节点上。在这个过程中，是热备份，所以可以不停止服务。
第二过程： 短暂停止服务，对有了热备份的故障节点进行增量恢复，恢复在全量备份期间产生的增量数据，让失败节点的数据与现有节点的一致。增量恢复后，对外提供服务。增量服务时间较短，所以停止服务的时间较短。
pgpool-II 提供了参数，允许用户指定第一个过程和第二个过程的脚本程序，从而灵活定义如何对数据库做全量热备份及增量备份恢复，第一个过程可以使用PostgreSQL自身提供的基于WAL日志的热备份功能。

上面是简单的在线恢复过程，实际 pgpool-II 的更详细恢复步骤如下：
    执行 CHECKPOINT
    在线恢复的第一阶段：使用postgresql.conf 中的 recovery_user 和 recovery_pass，连接到一台没有坏的主库上的 template1 数据库上，调用pgpool提供的C函数 pgpool_recovery，执行 reocvery_1st_stage_command 脚本
    等待所有的客户端断开与 pgpool 的连接，然后 pgpool-II 停止服务；
    再一次执行 checkpoint；
    在线恢复第二阶段，与前面类似，执行 recovery_2nd_stage_command 指定的脚本，这个脚本是在数据库的数据目录下的；
    启动要恢复的数据库：与前面一样，同样是连接到一台没有坏的主库上，只是这次要执行主库上的函数 pgpool_remote_start，这个函数自动执行名为 pgpool_remote_start 脚本，这个脚本在主库上，需要ssh到恢复节点才能开始恢复；
    pgpool-II 恢复用户的使用；

从上面的过程，可以总结几点：
    pgpool-II 中恢复使用的几个自定义脚本都是放在后端数据库的 PGDATA目录下的，而不是在 pgpool-II 所运行的机器上；
    这几个自定义脚本的执行，实际是pgpool-II连接到后端数据库，调用pgpool-II提供的C语言函数，然后C语言函数来执行的；
    pgpool-II提供的C函数不是谁的能执行的，必须是postgresql的超级用户才可以。
    上面的过程，最需要关注第二个阶段，第二阶段开始后，pgpool-II就停止服务来，这个阶段时间越短越好。
    在“等待所有的客户端断开与pgpool的连接，然后pgpool-II 停止服务“是，如果客户端一直没有断开与 pgpool 的连接，那就不能开始第二阶段，这也是个大问题。
    有一些过程是通过执行脚本来完成的，如果脚本因编写原因，或者其他原因hang住来，会不会让给pgpool-II一直处于恢复状态？
    recovery_timeout ： 在恢复过程中，超过这个时间没有完成，则 pgpool-II 取消在线恢复，正常提供服务，因为全量备份时间比较长，这个参数也需要设置一个比较长的时间。
    client_idel_limit_in_recovery ： 在恢复第二阶段，客户端执行一个命令后，若指定的时间内没有再执行命令，则 pgpool-II 断开此连接。默认是0，不主动断开连接；可以设置为 -1，立即断开与客户端的连接。


### 4.2  pgpool-II 的健康检查

    执行用户的请求失败后做“failover”，可以主动配置检测。
    当然并不是任何命令执行失败后都会 failover，如果用户发出的命令本身有问题，导致执行失败，此事不会发生切换；只有与后端数据库的通信故障时，才会切换；如果网络故障hang住时间长，会导致故障后长时间内不能完成切换。
    主动检测的方法是 pgpool-II 主动发起一个到后端数据库的连接，看能否连接，以判断后端数据库工作是否正常，如果连接在一定时间内不返回，pgpool-II 会认为后端数据库出现来问题。

    健康检查主要有 pgpool.conf 中的几个参数控制：
    health_check_timeout ： 指定健康检查超时时间，在这个时间内不返回，则认为后端出现故障，默认为20秒。
    health_check_period : 检查的周期，即多长时间检测一次。默认为0，表示不实用健康检查功能。
    health_check_user ： 健康检查时，连接后端数据库的用户名
    health_check_password ： 健康检查时，连接后端数据库的密码


### 4.3  复制和负载均衡模式下的高可用示例

    pgpool-II 复制和负载均衡的高可用示例环境

主机名    IP地址       角色          数据库名称    数据目录
proxy01  10.0.3.201  安装pgpool    N/A          N/A
data01   10.0.3.212  后端数据节点   datadb       /home/postgres/pgdata
data02   10.0.3.213  后端数据节点   datadb       /home/postgres/pgdata  

    其中pgpool-II 安装在 proxy01 机器的 /home/postgres/pgpool 目录下。因为要使用在线恢复，需要在后端数据库节点 data01 和 data02 上安装 pgpool-II 的C语言函数。

    pcp文件中的配置为：
osddba:{md5_value}

    pool_hba.conf 中的配置如下：
local all  all         trust
host  all  all   127.0.0.1    md5
host  all  all   0/0          md5

    pool_passwd 配置文件的内容如下：
osdba:{md5_value}

    配置文件 /home/postgres/pgpool/pgpool.conf 的内容如下：


其中的重点是  pgpool.conf 的配置
    要使用复制和负载均衡模式，所以下面两项要设置为 on ：
replication_mode = on
load_balance_mode = on

    使用在线恢复时，可看到后端数据库配置中多了两项，如下：
backedn_data_directory0 = '/home/postgres/pgdata'
backend_flag0 = 'ALLOW_TO_FAILOVER'

    连接到主库，调用C函数，执行备份恢复的超级用户信息为：
recovery_user = 'osdba'
recovery_passwor = 'xxxxx'

    在线恢复的几个最重要的参数：
recovery_1st_stage_command = 'recovery_1st.sh'
recovery_2nd_stage_command = 'recovery_2nd.sh'
recovery_timeout = 3600
client_limit_in_recovery = -1

    实际还有一个脚本 pgpool_remote_start ，这个脚本名称固定，不能任意配置指定。
    这三个脚本的用途分别为：
    第一阶段脚本为： recovery_1st.sh 使用流复制完成全量备份，同时把要恢复的节点上的数据库启动到异步 standby 的模式下，从而开始恢复从主库上过来的WAL日志
    第二阶段脚本为： recovery_2en.sh 检查恢复节点上 standby 库是否与主库完全一直了，如果一致，则退出。
    pgpool_remote_start 脚本用于激活恢复的节点上的备库。第二阶段后， pgpool-II 不会让主库完全一样了。此事 pgpool-II 就可以进入正常模式工作了。

    在线恢复配置的难点，就是如何编写这三个脚本，这个三个脚本的示例为：

    recovery_1st.sh 脚本：

    脚本内容解析：

    recovery_2nd.sh 脚本：

    脚本内容解析：

    pool_remote_start 脚本：

    脚本内容解析：


高可用切换演示：



### 4.4  使用流复制的主备模式下的高可用示例

    pgpool-II 复制和负载均衡的高可用示例环境

主机名    IP地址       角色          数据库名称    数据目录
proxy01  10.0.3.201  安装pgpool    N/A          N/A
data01   10.0.3.212  后端数据节点   datadb       /home/postgres/pgdata
data02   10.0.3.213  后端数据节点   datadb       /home/postgres/pgdata  

在备库模式下，如果备库出现问题，基本不需要做什么处理；而主库出现问题，需要激活备库，让备库工作从只读模式提升到可读写的模式。

先把 pgpool 的各种配置文件准备好：

pcp.conf 文件中的配置如下：

pool_hba.conf  中的配置如下：

pool_passwd 配置文件中的内容如下：

pgpool.conf 配置文件中的内容如下：

在使用流复制的主备模式下，一般需要配置 sr_check_ 相关参数，如：
sr_check_period = 5
sr_check_user = 'osdba'
sr_check_password = 'xxxxx'

在从库上安装 C语言函数：

从库上的 postgresql.conf ，一些关键配置如下：
listen_addressees = '*'
wal_level = hot_standby
max_wal_senders = 10
hot_standby = on

在两个服务器中，创建 .pgpass 文件： 

使用 pg_basebackup 工具搭建从库：
pg_basebackup  -x -h {host_ip}  -P -U postgres -D /home/postgres/pgdata

创建一个 recovery.conf  文件，内容为：
stadnby_mode = 'on'
primary_conninfo = ''

至此就可以启动 10.0.3.212 上的备库
pg_ctl -D {pg_data_dir}  start 

测试主备模式的 pgpool 的连接：
psql -h 10.0.3.201  -p 9999 -U osdba  -d datadb

测试故障切换，查看 pgpool 连接能否正常

关闭从库

关闭主库

备库 down 之后，再启动，不会自动加入节点中，需要执行 pcp_recovery_node 命令，将备库节点的状态变成正常

再次确认后端数据库节点的状态：


## 五、 pgpool-II 总结

上面介绍了 pgpool-II 的原理和使用，但 pgpool-II 还有更丰富的功能，以及一些更复杂的配置方法。

其他内容可以参考官方文档和资料。





------------------------

测试环境：

10.170.0.2  dba-test-vm-pg12-replicaiton-test
10.170.0.3  dba-test-vm-pg12-replicaiton-test-03


##  在主机2创建 replication
vim pg_start.sh  pg_stop.sh  psql.sh  setup_pg_replication.sh

/bin/sh  setup_pg_replication.sh
10.170.0.2
1533
1533

但启动实例时，提示下面的错误：
2020-08-20 16:36:52.597 CST [29011] FATAL:  could not access file "hll": No such file or directory
2020-08-20 16:36:52.597 CST [29011] LOG:  database system is shut down

还是启动文件中的扩展报错：
shared_preload_libraries = 'hll,hstore,pg_trgm,uuid-ossp,pglogical'
将扩展注释掉，则可以启动成功。

## 安装 pgpool
yum search pgpool-II

# yum install pgpool-II-12


-- pgpool 安装过程

[root@dba-test-vm-pg12-replicaiton-test-03 data]# yum install pgpool-II-12
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.xtom.com.hk
 * centos-sclo-rh: mirror-hk.koddos.net
 * epel: d2lzkl7pfhq30w.cloudfront.net
 * extras: mirror-hk.koddos.net
 * updates: mirror-hk.koddos.net
Resolving Dependencies
--> Running transaction check
---> Package pgpool-II-12.x86_64 0:4.1.2-1.rhel7 will be installed
--> Processing Dependency: libmemcached for package: pgpool-II-12-4.1.2-1.rhel7.x86_64
--> Processing Dependency: libmemcached.so.11()(64bit) for package: pgpool-II-12-4.1.2-1.rhel7.x86_64
--> Running transaction check
---> Package libmemcached.x86_64 0:1.0.16-5.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==============================================================================================
 Package                 Arch              Version                    Repository         Size
==============================================================================================
Installing:
 pgpool-II-12            x86_64            4.1.2-1.rhel7              pgdg12            707 k
Installing for dependencies:
 libmemcached            x86_64            1.0.16-5.el7               base              237 k

Transaction Summary
==============================================================================================
Install  1 Package (+1 Dependent package)

Total download size: 944 k
Installed size: 4.0 M
Is this ok [y/d/N]: y
Downloading packages:
(1/2): libmemcached-1.0.16-5.el7.x86_64.rpm                            | 237 kB  00:00:00
(2/2): pgpool-II-12-4.1.2-1.rhel7.x86_64.rpm                           | 707 kB  00:00:02
----------------------------------------------------------------------------------------------
Total                                                         344 kB/s | 944 kB  00:00:02
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : libmemcached-1.0.16-5.el7.x86_64                                           1/2
  Installing : pgpool-II-12-4.1.2-1.rhel7.x86_64                                          2/2
  Verifying  : libmemcached-1.0.16-5.el7.x86_64                                           1/2
  Verifying  : pgpool-II-12-4.1.2-1.rhel7.x86_64                                          2/2

Installed:
  pgpool-II-12.x86_64 0:4.1.2-1.rhel7

Dependency Installed:
  libmemcached.x86_64 0:1.0.16-5.el7

Complete!

# rpm -ql pgpool-II-12
/etc/pgpool-II-12/failover.sh.sample
/etc/pgpool-II-12/follow_master.sh.sample
/etc/pgpool-II-12/pcp.conf.sample
/etc/pgpool-II-12/pgpool.conf.sample
/etc/pgpool-II-12/pgpool.conf.sample-logical
/etc/pgpool-II-12/pgpool.conf.sample-master-slave
/etc/pgpool-II-12/pgpool.conf.sample-replication
/etc/pgpool-II-12/pgpool.conf.sample-stream
/etc/pgpool-II-12/pgpool_remote_start.sample
/etc/pgpool-II-12/pool_hba.conf.sample
/etc/pgpool-II-12/recovery_1st_stage.sample
/etc/pgpool-II-12/recovery_2nd_stage.sample
/etc/sysconfig/pgpool-II-12
/run
/usr/lib/systemd/system/pgpool-II-12.service
/usr/lib/tmpfiles.d/pgpool-II-12.conf
/usr/pgpool-12
/usr/pgpool-12/bin/pcp_attach_node
/usr/pgpool-12/bin/pcp_detach_node
/usr/pgpool-12/bin/pcp_node_count
/usr/pgpool-12/bin/pcp_node_info
/usr/pgpool-12/bin/pcp_pool_status
/usr/pgpool-12/bin/pcp_proc_count
/usr/pgpool-12/bin/pcp_proc_info
/usr/pgpool-12/bin/pcp_promote_node
/usr/pgpool-12/bin/pcp_recovery_node
/usr/pgpool-12/bin/pcp_stop_pgpool
/usr/pgpool-12/bin/pcp_watchdog_info
/usr/pgpool-12/bin/pg_enc
/usr/pgpool-12/bin/pg_md5
/usr/pgpool-12/bin/pgpool
/usr/pgpool-12/bin/pgpool_setup
/usr/pgpool-12/bin/pgproto
/usr/pgpool-12/bin/watchdog_setup
/usr/pgpool-12/lib/libpcp.so
/usr/pgpool-12/lib/libpcp.so.1
/usr/pgpool-12/lib/libpcp.so.1.0.0
/usr/pgpool-12/share/pgpool-II-pg12-libs.conf
/usr/pgpool-12/share/pgpool-II/insert_lock.sql
/usr/pgpool-12/share/pgpool-II/pgpool.pam
/usr/pgsql-12/lib/bitcode/pgpool-recovery.index.bc
/usr/pgsql-12/lib/bitcode/pgpool-recovery/pgpool-recovery.bc
/usr/pgsql-12/lib/bitcode/pgpool-regclass.index.bc
/usr/pgsql-12/lib/bitcode/pgpool-regclass/pgpool-regclass.bc
/usr/pgsql-12/lib/bitcode/pgpool_adm.index.bc
/usr/pgsql-12/lib/bitcode/pgpool_adm/pgpool_adm.bc
/usr/share/doc/pgpool-II-12-4.1.2
/usr/share/doc/pgpool-II-12-4.1.2/AUTHORS
/usr/share/doc/pgpool-II-12-4.1.2/ChangeLog
/usr/share/doc/pgpool-II-12-4.1.2/INSTALL
/usr/share/doc/pgpool-II-12-4.1.2/NEWS
/usr/share/doc/pgpool-II-12-4.1.2/README
/usr/share/doc/pgpool-II-12-4.1.2/TODO
/usr/share/licenses/pgpool-II-12-4.1.2
/usr/share/licenses/pgpool-II-12-4.1.2/COPYING
/var/run/pgpool-II-12



-------  配置 pgpool 启动文件后，有报错：
Aug 21 08:34:54 dba-test-vm-pg12-replicaiton-test-03 pgpool[31278]: [4-1] 2020-08-21 08:34:54: pid 31278: FATAL:  could not open pid file as /var/run/pgpool/pgpool.pid. reason: No such file or directory

mkdir -p /var/run/pgpool/pgpool.pid

启动 pgpool 命令如下：
pgpool -n -d > /tmp/pgpool.log 2>&1 &
pgpool -a  /etc/pool_hba.conf -f /etc/pgpool.conf  -F /etc/pcp.conf

重新加载不需要重启生效的命令：
pgpool reload 

关闭 pgpool :
pgpool -m fast stop 

查看系统日志：
tail -f /var/log/messages

对应的日志为：
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [4-1] 2020-08-21 08:40:26: pid 31294: LOG:  Backend status file /tmp/pgpool_status does not exist
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [9-1] 2020-08-21 08:40:26: pid 31294: LOG:  memory cache initialized
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [9-2] 2020-08-21 08:40:26: pid 31294: DETAIL:  memcache blocks :64
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [11-1] 2020-08-21 08:40:26: pid 31294: LOG:  pool_discard_oid_maps: discarded memqcache oid maps
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [12-1] 2020-08-21 08:40:26: pid 31294: LOG:  waiting for watchdog to initialize
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [12-1] 2020-08-21 08:40:26: pid 31296: LOG:  setting the local watchdog node name to "10.170.0.2:9999 Linux dba-test-vm-pg12-replicaiton-test-03"
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [13-1] 2020-08-21 08:40:26: pid 31296: LOG:  watchdog cluster is configured with 1 remote nodes
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [14-1] 2020-08-21 08:40:26: pid 31296: LOG:  watchdog remote node:0 on 10.170.0.2:9000
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [15-1] 2020-08-21 08:40:26: pid 31296: LOG:  interface monitoring is disabled in watchdog
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [16-1] 2020-08-21 08:40:26: pid 31296: INFO:  IPC socket path: "/tmp/.s.PGPOOLWD_CMD.9000"
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [17-1] 2020-08-21 08:40:26: pid 31296: LOG:  watchdog node state changed from [DEAD] to [LOADING]
Aug 21 08:40:26 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [19-1] 2020-08-21 08:40:26: pid 31296: LOG:  new outbound connection to 10.170.0.2:9000
Aug 21 08:40:31 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [24-1] 2020-08-21 08:40:31: pid 31296: LOG:  watchdog node state changed from [LOADING] to [JOINING]
Aug 21 08:40:35 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [29-1] 2020-08-21 08:40:35: pid 31296: LOG:  watchdog node state changed from [JOINING] to [INITIALIZING]
Aug 21 08:40:36 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [34-1] 2020-08-21 08:40:36: pid 31296: LOG:  I am the only alive node in the watchdog cluster
Aug 21 08:40:36 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [34-2] 2020-08-21 08:40:36: pid 31296: HINT:  skipping stand for coordinator state
Aug 21 08:40:36 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [35-1] 2020-08-21 08:40:36: pid 31296: LOG:  watchdog node state changed from [INITIALIZING] to [MASTER]
Aug 21 08:40:36 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [37-1] 2020-08-21 08:40:36: pid 31296: LOG:  I am announcing my self as master/coordinator watchdog node
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [42-1] 2020-08-21 08:40:40: pid 31296: LOG:  I am the cluster leader node
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [42-2] 2020-08-21 08:40:40: pid 31296: DETAIL:  our declare coordinator message is accepted by all nodes
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [43-1] 2020-08-21 08:40:40: pid 31296: LOG:  setting the local node "10.170.0.2:9999 Linux dba-test-vm-pg12-replicaiton-test-03" as watchdog cluster master
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [45-1] 2020-08-21 08:40:40: pid 31296: LOG:  I am the cluster leader node but we do not have enough nodes in cluster
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [45-2] 2020-08-21 08:40:40: pid 31296: DETAIL:  waiting for the quorum to start escalation process
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [13-1] 2020-08-21 08:40:40: pid 31294: LOG:  watchdog process is initialized
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [13-2] 2020-08-21 08:40:40: pid 31294: DETAIL:  watchdog messaging data version: 1.1
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [46-1] 2020-08-21 08:40:40: pid 31296: LOG:  new IPC connection received
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [16-1] 2020-08-21 08:40:40: pid 31294: LOG:  Setting up socket for 0.0.0.0:9999
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [17-1] 2020-08-21 08:40:40: pid 31294: LOG:  Setting up socket for :::9999
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [18-1] 2020-08-21 08:40:40: pid 31294: LOG:  find_primary_node_repeatedly: waiting for finding a primary node
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31296]: [48-1] 2020-08-21 08:40:40: pid 31296: LOG:  new IPC connection received
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31297]: [15-1] 2020-08-21 08:40:40: pid 31297: LOG:  2 watchdog nodes are configured for lifecheck
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31297]: [16-1] 2020-08-21 08:40:40: pid 31297: LOG:  watchdog nodes ID:0 Name:"10.170.0.2:9999 Linux dba-test-vm-pg12-replicaiton-test-03"
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31297]: [16-2] 2020-08-21 08:40:40: pid 31297: DETAIL:  Host:"10.170.0.2" WD Port:9000 pgpool-II port:9999
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31297]: [17-1] 2020-08-21 08:40:40: pid 31297: LOG:  watchdog nodes ID:1 Name:"Not_Set"
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31297]: [17-2] 2020-08-21 08:40:40: pid 31297: DETAIL:  Host:"10.170.0.2" WD Port:9000 pgpool-II port:1533
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [33-1] 2020-08-21 08:40:40: pid 31294: LOG:  find_primary_node: primary node is 0
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [34-1] 2020-08-21 08:40:40: pid 31294: LOG:  find_primary_node: standby node is 1
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [35-1] 2020-08-21 08:40:40: pid 31294: LOG:  pgpool-II successfully started. version 4.1.2 (karasukiboshi)
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [36-1] 2020-08-21 08:40:40: pid 31294: LOG:  node status[0]: 1
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31294]: [37-1] 2020-08-21 08:40:40: pid 31294: LOG:  node status[1]: 2
Aug 21 08:40:40 dba-test-vm-pg12-replicaiton-test-03 pgpool[31333]: [36-1] 2020-08-21 08:40:40: pid 31333: LOG:  PCP process: 31333 started
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31331]: [18-1] 2020-08-21 08:40:41: pid 31331: LOG:  createing watchdog heartbeat receive socket.
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31331]: [18-2] 2020-08-21 08:40:41: pid 31331: DETAIL:  bind receive socket to device: "eth0"
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31331]: [19-1] 2020-08-21 08:40:41: pid 31331: LOG:  set SO_REUSEPORT option to the socket
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31331]: [20-1] 2020-08-21 08:40:41: pid 31331: LOG:  creating watchdog heartbeat receive socket.
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31331]: [20-2] 2020-08-21 08:40:41: pid 31331: DETAIL:  set SO_REUSEPORT
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31332]: [18-1] 2020-08-21 08:40:41: pid 31332: LOG:  creating socket for sending heartbeat
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31332]: [18-2] 2020-08-21 08:40:41: pid 31332: DETAIL:  bind send socket to device: eth0
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31332]: [19-1] 2020-08-21 08:40:41: pid 31332: LOG:  set SO_REUSEPORT option to the socket
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31332]: [20-1] 2020-08-21 08:40:41: pid 31332: LOG:  creating socket for sending heartbeat
Aug 21 08:40:41 dba-test-vm-pg12-replicaiton-test-03 pgpool[31332]: [20-2] 2020-08-21 08:40:41: pid 31332: DETAIL:  set SO_REUSEPORT


确认 pgpool 进程：


连接 pgpool  实例，确认后端数据库：
[root@dba-test-vm-pg12-replicaiton-test-03 run]# psql -h 10.170.0.3 -p 9999 postgres postgres
Password for user postgres:
psql (12.4, server 12.3)
Type "help" for help.

postgres=#
postgres=#
postgres=# show pool_nodes;
 node_id |  hostname  | port | status | lb_weight |  role   | select_cnt | load_balance_node | replication_delay | replication_state | replication_sync_state | last_status_change
---------+------------+------+--------+-----------+---------+------------+-------------------+-------------------+-------------------+------------------------+---------------------
 0       | 10.170.0.2 | 1533 | up     | 0.500000  | primary | 0          | true              | 0                 |                   |                        | 2020-08-21 08:46:00
 1       | 10.170.0.3 | 1533 | up     | 0.500000  | standby | 0          | false             | 0                 |                   |                        | 2020-08-21 08:46:00
(2 rows)


-- 第二个阶段，另外一个服务器上部署 pgpool

yum install pgpool-II-12






