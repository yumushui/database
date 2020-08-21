
# PgBouncer

lightweight connection pooler for PostgreSQL

https://www.pgbouncer.org/

## 1 PgBouncer function

PgBouncer 是为了 PostgreSQL 数据库提供的i 个轻量级链接池工具，作用如下：
1 应用程序直接与数据库链接，每次都会消耗较多资源，PgBouncer 后端与PostgreSQL链接不变，前端与业务程序交互
2 允许前端创建多个连接，把前端的连接聚合到适量的数据库上。
3 能对客户端连接进行限制，预防过多或恶意的连接请求。

PgBouncer 是轻量级的连接池，主要体现在：
1 PgBouncer使用 libevent 进行 socket通信，这种通信方式效率很高。
2 PgBouncer是使用C语言编写，实现得很精巧，每个连接仅消耗 2KB 的内存。

PgBouncer官网
'''
http://www.pgbouncer.org/
'''

PgBouncer安装介质
'''
http://www.pgbouncer.org/downloads/

'''

PgBouncer官方文档
'''
Features
http://www.pgbouncer.org/features.html

Tutorials
http://www.pgbouncer.org/community.html

github
https://github.com/pgbouncer/pgbouncer
'''

PgBouncer使用参考
'''
数据库连接池中间件-pgbouncer
https://blog.csdn.net/cdnight/article/details/90452248


'''


## 2 PgBouncer concept

PgBouncer 目前支持三种链接池模型：
session ： 会话级连接，在它的连接生命期内，链接池分配给它一个数据库连接。客户端断开时，数据库连接会放回连接池。
transaction : 事务级别连接，当客户端的每个事务结束时，数据连接就会重新释放会连接池中，再次执行一个事务时，需要再从连接池再获得一个连接。
statement ： 每执行完一个SQL语句时，连接就会重新释放回连接池，再次执行一个SQL语句时，需要再次从连接池中获得连接。这种模式意味着在客户端强制 auto commit 模式。

## 3 PgBouncer Install

使用软件管理器安装
-- 在 Redhat Linux  或 CentOS 下，使用yum安装：
yum install pgbouncer

-- 在 Debian 或 Ubuntu 下，使用 apt-get 安装：
sudo apt-get install pgbouncer

使用源码安装
到 http://pgfoundry.org/ 网站上下载 PgBouncer 的源码，然后从源码文件编译安装。
wget  pgbouncer-1.5.4.tar.gz
由于 pgbouncer 是基于 libevent 开发的，需要先安装一些依赖包：
yum -y install libevent

编译安装：
tar -zxvf pgbouncer-1.5.4.tar.gz
cd pgbouncer-1.5.4
./configure
make 
sudo make install

这样默认安装在  /usr/local/bin  目录下

## 4 PgBouncer Config and Usage

### 4.1 简单配置方法
先只简单配置 pgbouncer.ini, 可以尽快入手使用 pgbouncer。后面在详细讲解 pgbouncer 的各个配置项。

源码安装完毕后，在 /usr/local/share/doc/pgbouncer 目录下有一个 pgbouncer.ini 可以作为配置文件模板

如果机器上只有一个PostgreSQL数据库实例，可以把pgboucner的配置文件放到 /etc 目录下。
如果机器上有多个PostgreSQL实例，最好为不同的实例，建立不同的pgbouncer,不同实例的配置文件放到不同的目录下。

例如，将配置文件放到 /home/osdba/pgbouncer 目录下：
cp ///pgbouncer.ini /// PgBouncer.ini

编辑配置文件的内容：
vim PgBouncer.ini

[database]

[PgBouncer]

配置文件中，主要有两部分：
[database] ： 此部分用于配置连接后端数据库，以及后端数据库的连接参数
[pgbouncer] : 此部分配置 pgbouncer 的配置项，包括最多允许用户建立多少个连接，默认连接池建立多少个连接到后端数据库。

### 4.2 启动 PgBouncer

启动 PgBouncer 的命令为：
pgbouncer -d ///pgbouncer.ini

-d 是定义一 daemon 后台的方式运行，命令最后一个参数制定启动配置文件。

实际启动命令：

启动过程的日志文件内容：

使用 psql 连接到 pgbouncer :
psql -p 6432 postgres

### 4.3 停止 PgBouncer 

停止 PgBouncer 最简单的方式，就是kill掉对应进程，进程好在启动时，会写入到一个文件中：
kill `cat ///pgbouncer.pid`

