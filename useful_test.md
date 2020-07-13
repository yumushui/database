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



### MySQL High Availability 02 : GTID + Binlog Server At Booking & Facebook

### MySQL High Availability 03 : GTID + 增强半同步 及多IDC架构 及 使用架构

### MySQL High Availability 04 : Mysql innodb cluster



