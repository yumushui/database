#!/usr/bin/env python
# -*- coding:utf-8 -*-

print ('''

--查看数据库大小，不计算索引
select pg_size_pretty(pg_database_size('mydb'));

--查看数据库大小，包含索引
select pg_size_pretty(pg_total_size('mydb'));

--查看表中索引大小
select pg_size_pretty(pg_indexes_size('test_1'));

--查看表大小,不包括索引
select pg_size_pretty(pg_relation_size('test_1'));
       
--or
\dt+ test_1
--查看表大小,包括索引
select pg_size_pretty(pg_total_relation_size('test_1'));

--查看某个模式大小，包括索引。不包括索引可用pg_relation_size
select schemaname,round(sum(pg_total_relation_size(schemaname||'.'||tablename))/1024/1024) "Mb" 
from pg_tables where schemaname='mysch' group by 1;

--查看表空间大小
select pg_size_pretty(pg_tablespace_size('pg_global'));

--查看表对应的数据文件
select pg_relation_filepath('test_1');

--切换log日志文件到下一个
select pg_rotate_logfile();

--切换日志
select pg_switch_xlog();
checkpoint


      ''')
print('''




## postgresql 常用的管理命令

###  查看系统信息的常用命令

查看pg数据库实例版本
select version();

查看pg数据库启动时间：
select pg_postmaster_start_time();

查看最后load配置文件的时间：
select pg_conf_load_time();

使用 pg_ctl reload 改变配置的装载时间：
pg_ctl reload

psql
> select pg_conf_load_time();

显示数据库时区：
show tiemzone;

注意，有的数据库时区不是当前操作系统的时区，这是在数据库中看到的时间，就和操作系统看到的时间不一样：
date

psql
> show timezone
> select now();

查看当前实例中有那些数据库：
psql -l

psql
> \l

查看当前用户名：
select user;
select current_user;

查看 session 用户：
select session_user;

注意，通常情况下 session_user 和 user 是相同的，但当用命令 set role 改变用户角色后，这两者就不一样了：
set role u01;
select session_user;
select user;

查询当前连接的数据库名称：
select current_catalog, current_database();

注意，使用 current_catalog 和 current_database（） 都显示当前连接的数据库，这两者功能完全相同，只不过 catalog 是SQL标准中的用语。

查询当前 session 所在的客户端的 IP地址和端口：
select inet_client_addr(), inet_client_port();

查看当前 session 的后端服务进程的 pid ：
select pg_backend_pid();

通过操作系统命令查看此后台进程：
ps -ef | grep {pid_number} | grep -v grep

查看当前的一些参数配置情况：
show shared_buffers;

select current_setting('shared_buffers');

select name,value from pg_settings where name like '%shared%';

修改当前 session 的参数配置：
set maintenance_work_mem to '128MB';

SELECT set_config('maintenance_work_mem', '128MB', false);

查看当前正在写的 WAL 文件：
select pg_xlogfile_name(pg_current_xlog_location());

查看当前 WAL 的 buffer 还有多少字节没有写入到磁盘中：
select pg_xlog_location_diff( pg_current_xlog_insert_location(), pg_current_xlog_location() );

select pg_xlog_location_diff( pg_current_xlog_insert_location(), pg_current_xlog_location() );

查看数据库实例是否在做基础备份：
select pg_is_in_backup(), pg_backup_start_time();

查看当前数据库是 hot standby 状态，还是正常状态：
select pg_is_in_recovery();

如果上面结果返回为真 t,则说明该数据库处于 hot standby状态。

查看数据库大小，库名为 osdba:
select pg_database_size('osdba'), pg_size_pretty( pg_database_size('osdba') );

注意，如果数据库中有很多表，使用上面的命令会比较慢，也可能对当前系统产生不利的影响。pg_size_pretty() 函数会把数据以 MB、GB等格式显示出来，这样更直观。

查看表大小的命令：
select pg_size_pretty( pg_relation_size('ipdb2') );

select pg_size_pretty( pg_total_relation_size('ipdb2') );

上面的结果中，pg_relation_size() 近计算表大小，不包括索引大小，而 pg_total_relation_size（）则把表上的索引也计算了。

查看表上所有索引的大小：
select pg_size_pretty( pg_indexes_size('ipdb2') );

注意，pg_idnexes_size() 函数的参数名是一个表对应的 oid (输入表名会自动转换成oid)，而不是索引的名称。

查看表空间的大小：
select pg_size_pretty( pg_tablespace_size('pg_global') );

select pg_size_pretty( pg_tablespace_size('pg_default') );

查看表对应的数据文件：
select pg_relation_filepath('test01');

###  系统维护常用命令

修改 pg 的配置文件 postgresql.conf 后，让修改神效的方法有两种：

方法一： 在操作系统使用工具命令

pg_ctl reload -d {pg_data_dir}

方法二： 在 psql 中使用SQL命令

>  select pg_reload_conf();

注意，如果需要重启数据库服务才能生效的配置项，修改后用上面的方法不能生效，需要重启实例才行。

切换 log 日志到下一个的命令：

select pg_rotate_logfile();

切换 WAL 日志文件命令：

select pg_switch_xlog();

手工产生一次 checkpoint，命令为：

checkpoint;

取消一个正在执行的SQL方法

有两个函数可以完成这个功能：
pg_cancel_backend(pid): 取消一个正在执行的 SQL。
pg_terminate_backend(pid): 终止一个后台服务进程，同时释放此后台进程的资源。
这两者的区别是： pg_cancel_backend() 函数实际是给正在执行的SQL任务配置一个取消标志，正在执行的任务在合适的时候检测到此标志后，会主动退出；
但如果这个任务没有主动检测到这个标志，则该任务就无法正常退出，这时需要 pg_terminate_backend 命令来中止SQL的执行。

通常的做法是，先查询 pg_stat_activity，找出长时间运行的 SQL，命令为；
select pid,usename,query_start,query from pg_stat_activity;

然后使用 pg_cacel_backend() 取消这个 SQL，如果这个取消不了，再使用  pg_terminage_backend()命令执行。

select pg_cancel_backend(567);

select pg_terminate_backend(567);

select pid,usename,query_start,query from pg_stat_activity;




###  PostgreSQL 查询所有数据库大小，表大小，索引大小，以及表空间大小

1. 查询数据库大小

-- 查询单个数据库大小
select pg_size_pretty(pg_database_size('postgres')) as size;
 
-- 查询所有数据库大小
select datname, pg_size_pretty (pg_database_size(datname)) AS size from pg_database; 

2. 查询表大小

-- 查询单个表大小
select pg_size_pretty(pg_relation_size('mytab')) as size;
 
-- 查询所有表大小
select relname, pg_size_pretty(pg_relation_size(relid)) as size from pg_stat_user_tables;
 
-- 查询单个表的总大小，包括该表的索引大小
select pg_size_pretty(pg_total_relation_size('tab')) as size;
 
-- 查询所有表的总大小，包括其索引大小
select relname, pg_size_pretty(pg_total_relation_size(relid)) as size from pg_stat_user_tables;

3. 查询索引大小（暂时没有一次性查询所有索引大小的函数）

-- 查询单个索引大小
select pg_size_pretty(pg_relation_size('myindex')) as size;

4. 查询表空间大小

-- 查询单个表空间大小
select pg_size_pretty(pg_tablespace_size('pg_default')) as size;
 
-- 查询所有表空间大小
select spcname, pg_size_pretty(pg_tablespace_size(spcname)) as size from pg_tablespace;
-- 或
select spcname, pg_size_pretty(pg_tablespace_size(oid)) as size from pg_tablespace;

     
     ''')