### 4.4 查看连接池信息

pgbouncer提供了一个虚拟数据库 pgbouncer,然后执行一些特殊的命令，显示连接池信息，这个就是 pgbouncer 的 console 控制界面。
psql -p 6432 pgbouncer
show help;

执行 show help; 可以看到所有的帮助命令，所有命令都需要有一个分号结尾。
--  查看客户端连接情况的命令：
show client;

-- 查看连接池的命令
show pools;

### 4.5 PgBouncer的配置文件详解

配置文件是 ini 格式的，主要有两部部分组成，结构为：

[database]
db = ...
[pgbouncer]
...

#### 4.5.1 [database] 部分的配置项
这一部分的配置项比较简单，每行都是 key=value 组成，主要是后端数据库连接串，这个连接串与 libpq 连接函数的连接串相同。
postgres  = host=localhost port=5432 dbname=postgres user=osdba

这几个选项用于指定后端数据连接信息，如果连接串中没有指定 user 和 password，那么将使用客户端连接 pgbouncer时的用户名和密码连接后端数据库，并为每个不同的用户建立一个连接；
如果连接串指定了 user 和 password， pgbouncer将使用这里设置的用户名和密码来连接后端数据库，这样对数据库来说，就只有一个连接了。

除了连接串，还有一个可选的配置参数：
pool_size : 配置连接池大小，如果没有配置，则使用 pgbouncer 部分的 default_pool_size 配置项的值
connect_query : 在连接之前执行一个sql语句，用于探测此连接是否正常。如果执行该语句出错，则选择另外一个连接
client_encoding : 指定客户端的字符集编码
datestyle : 指定日期类型参数
timezone : 指定时区




#### 4.5.2 [pgbouncer] 部分的配置项

pgbouncer部分的配置项很多，可以分为几类：
通用配置项
日志配置项
Console访问配置项
连接健康检查和超时配置项
危险的超时配置项
底层网络配置项

这些配置项的具体说明为

#### 4.5.3 用户密码文件

pgbouncer认证文件的格式如下：
“username1” “password” ...
“username2” “md5abdce12312” ...

此文件是一个文本文件，每行是一个用户。每行必须有两列，每两的内容必须以英文双引号括起来。
这个文件的格式与 pg 8.* 版本中数据目录下的用户密码格式完全一样，如果是 pg 8.* 可以直接使用数据库用户认证文件，或者把文件拷贝过来。
在 pg 9.* 后取消了这个文件，将内容放到了 pg_shadow 中，需要查询这个表的内容，手工生成上面的用户密码文件。命令为：
psql 
select name,passwd from  pg_shadow order by 1;

实际上，在 pgbouncer 的源码包中有一个python脚本 ./etc/mkauth.py 文件，可以从上面的表中，读取数据生成文件，可以查看脚本的内容。



##########################################

-- 连接池  pgbouncer

https://github.com/Vonng/pg

连接池

 pgbouncer安装
 pgbouncer配置文件
 pgbouncer使用方法
 pgpool的应用方式


## 安装
### 生产环境CentOS/RedHat使用yum进行二进制安装

# 检查所有以pg打头的包：
sudo yum list pg*

# 显示所有版本的pgbouncer
yum --showduplicates list pgbouncer

# 移除旧版本的pgbouncer
sudo yum -y remove pgbouncer

# 选择需要安装的版本
sudo yum -y install pgbouncer-1.9.0

# 检查版本
pgbouncer --version


### Mac下直接使用brew安装：

brew install pgbouncer

编译Pgbouncer需要一些依赖：

GNU Make 3.81+
libevent 2.0
pkg-config
(optional) OpenSSL 1.0.1 for TLS support.
(optional) c-ares as alternative to libevent’s evdns.
源码下载地址：https://pgbouncer.github.io/downloads/

$ git clone https://github.com/pgbouncer/pgbouncer.git
$ cd pgbouncer
$ git submodule init
$ git submodule update
$ ./autogen.sh
$ ./configure ...
$ make
$ make install

## 配置
设置目录
```
# run as root, setup directories

mkdir -p /var/log/pgbouncer /var/run/pgbouncer /etc/pgbouncer
chown -R pgbouncer:pgbouncer /var/log/pgbouncer /var/run/pgbouncer /etc/pgbouncer
```

