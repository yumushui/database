# Database

## Postgresql

### digoal  github pg blog
https://github.com/digoal/blog/blob/master/README.md
https://github.com/digoal/pgsql_admin_script


### Francs 
Francs's blog  Postgresql中文网
https://postgres.fun/

### Vonng  冯若航
https://github.com/Vonng/pg/blob/master/test/README.md   Postgresql监控实战
https://github.com/Vonng/pg   
https://github.com/Vonng/pg/blob/master/admin/migration-without-downtime.md   
https://github.com/Vonng/pg/blob/master/admin/backup-overview.md
https://github.com/Vonng/pg/blob/master/admin/replication-delay.md
https://github.com/Vonng/pg/blob/master/admin/alert-overview.md
http://vonng.com/      personal blog

### 2nd Quadrant PostgreSQL
BDR   https://www.2ndquadrant.com/en/resources/postgres-bdr-2ndquadrant/
PostgreSQL with High Availability    https://www.2ndquadrant.com/en/resources/highly-available-postgresql-clusters/
Kubernetes Operators for HA PostgreSQL & BDR   https://www.2ndquadrant.com/en/resources/kubernetes-operators-for-highly-available-postgresql-and-bdr/
Postgres Cloud Manager  https://www.2ndquadrant.com/en/resources/postgres-cloud-manager/  
Postgres Installer  https://www.2ndquadrant.com/en/resources/postgresql-installer-2ndquadrant/
2ndQPostgres  https://www.2ndquadrant.com/en/resources/2ndqpostgres/
pglogical    https://www.2ndquadrant.com/en/resources/pglogical/
Barman   https://www.2ndquadrant.com/en/resources/barman/
repmgr   https://www.2ndquadrant.com/en/resources/repmgr/
OmniDB   https://www.2ndquadrant.com/en/resources/omnidb/
SQL Firewall  https://www.2ndquadrant.com/en/resources/postgresql-security-firewall/
Postgres-XL  https://www.2ndquadrant.com/en/resources/postgres-xl/


### NTT OSS Center DBMS Development and Support Team
Tokyo, Japan
https://github.com/ossc-db
pg_rman  https://github.com/ossc-db/pg_rman


### postgresql high avralibale 
https://github.com/digoal/PostgreSQL_HA_with_primary_standby_2vip

###  Zalando SE 
The org page fro Zalando, Europe's leading online fashion platform. Visit opensource.zalando.com for project stats.
https://tech.zalando.com

patroni
https://github.com/zalando/patroni
https://postgres.fun/20200529182600.html
https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling


## MySQL

### MySQL High Availability 01 : MHA
https://www.cnblogs.com/keerya/p/7883766.html
```
MHA 适用场景：
    版本<5.5 ,异步复制   一主多从环境
    基于传统复制的高可用
解决问题：
    尽最大能力做数据补偿
    最大努力实现RPO，有RTO概念支持
存在的问题：
    GTID 模型强依赖 binlog server
    对 5.7 后的binlog 不能识别，对并行复制支持不好
    服务IP切换依赖自行编写的脚本，也可以和DNS结合使用
    运维上需要做SSH信任，切换判断，现在项目基本无维护

优点：
    mysql <= 5.5 , mysql高可用王者
    可以利用原始主库上 binlog ，slave上的 relay log 进行数据补偿
    为了绝对保证RPO，需要把 binlog 放到共享存上
缺点：
    运行中，不再管理从库是不是复制
    如果使用共享存储binlog，会把幽灵事务补偿到从库上
    对于 mysql 5.7 的 binlog 解析报错
```


### MySQL High Availability 02 : GTID + Binlog Server At Booking & Facebook

```
多个IDC机房，一个IDC机房 有一个master主，一个slave从； 其他几个IDC中，只有一个slave从库，binlog server； 每个IDC实例上，都需要有 monitor  和 consul
    从master主到 binlog server之间，使用 binlog半同步，保证数据安全，一般至少两个，保证 RPO
    master主和多个slave从之间，采用异步复制，保障性能，通过监控延时，保证 RTO
    Monitor 多个IDC中 Monitor 组成分布式监控，把健康的mysql注册到 consul中，同时对于从库复制延时情况，也同步到consul中
    Consul 配置中心，对外提供健康的 mysql服务

特性：
    基于 mysql 5.6 + GTID
    binlog server 使用 半同步 （是否允许半同步退化）
缺点：
    存在幻读问题
    mysql 5.6 本身半同步 ack 确认在 dump_thread 中， dump_thread 存在IO瓶颈问题
```

