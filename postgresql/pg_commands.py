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