修改配置文件
```
cat > /etc/pgbouncer/pgbouncer.ini <<-EOF
[databases]
putong-payment = 
putong-payment-old = host=10.191.161.35 dbname=putong-payment

[pgbouncer]

logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid

listen_addr = *
listen_port = 6432

auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt

admin_users = postgres
stats_users = stats, postgres

pool_mode = transaction
server_reset_query = 

application_name_add_host = 1
max_client_conn = 20000
default_pool_size = 50

reserve_pool_size = 10
reserve_pool_timeout = 5
max_db_connections = 80

log_connections = 0
log_disconnections = 0

ignore_startup_parameters = extra_float_digits

EOF

chown pgbouncer:pgbouncer /etc/pgbouncer/pgbouncer.ini
chmod 0600 /etc/pgbouncer/pgbouncer.ini
```

用户列表文件
```
cat > /etc/pgbouncer/userlist.txt <<-EOF
"putong" "xxxxx"
"stats" "123456"
EOF

chown pgbouncer:pgbouncer /etc/pgbouncer/userlist.txt
chmod 0600 /etc/pgbouncer/userlist.txt
```

## 启动

以pgbouncer身份启动
```
sudo -iu pgbouncer /usr/bin/pgbouncer -d -R /etc/pgbouncer/pgbouncer.ini
```
这里-d选项代表以守护进程的模式启动，-R表示重启，如果已经有Pgbouncer实例，新的进程会接管老进程。

显示统计信息：
```
psql postgres://stats@tmp:6432/pgbouncer?host=/tmp -c "SHOW STATS;"
```

连接实际数据库：
```
psql postgres://putong@tmp:6432/putong-payment?host=/tmp
```

检查Pgbouncer的CPU使用：
```
top -d1 -bn10 -p `cat /var/run/pgbouncer/pgbouncer.pid` | grep pgbouncer
```

## 监控
监控pgbouncer可以使用prometheus，通过pgbouncer_exporter实现监控。

PostgreSQL的Exporter：https://github.com/wrouesnel/postgres_exporter/releases

Pgbouncer的Exporter：




##########################################
测试 pgbouncer

## 测试 VM 01 
dba-test-vm-pg12-replicaiton-test
10.170.0.2
34.96.181.35

gcloud beta compute ssh --zone "asia-east2-a" "dba-test-vm-pg12-replicaiton-test" --project "airwallex-acquiring-poc"


vim gcp_vm_01.sh

#!/bin/sh
# the host is : dba-test-vm-pg12-replicaiton-test
# 10.170.0.2
# 34.96.181.35

source /Users/feixiang.zhao/My_git/py_virtual_dir/venv37/bin/activate
gcloud beta compute ssh --zone "asia-east2-a" "dba-test-vm-pg12-replicaiton-test" --project "airwallex-acquiring-poc"

## 测试 VM 02
dba-test-vm-pg12-replicaiton-test-03
10.170.0.3
34.96.147.244

gcloud beta compute ssh --zone "asia-east2-a" "dba-test-vm-pg12-replicaiton-test-03" --project "airwallex-acquiring-poc"


vim gcp_vm_03.sh

#!/bin/sh
# the host is : dba-test-vm-pg12-replicaiton-test-03
# 10.170.0.3
# 34.96.147.244

source /Users/feixiang.zhao/My_git/py_virtual_dir/venv37/bin/activate
gcloud beta compute ssh --zone "asia-east2-a" "dba-test-vm-pg12-replicaiton-test-03" --project "airwallex-acquiring-poc"


## pgbouncer 安装

[root@dba-test-vm-pg12-replicaiton-test-03 ~]# /bin/sh pgbouncer_install.sh
info: pgbouncer.service not found, install pgbouncer
info: overwrite /etc/pgbouncer/pgbouncer.ini
info: overwrite /etc/pgbouncer/userlist.txt
info: increase pgbouncer file limit
info: overwrite /etc/systemd/system/pgbouncer.service
info: start pgbouncer.service


[root@dba-test-vm-pg12-replicaiton-test ~]# /bin/sh pgbouncer_install.sh
info: pgbouncer.service not found, install pgbouncer
info: /bin/pgbouncer not found, download from yum
info: overwrite /etc/pgbouncer/pgbouncer.ini
info: overwrite /etc/pgbouncer/userlist.txt
info: increase pgbouncer file limit
info: overwrite /etc/systemd/system/pgbouncer.service
info: start pgbouncer.service

## 配置 database