### MySQL High Availability 03 : GTID + 增强半同步 及多IDC架构 及 使用架构
Xenon GTID + 增强半同步
```
第三代增强半同步复制
    这代产品对于 mysql版本有强依赖：  mysql 5.7 以后版本
    代表产品：  mysql replication manager  /  github  orcheastrator
    国内青云开源的：  Xenon (mysql plus)

mysql 5.7 增强点：
    1 增强半同步，主从为了增强半同步都独立出来线程
    2  主库binlog group commit
    3  从库： 并行复制，基于事务的并行复制， sql_thread: writeset 从库上的并行提升

	特点：
    每个节点都有一个独立的 agent
    利用 raft构建集群，利用 gtid做index选主
    leader 对外提供写服务
    follow 节点可以对外提供读服务
    适合结合 docker 工作
```
Orchestrator + proxySQL + mutil-IDC
```
第三代  增强复制高可用
mysql层面参数配置
    set global slave_net_timeout = 5;
    change master to master_connect_retry=1 , master_retry_count = 86400;

	Orchestrator 通过tcp分别于 master和slave进行连接
1 Orchestrator 监控M，当为M挂掉
2 获取 slave上的 show slave status 输出，依据 io_thread 状态对 master 进一步判断
3  因为基于 GTID + 增强半同步， master_auto_position = 1 的特性，两个 slave间，非常好处理数据一致性

特点：
    利用 mysql自身特性，复制并行度高， dump_thread 读取 binlog 可并行，半同步 ack 线程独立，实现 binlog group  commit , writeset 等
    基本不用担心复制延迟，主库能并行的，从库也能并行
    强依赖于增强半同步（依赖多个slave），利用半同步保证RPO， TRO依赖于复制延迟
缺点：
    增强半同步中存在幽灵事务 （local commit）
    增强半同步运维上可能出现影响

这代产品的特点：
     简单，方便运维
     充分利用mysql自身的特性，并行复制，增强半同步
     扩展灵活，都可以支持调用外部脚本

```
### MySQL High Availability 04 : Mysql innodb cluster

```
MySQL 原生高可用

利用 MGR mysql原生高可用特点
    mysql router 默认包含在mysql发行包中，mysql route 可以部署多个
    mysql router 提供基于端口号的读写分离
    mysql shell 支持快速构建 MGR
    开源社区可以利用 proxysql 替代 mysql router

优点
    原生高可用，官方推荐 single master，但实际建议使用 multi master模式，单点写入
    推荐 proxysql + MGR 结合，性能为王的环境： mysql route
缺点
    使用上有一些限制
     运维方面有难度，特别对于 multi master 模式，需要控制写入及并发（更新丢失）

小结
    从第二代高可用开始后，整个高可用技术中出现：  配置中心consul ， DNS ， proxy 或 lvs类技术 等综合应用
    从原来的单集群运维扩展到：  数据库托管服务， RDS平台
    从实现上看，更偏重于自我定制高可用平台

```

mysql 高可用选择建议
| | mysql版本 | 可用软件 | 存在问题|
|--|--|--|--|
|第一代|mysql 5.5|MHA|传统复制，主库存在没有把日志传输到从库上的风险，数据补偿不能处理mysql本身的幽灵事件|
|第二代|mysql 5.6|FaceBook开源的mysql， Maxscale|利用 binlog server 和主库做半同步，保证数据安全，binlog server没有太好的开源解决方案|
|第三代|mysql 5.7|Xenon,mysql replication manager,Github orchestrator|增强半同步，基本完美|
|第四代|mysql 8.0mysql 5.7|mysql-router, proxysql, mgr|原生高可用解决方案|

现在选择高可用推荐： 第三代，第四代架构中选择