##  postgresql partition tables

query the define partition table info  -  the (talbe_name) should be define:
```
SELECT
    nmsp_parent.nspname AS parent_schema ,
    parent.relname AS parent ,
    nmsp_child.nspname AS child ,
    child.relname AS child_schema
FROM
    pg_inherits JOIN pg_class parent
        ON pg_inherits.inhparent = parent.oid JOIN pg_class child
        ON pg_inherits.inhrelid = child.oid JOIN pg_namespace nmsp_parent
        ON nmsp_parent.oid = parent.relnamespace JOIN pg_namespace nmsp_child
        ON nmsp_child.oid = child.relnamespace
WHERE
    parent.relname = 'table_name';
```

the query result like 
```
accounting@pgm-j6cdomxz53134an2132790.pg.rds.aliyuncs.com:1921=>SELECT
    nmsp_parent.nspname AS parent_schema ,
    parent.relname AS parent ,
    nmsp_child.nspname AS child ,
    child.relname AS child_schema
FROM
    pg_inherits JOIN pg_class parent
        ON pg_inherits.inhparent = parent.oid JOIN pg_class child
        ON pg_inherits.inhrelid = child.oid JOIN pg_namespace nmsp_parent
        ON nmsp_parent.oid = parent.relnamespace JOIN pg_namespace nmsp_child
        ON nmsp_child.oid = child.relnamespace
WHERE
    parent.relname = 'accounting_journal';
 parent_schema |       parent       | child  |         child_schema
---------------+--------------------+--------+------------------------------
 public        | accounting_journal | public | accounting_journal_p20201001
 public        | accounting_journal | public | accounting_journal_p20201002
 public        | accounting_journal | public | accounting_journal_p20201003
 public        | accounting_journal | public | accounting_journal_p20201004
 public        | accounting_journal | public | accounting_journal_p20201005
 public        | accounting_journal | public | accounting_journal_p20201006
```