postgres=# \c gcp_test_db
You are now connected to database "gcp_test_db" as user "postgres".
gcp_test_db=#
gcp_test_db=# \c testplate0
ERROR:  no such database: testplate0
Previous connection kept

如果 pgbouncer 中没有配置过database，直接连接 pgbouncer 会报错


[root@dba-test-vm-pg12-replicaiton-test-03 pgbouncer]# psql -h 127.0.0.1 -p 6432 -U gcp_test_db_admin -d postgres
psql: error: could not connect to server: ERROR:  no such user: gcp_test_db_admin

如果 user list 中没有配置用户，连接也会报错

[root@dba-test-vm-pg12-replicaiton-test-03 pgbouncer]# psql -h 127.0.0.1 -p 6432 -U gcp_test_db_admin -d postgres
psql (12.3)
Type "help" for help.

postgres=# select current_user;
 current_user
--------------
 postgres
(1 row)

postgres=# \l
                                              List of databases
    Name     |       Owner       | Encoding | Collate |   Ctype    |            Access privile
ges
-------------+-------------------+----------+---------+------------+--------------------------
---------------
 gcp_test_db | gcp_test_db_admin | UTF8     | C       | en_US.utf8 | =Tc/gcp_test_db_admin
              +
             |                   |          |         |            | gcp_test_db_admin=CTc/gcp
_test_db_admin
 postgres    | postgres          | UTF8     | C       | en_US.utf8 |
 template0   | postgres          | UTF8     | C       | en_US.utf8 | =c/postgres
              +
             |                   |          |         |            | postgres=CTc/postgres
 template1   | postgres          | UTF8     | C       | en_US.utf8 | =c/postgres
              +
             |                   |          |         |            | postgres=CTc/postgres
(4 rows)

postgres=# \c gcp_test_db
You are now connected to database "gcp_test_db" as user "gcp_test_db_admin".
gcp_test_db=#

添加用户配置后，切换到不同的库，会对应不同的用户



-- 连接管理地址，一般用户连接会报错
# psql -h 127.0.0.1 -p 6432 -U gcp_test_db_admin -d pgbouncer
psql: error: could not connect to server: ERROR:  not allowed

使用指定对管理账号，才能成功
[root@dba-test-vm-pg12-replicaiton-test-03 pgbouncer]# psql -h 127.0.0.1 -p 6432 -U postgres -d pgbouncer
psql (12.3, server 1.14.0/bouncer)
Type "help" for help.

pgbouncer=# \dt
ERROR:  failure
server closed the connection unexpectedly
	This probably means the server terminated abnormally
	before or while processing the request.
The connection to the server was lost. Attempting reset: Succeeded.
psql (12.3, server 1.14.0/bouncer)
pgbouncer=# show help;
NOTICE:  Console usage
DETAIL:
	SHOW HELP|CONFIG|DATABASES|POOLS|CLIENTS|SERVERS|USERS|VERSION
	SHOW FDS|SOCKETS|ACTIVE_SOCKETS|LISTS|MEM
	SHOW DNS_HOSTS|DNS_ZONES
	SHOW STATS|STATS_TOTALS|STATS_AVERAGES|TOTALS
	SET key = arg
	RELOAD
	PAUSE [<db>]
	RESUME [<db>]
	DISABLE <db>
	ENABLE <db>
	RECONNECT [<db>]
	KILL <db>
	SUSPEND
	SHUTDOWN

SHOW

-- 热加载配置文件
pgbouncer=# RELOAD;


-- 问题
pgbouncer  【database】配置中，所有database不能重名，一个业务DB，只有一个用户

如果配置如下：
        [databases]
        postgres = host=10.170.0.2  port=1533 user=postgres dbname=postgres password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db = host=10.170.0.2  port=1533 user=gcp_test_db_admin dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db = host=10.170.0.2  port=1533 user=gcp_test_db_rw dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db = host=10.170.0.2  port=1533 user=gcp_test_db_r dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50

对应可用的结果为：
pgbouncer=# show databases;
    name     |    host    | port |  database   |  force_user   | pool_size | reserve_pool | pool_mode | max_connections | current_connections | paused | disabled
