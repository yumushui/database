'''
PG 之 高可用、工具及架构设计

# Pooling 连接池

Pooling  工具

PgBouncer
    - 低资源消耗
    - 会话保持
    - 多个后端数据库
    - 多种模式
        Session Pooling
        Transaction Pooling
        Statement Pooling

Pgpool-II
    - 连接池模式
    - 复制管理
    - 读写分离
    - 负载均衡
    - 并行查询

Pooling 架构

PgBouncer + Pgpool-II

VIP/CNAME
PGBouncer  PGBouncder PGBouncer
pgpool   pgpool    pgpool
pg1      pg1       pg1


# Replication

物理复制
    - 流复制支持
    - 多从库复制
    - 级连复制
    - 延时复制
    - 同步复制 vs 异步复制
    - Hot Standby
    - Point In Time Recovery
    - Pg_rewind
    - pg_receivexlog

PG1 - 流复制（单向全量、高效） - PG2

逻辑复制
    - Slony
    - Bucardo
    - pglogical
        更好的性能
        同步 vs 异步复制
        延时复制
        冲突管理
        行过滤
        字段过滤
        DML语句过滤
        不同的用户，权限控制

PG1 - 逻辑复制（双向按需、多粒度） - PG2

Replication Management Tools  复制管理工具

Barman   - 备份恢复管理器
    Parallel Copy for Backup and Recovery  备份和恢复的并行拷贝
    Incremental Backup and Recovery   增量备份与恢复
    WAL Files Compression    日志文件压缩
    Remote Recovery    远程恢复
    Cooperration with Standby servers   和standby servers的合作
    Zero data loss backups    零数据丢失的备份


WAL-E     日志管理器
continue archiving of PostgreSQL WAL files and base backups  持续获取WAL日志和基础备份
    AWS S3
    Azure Blob Store
    Google Storage
    Swift
    File System

repmgr  从节点管理器

App server
VIP
Primary
   - Replication - local Standby （Repmgrd check standby, Check & write Primary）
   - Replication - Remote Standby (Repmgrd check standby, Check & write Primary)


walctl  日志管理器

Master
Archive （接收主库）
Clone  Clone Clone  Clone


# HA Architecture   高可用架构

Pacemaker + corosync

node1  - Heatbeat - node2
Fencedisk

心跳网络断开，集群发生脑裂；
集群仲裁，结果是 node2 存活（quorate）；
node2 将 node1 注册到 Fencedisk 上的 key 清理掉；
node1 上的 watchdog 检测到自己的 key 不见络；
于是 node1 自己 panic (ipmitool power rest)
    - reboot -f
    - sysrq + b ，释放资源
node2 启动资源组，继续服务。


Patroni + ETCD (Consul, ZK)

HA proxy
Patroni  Patroni  Patroni
PG       PG       PG
etcd(Consul, ZK)

Etcd 

Http Server
Raft
WAL
Entry
Snapshot   Store
'''