PostgreSQL 12 psql客户端支持快捷键dP列出分区表。

```
create table p (id int , info text, crt_time timestamp) partition by hash (id);    
create table p0 partition of p  for values WITH (MODULUS 4, REMAINDER 0);    
create table p1 partition of p  for values WITH (MODULUS 4, REMAINDER 1);    
create table p2 partition of p  for values WITH (MODULUS 4, REMAINDER 2);   
create table p3 partition of p  for values WITH (MODULUS 4, REMAINDER 3);    
insert into p select generate_series (1,100000000) , md5(random()::text), now();  
  
  
postgres=# \dP+  
                           List of partitioned relations  
 Schema | Name |  Owner   |       Type        | On table | Total size | Description   
--------+------+----------+-------------------+----------+------------+-------------  
 public | p    | postgres | partitioned table |          | 7303 MB    |   
(1 row)  
```

###  query the partition table number

```
SELECT
    nspname ,
    relname ,
    COUNT(*) AS partition_num
FROM
    pg_class c ,
    pg_namespace n ,
    pg_inherits i
WHERE
    c.oid = i.inhparent
    AND c.relnamespace = n.oid
    AND c.relhassubclass
    AND c.relkind = 'r'
GROUP BY 1,2 ORDER BY partition_num DESC;
```


PostgreSQL 数据库实例只读锁定（readonly） - 硬锁定，软锁定，解锁

https://github.com/digoal/blog/blob/master/201901/20190130_02.md

PostgreSQL DBA最常用SQL

https://github.com/digoal/blog/blob/master/202005/20200509_02.md


PostgreSQL 数据库开发规范

https://github.com/digoal/blog/blob/master/201609/20160926_01.md

阿里云RDS PostgreSQL 12 + pgpool 的读写分离配置

https://github.com/digoal/blog/blob/master/202002/20200229_01.md

PostgreSQL HAProxy ha & load balance 代理

https://github.com/digoal/blog/blob/master/201911/20191101_01.md

PostgreSQL 会话ssl状态查询 - pg_stat_ssl , sslinfo

https://github.com/digoal/blog/blob/master/201909/20190908_02.md

如何修改PostgreSQL分区表分区范围 - detach attach - 拆分、合并、非平衡分区表、深度不一致分区表

https://github.com/digoal/blog/blob/master/201906/20190621_02.md

PostgreSQL 生成对象DDL语句 - ddlx 插件 - "show create"

https://github.com/digoal/blog/blob/master/201906/20190610_01.md


删除用户风险大，试试锁定用户

https://github.com/digoal/blog/blob/master/201905/20190508_01.md

PostgreSQL 三种心跳(keepalive)指标的应用 - 时间戳、redo(wal)位点、事务号

https://github.com/digoal/blog/blob/master/201905/20190503_04.md

PostgreSQL 12 preview - partitions pruned at plan time. 原生分区表性能提升23.5倍，已与pg_pathman持平。

https://github.com/digoal/blog/blob/master/201903/20190331_01.md

PostgreSQL 12 preview - REINDEX CONCURRENTLY

https://github.com/digoal/blog/blob/master/201903/20190330_02.md

PostgreSQL PITR 任意时间点恢复过程中如何手工得到recovery需要的下一个WAL文件名 - 默认情况下restore_command自动获取

https://github.com/digoal/blog/blob/master/201903/20190305_01.md

PostgreSQL 知识图谱 (xmind, png格式)

https://github.com/digoal/blog/blob/master/201903/20190303_01.md

PostgreSQL 持续稳定使用的小技巧 - 最佳实践、规约、规范

https://github.com/digoal/blog/blob/master/201902/20190219_02.md

PostgreSQL 普通表在线转换为分区表 - online exchange to partition table

https://github.com/digoal/blog/blob/master/201901/20190131_01.md

PostgreSQL pg_rewind，时间线修复，脑裂修复，flashback - 从库开启读写后，回退为只读从库。异步主从发生角色切换后，主库rewind为新主库的从库

https://github.com/digoal/blog/blob/master/201901/20190128_02.md

PostgreSQL HA patroni

https://github.com/digoal/blog/blob/master/201901/20190105_02.md






