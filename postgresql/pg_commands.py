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
PostgreSQL 查询所有数据库大小，表大小，索引大小，以及表空间大小

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