-------------+------------+------+-------------+---------------+-----------+--------------+-----------+-----------------+---------------------+--------+----------
 gcp_test_db | 10.170.0.2 | 1533 | gcp_test_db | gcp_test_db_r |        50 |            5 |        |               0 |                   0 |      0 |        0
 pgbouncer   |            | 6432 | pgbouncer   | pgbouncer     |         2 |            0 | statement |               0 |                   0 |      0 |        0
 postgres    | 10.170.0.2 | 1533 | postgres    | postgres      |        50 |            5 |        |               0 |                   0 |      0 |        0
(3 rows)
配置了三个 dbname 为 gcp_test_db 的选项

必须在 pgbouncer.ini 配置不同的name，才会都生效，但连接的时候也会有问题：
        [databases]
        postgres = host=10.170.0.2  port=1533 user=postgres dbname=postgres password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db_admin = host=10.170.0.2  port=1533 user=gcp_test_db_admin dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db = host=10.170.0.2  port=1533 user=gcp_test_db_rw dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db_r = host=10.170.0.2  port=1533 user=gcp_test_db_r dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
对应可用的结果为：
pgbouncer=# show databases;
       name        |    host    | port |  database   |    force_user     | pool_size | reserve_pool | pool_mode | max_connections | current_connections | paused | disabled
-------------------+------------+------+-------------+-------------------+-----------+--------------+-----------+-----------------+---------------------+--------+----------
 gcp_test_db       | 10.170.0.2 | 1533 | gcp_test_db | gcp_test_db_rw    |        50 |    5 |           |               0 |                   0 |      0 |        0
 gcp_test_db_admin | 10.170.0.2 | 1533 | gcp_test_db | gcp_test_db_admin |        50 |    5 |           |               0 |                   0 |      0 |        0
 gcp_test_db_r     | 10.170.0.2 | 1533 | gcp_test_db | gcp_test_db_r     |        50 |    5 |           |               0 |                   0 |      0 |        0
 pgbouncer         |            | 6432 | pgbouncer   | pgbouncer         |         2 |    0 | statement |               0 |                   0 |      0 |        0
 postgres          | 10.170.0.2 | 1533 | postgres    | postgres          |        50 |    5 |           |               0 |                   1 |      0 |        0
(5 rows)


#####################################

通过以上的测试，对于 pgbouncer 的结论如下；
1 pgbouncer 的使用非常简单，用 yum  安装软件，然后配置两个配置文件， 
  pgbouncer.ini 配置后端 database 信息和前端 pgbouncer 信息；
  userlist.txt 文件中配置访问用户信息，

2 pgbouncer 前端对于应用的用户，首先由两个配置文件决定：
        auth_type = trust
        auth_file = /etc/pgbouncer/userlist.txt
然后在 userlist.txt 文件中配置：
如果这个文件没有配置用户，即使后端数据库中有用户，也是无法连接的；
userlist.txt 中的用户认证方式也有多种，如果是 trust 方式，只会校验业务账号是否存在，与后端pg联通，主要是后端数据库保证的；
如果是 md5 方式，则 userlist.txt 中需要配置 业务账号 和 加密的密码，需要双重验证正常后，才能通过

3 pgbouncer 中后端的数据库，需要配置连接串
        [databases]
        postgres = host=10.170.0.2  port=1533 user=postgres dbname=postgres password=123456 connect_query='SELECT 1' pool_size=50
        gcp_test_db_admin = host=10.170.0.2  port=1533 user=gcp_test_db_admin dbname=gcp_test_db password=123456 connect_query='SELECT 1' pool_size=50
但问题是，database中，每个连接串，都需要有一个名字，这几个名字之间不能重复；
这就造成了，多个database只能用一个 DB的情况，这与直接连接 pg database ，一个DB，可以用多个用户连接有区别；

4 pgbouncer 的配置，可以热加载
如果增加 database，或者调整 database 在 pgbouncer 管理接口中，执行 reload 命令，就可以热加载，这可以解决后端数据库迁移问题。
所谓的热加载，配置修改完毕后，就可以reload生效，新的会话，会直接连接新实例；
但老的会话，依然可以保持，直到断开，对业务来说，会话保持，更友好一些。

5 pgbouncer 只专注于会话连接池工具
其他的 LB负载均衡，高可用，都需要结合其他软件，比如 haproxy ，LVS，DNS等结合实现高可用功能。
不过也胜在 pgbouncer 简单，只需要两个配置文件，可以在很多台服务器上用相同的文件，启动相同的服务，就可以达到完全一样的效果。
这就相当于应用服务器，是无状态的，可以扩展和结合第三方软件实现高可用。






