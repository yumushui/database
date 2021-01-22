
# postgresql 序列 sequence

https://www.postgresql.org/docs/12/functions-sequence.html

## 一、简介

序列对象 sequence（也叫序列生成器）就是用CREATE SEQUENCE 创建的特殊的单行表。一个序列对象通常用于为行或者表生成唯一的标识符。

##  二、创建序列

###  方法一：直接在表中指定字段类型为serial 类型

```
create table tab_seq_test (
id serial,
name text);

dba_test_gcp_db@127.0.0.1:5432=>select version();
                                         version
------------------------------------------------------------------------------------------
 PostgreSQL 12.4 on x86_64-pc-linux-gnu, compiled by Debian clang version 10.0.1 , 64-bit
(1 row)
dba_test_gcp_db@127.0.0.1:5432=>create table tab_seq_test (
dba_test_gcp_db(> id serial,
dba_test_gcp_db(> name text);
CREATE TABLE
```

###  方法二：先创建序列名称，然后在新建的表中列属性指定序列就可以了，该列需int 类型

创建序列的语法：
```
CREATE [ TEMPORARY | TEMP ] SEQUENCE name [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ START [ WITH ] start ] [ CACHE cache ] [ [ NO ] CYCLE ]
    [ OWNED BY { table.column | NONE } ]
```

实例：
```
create sequence tab_seq_test2_id_seq increment by 1 minvalue 1 no maxvalue start with 1;   

create table tab_seq_test2 (
id int4 not null default nextval('tab_seq_test2_id_seq'),
name text);


dba_test_gcp_db@127.0.0.1:5432=>create sequence tab_seq_test2_id_seq increment by 1 minvalue 1 no maxvalue start with 1;
CREATE SEQUENCE
dba_test_gcp_db@127.0.0.1:5432=>create table tab_seq_test2 (
dba_test_gcp_db(> id int4 not null default nextval('tab_seq_test2_id_seq'),
dba_test_gcp_db(> name text);
CREATE TABLE
```

##  三、查看序列

在表中查看序列
```
dba_test_gcp_db@127.0.0.1:5432=>\d tab_seq_test
                            Table "public.tab_seq_test"
 Column |  Type   | Collation | Nullable |                 Default
--------+---------+-----------+----------+------------------------------------------
 id     | integer |           | not null | nextval('tab_seq_test_id_seq'::regclass)
 name   | text    |           |          |

dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>\d tab_seq_test2
                            Table "public.tab_seq_test2"
 Column |  Type   | Collation | Nullable |                  Default
--------+---------+-----------+----------+-------------------------------------------
 id     | integer |           | not null | nextval('tab_seq_test2_id_seq'::regclass)
 name   | text    |           |          |

dba_test_gcp_db@127.0.0.1:5432=>
```

查看序列属性
```
dba_test_gcp_db@127.0.0.1:5432=>\ds
                          List of relations
 Schema |           Name           |   Type   |         Owner
--------+--------------------------+----------+-----------------------
 public | tab_overtime_test_id_seq | sequence | dba_test_gcp_db_admin
 public | tab_seq_test2_id_seq     | sequence | dba_test_gcp_db_admin
 public | tab_seq_test_id_seq      | sequence | dba_test_gcp_db_admin
(3 rows)

dba_test_gcp_db@127.0.0.1:5432=>\d+ tab_seq_test_id_seq
                Sequence "public.tab_seq_test_id_seq"
  Type   | Start | Minimum |  Maximum   | Increment | Cycles? | Cache
---------+-------+---------+------------+-----------+---------+-------
 integer |     1 |       1 | 2147483647 |         1 | no      |     1
Owned by: public.tab_seq_test.id

dba_test_gcp_db@127.0.0.1:5432=>\d+ tab_seq_test2_id_seq
                    Sequence "public.tab_seq_test2_id_seq"
  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache
--------+-------+---------+---------------------+-----------+---------+-------
 bigint |     1 |       1 | 9223372036854775807 |         1 | no      |     1

dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test_id_seq;
 last_value | log_cnt | is_called
------------+---------+-----------
          1 |       0 | f
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test2_id_seq;
 last_value | log_cnt | is_called
------------+---------+-----------
          1 |       0 | f
(1 row)

```

##  四、序列应用

###  4.1 在INSERT 命令中使用序列

```
insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Abc');     
insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Def');

dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Abc');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Def');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  1 | Abc
  2 | Def
(2 rows)
```

###  4.2 数据迁移后更新序列

```
david=# truncate tbl_xulie;
TRUNCATE TABLE
david=# 
david=# insert into tbl_xulie values (nextval('tbl_xulie_id_seq'), 'Sandy');
INSERT 0 1
david=# insert into tbl_xulie values (nextval('tbl_xulie_id_seq'), 'David');
INSERT 0 1
david=# insert into tbl_xulie values (nextval('tbl_xulie_id_seq'), 'Eagle');
INSERT 0 1
david=# insert into tbl_xulie values (nextval('tbl_xulie_id_seq'), 'Miles');

dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (10, 'Def');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Aa');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Bb');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Cc');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Dd');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Ee');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Ff');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Gg');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Hh');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Jj');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Kk');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  1 | Abc
  2 | Def
 10 | Def
  3 | Aa
  4 | Bb
  5 | Cc
  6 | Dd
  7 | Ee
  8 | Ff
  9 | Gg
 10 | Hh
 11 | Jj
 12 | Kk
(13 rows)

dba_test_gcp_db@127.0.0.1:5432=>truncate table tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Ll');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Mm');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Nn');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
 13 | Ll
 14 | Mm
 15 | Nn
(3 rows)

dba_test_gcp_db@127.0.0.1:5432=>\copy tab_seq_test to '/tmp/tab_seq_test.sql';
COPY 3
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>truncate tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>alter sequence tab_seq_test_id_seq restart with 100;
ALTER SEQUENCE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
      15
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
     100
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
     101
(1 row)
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
(0 rows)

dba_test_gcp_db@127.0.0.1:5432=>begin;
BEGIN
dba_test_gcp_db@127.0.0.1:5432=>\copy tab_seq_test from '/tmp/tab_seq_test.sql';
COPY 3
dba_test_gcp_db@127.0.0.1:5432=>select setval('tab_seq_test_id_seq', max(id)) from tab_seq_test;
 setval
--------
     15
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>end;
COMMIT
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Oo');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
 13 | Ll
 14 | Mm
 15 | Nn
 16 | Oo
(4 rows)

dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
      17
(1 row)
dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
      17
(1 row)
dba_test_gcp_db@127.0.0.1:5432=>select lastval();
 lastval
---------
      17
(1 row)
```


##  五、序列函数

下面序列函数，为我们从序列对象中获取最新的序列值提供了简单和并发读取安全的方法。

|函数	|返回类型	|描述 |
|--|--|--|
|nextval(regclass)	|bigint	|递增序列对象到它的下一个数值并且返回该值。这个动作是自动完成的。即使多个会话并发运行nextval，每个进程也会安全地收到一个唯一的序列值。 |
|currval(regclass)	|bigint	|在当前会话中返回最近一次nextval抓到的该序列的数值。(如果在本会话中从未在该序列上调用过 nextval，那么会报告一个错误。)请注意因为此函数返回一个会话范围的数值，而且也能给出一个可预计的结果，因此可以用于判断其它会话是否执行过nextval。 |
|lastval()	|bigint	|返回当前会话里最近一次nextval返回的数值。这个函数等效于currval，只是它不用序列名为参数，它抓取当前会话里面最近一次nextval使用的序列。如果当前会话还没有调用过nextval，那么调用lastval将会报错。 |
|setval(regclass, bigint)	|bigint	|重置序列对象的计数器数值。设置序列的last_value字段为指定数值并且将其is_called字段设置为true，表示下一次nextval将在返回数值之前递增该序列。 |
|setval(regclass, bigint, boolean)	|bigint	|重置序列对象的计数器数值。功能等同于上面的setval函数，只是is_called可以设置为true或false。如果将其设置为false，那么下一次nextval将返回该数值，随后的nextval才开始递增该序列。 |


###  5.1 查看下一个序列值

```
dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
      18
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
      19
(1 row)
```


###  5.2 查看序列最近使用值

```
dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
      20
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
      20
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
      20
(1 row)
```


###  5.3 重置序列

+ 方法一：使用序列函数



  - a. setval(regclass, bigint)

```
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
 13 | Ll
 14 | Mm
 15 | Nn
 16 | Oo
(4 rows)

dba_test_gcp_db@127.0.0.1:5432=>truncate tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select setval('tab_seq_test_id_seq', 1);
 setval
--------
      1
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Pp');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Qq');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  2 | Pp
  3 | Qq
(2 rows)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
       3
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
       4
(1 row)
```

  - b. setval(regclass, bigint, boolean)

  -  b.1 setval(regclass, bigint, true)

```
dba_test_gcp_db@127.0.0.1:5432=>truncate tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>select setval('tab_seq_test_id_seq', 1, true);
 setval
--------
      1
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Rr');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Ss');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  2 | Rr
  3 | Ss
(2 rows)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
       3
(1 row)
```
效果同a. setval(regclass, bigint)

  -  b.2 setval(regclass, bigint, false)

```
dba_test_gcp_db@127.0.0.1:5432=>truncate tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>select setval('tab_seq_test_id_seq', 1, false);
 setval
--------
      1
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Tt');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values (nextval('tab_seq_test_id_seq'), 'Uu');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  1 | Tt
  2 | Uu
(2 rows)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
       2
(1 row)

```

+ 方法二：修改序列

修改序列的语法：

```
ALTER SEQUENCE name [ INCREMENT [ BY ] increment ]
    [ MINVALUE minvalue | NO MINVALUE ] [ MAXVALUE maxvalue | NO MAXVALUE ]
    [ START [ WITH ] start ]
    [ RESTART [ [ WITH ] restart ] ]
    [ CACHE cache ] [ [ NO ] CYCLE ]
    [ OWNED BY { table.column | NONE } ]
ALTER SEQUENCE name OWNER TO new_owner
ALTER SEQUENCE name RENAME TO new_name
ALTER SEQUENCE name SET SCHEMA new_schema
```

实例：

```
dba_test_gcp_db@127.0.0.1:5432=>truncate table tab_seq_test;
TRUNCATE TABLE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>alter sequence tab_seq_test_id_seq restart with 0;
ERROR:  RESTART value (0) cannot be less than MINVALUE (1)
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>alter sequence tab_seq_test_id_seq restart with 1;
ALTER SEQUENCE
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values(nextval('tab_seq_test_id_seq'::regclass), 'Aa');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>insert into tab_seq_test values(nextval('tab_seq_test_id_seq'::regclass), 'Bb');
INSERT 0 1
dba_test_gcp_db@127.0.0.1:5432=>
dba_test_gcp_db@127.0.0.1:5432=>select * from tab_seq_test;
 id | name
----+------
  1 | Aa
  2 | Bb
(2 rows)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
       2
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select nextval('tab_seq_test_id_seq');
 nextval
---------
       3
(1 row)

dba_test_gcp_db@127.0.0.1:5432=>select currval('tab_seq_test_id_seq');
 currval
---------
       3
(1 row)

```

##  六、删除序列

语法：
```
DROP SEQUENCE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```
当有表字段使用到PG序列时，不能直接删除。

```
david=# drop sequence tbl_xulie2_id_seq;
ERROR:  cannot drop sequence tbl_xulie2_id_seq because other objects depend on it
DETAIL:  default for table tbl_xulie2 column id depends on sequence tbl_xulie2_id_seq
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
david=# drop table tbl_xulie2;
DROP TABLE
david=# drop sequence tbl_xulie2_id_seq;
DROP SEQUENCE
david=# 
```

说明：对于序列是由建表时指定serial 创建的，删除该表的同时，对应的序列也会被删除。




##  七、参考资料

PostgreSQL官方文档：https://www.postgresql.org/docs/12/functions-sequence.html
PostgreSQL: 数据迁移之序列问题：http://francs3.blog.163.com/blog/static/40576727201281351925766/
PostgreSQL简介： https://www.postgresqltutorial.com/postgresql-sequences/


# sequence in postgres prod env

```
https://www.postgresql.org/docs/9.4/infoschema-sequences.html
https://www.postgresql.org/docs/9.5/information-schema.html

https://www.postgresql.org/docs/12/view-pg-sequences.html
```

##  源端：

```
kbank=> select version();
      version
-------------------
 PostgreSQL 9.4.19
(1 row)
kbank=> select min(payment_seq), max(payment_seq), count(payment_seq) from kbankv2.disbursement;
 min | max  | count
-----+------+-------
   1 | 6743 |  6742
(1 row)
kbank=> \d kbankv2.disbursement_payment_seq_seq
               Sequence "kbankv2.disbursement_payment_seq_seq"
  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache
--------+-------+---------+---------------------+-----------+---------+-------
 bigint |     1 |       1 | 9223372036854775807 |         1 | no      |     1
Owned by: kbankv2.disbursement.payment_seq

kbank=> select * from kbankv2.disbursement_payment_seq_seq;
        sequence_name         | last_value | start_value | increment_by |      max_value      | min_value | cache_value | log_cnt | is_cycled | is_called
------------------------------+------------+-------------+--------------+---------------------+-----------+-------------+---------+-----------+-----------
 disbursement_payment_seq_seq |       6770 |           1 |            1 | 9223372036854775807 |         1 |           1 |       0 | f         | t
(1 row)

kbank=> \d  information_schema.sequences
                              View "information_schema.sequences"
         Column          |                Type                | Collation | Nullable | Default
-------------------------+------------------------------------+-----------+----------+---------
 sequence_catalog        | information_schema.sql_identifier  |           |          |
 sequence_schema         | information_schema.sql_identifier  |           |          |
 sequence_name           | information_schema.sql_identifier  |           |          |
 data_type               | information_schema.character_data  |           |          |
 numeric_precision       | information_schema.cardinal_number |           |          |
 numeric_precision_radix | information_schema.cardinal_number |           |          |
 numeric_scale           | information_schema.cardinal_number |           |          |
 start_value             | information_schema.character_data  |           |          |
 minimum_value           | information_schema.character_data  |           |          |
 maximum_value           | information_schema.character_data  |           |          |
 increment               | information_schema.character_data  |           |          |
 cycle_option            | information_schema.yes_or_no       |           |          |


select currval('kbankv2.disbursement_payment_seq_seq');

kbank=> select * from information_schema.sequences;
 sequence_catalog | sequence_schema |        sequence_name         | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value | minimum_value |    maximum_value    | increment | cycle_option
------------------+-----------------+------------------------------+-----------+-------------------+-------------------------+---------------+-------------+---------------+--------------------+-----------+--------------
 kbank            | kbankv2         | disbursement_payment_seq_seq | bigint    |                64 |                       2 |             0 | 1           | 1             | 9223372036854775807 | 1         | NO
(1 row)



```


##  目标端：

```
kbank=> select version();
     version
-----------------
 PostgreSQL 12.4
(1 row)
kbank=> select min(payment_seq), max(payment_seq), count(payment_seq) from disbursement;
 min | max  | count
-----+------+-------
   1 | 6743 |  6742
(1 row)

kbank=> \d disbursement_payment_seq_seq
                Sequence "public.disbursement_payment_seq_seq"
  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache
--------+-------+---------+---------------------+-----------+---------+-------
 bigint |  6743 |       1 | 9223372036854775807 |         1 | no      |     1

kbank=> \d pg_sequences
              View "pg_catalog.pg_sequences"
    Column     |  Type   | Collation | Nullable | Default
---------------+---------+-----------+----------+---------
 schemaname    | name    |           |          |
 sequencename  | name    |           |          |
 sequenceowner | name    |           |          |
 data_type     | regtype |           |          |
 start_value   | bigint  |           |          |
 min_value     | bigint  |           |          |
 max_value     | bigint  |           |          |
 increment_by  | bigint  |           |          |
 cycle         | boolean |           |          |
 cache_size    | bigint  |           |          |
 last_value    | bigint  |           |          |

 kbank=> select * from pg_catalog.pg_sequences;
 schemaname |         sequencename         | sequenceowner | data_type | start_value | min_value |      max_value      | increment_by | cycle | cache_size | last_value
------------+------------------------------+---------------+-----------+-------------+-----------+---------------------+--------------+-------+------------+------------
 public     | disbursement_payment_seq_seq | kbank_admin   | bigint    |        6743 |         1 | 9223372036854775807 |            1 | f     |          1 |
(1 row)
```

调整 sequence

```
postgres=> \c kbank
psql (12.5 (Ubuntu 12.5-1.pgdg16.04+1), server 12.2)
You are now connected to database "kbank" as user "airwallex".
kbank=>
kbank=> select min(payment_seq), max(payment_seq), count(payment_seq) from disbursement;
 min | max  | count
-----+------+-------
   1 | 6743 |  6742
(1 row)

kbank=>
kbank=> \d pg_sequences
              View "pg_catalog.pg_sequences"
    Column     |  Type   | Collation | Nullable | Default
---------------+---------+-----------+----------+---------
 schemaname    | name    |           |          |
 sequencename  | name    |           |          |
 sequenceowner | name    |           |          |
 data_type     | regtype |           |          |
 start_value   | bigint  |           |          |
 min_value     | bigint  |           |          |
 max_value     | bigint  |           |          |
 increment_by  | bigint  |           |          |
 cycle         | boolean |           |          |
 cache_size    | bigint  |           |          |
 last_value    | bigint  |           |          |

kbank=>
kbank=> select * from pg_catalog.pg_sequences;
 schemaname |         sequencename         | sequenceowner | data_type | start_value | min_value |      max_value      | increment_by | cycle | cache_size | last_value
------------+------------------------------+---------------+-----------+-------------+-----------+---------------------+--------------+-------+------------+------------
 public     | disbursement_payment_seq_seq | kbank_admin   | bigint    |        6743 |         1 | 9223372036854775807 |            1 | f     |          1 |
(1 row)

kbank=>
kbank=> select nextval('disbursement_payment_seq_seq');
 nextval
---------
    6743
(1 row)

kbank=> select currval('disbursement_payment_seq_seq');
 currval
---------
    6743
(1 row)

kbank=> select * from pg_catalog.pg_sequences;
 schemaname |         sequencename         | sequenceowner | data_type | start_value | min_value |      max_value      | increment_by | cycle | cache_size | last_value
------------+------------------------------+---------------+-----------+-------------+-----------+---------------------+--------------+-------+------------+------------
 public     | disbursement_payment_seq_seq | kbank_admin   | bigint    |        6743 |         1 | 9223372036854775807 |            1 | f     |          1 |       6743
(1 row)

kbank=> select nextval('disbursement_payment_seq_seq');
 nextval
---------
    6744
(1 row)

kbank=> select * from pg_catalog.pg_sequences;
 schemaname |         sequencename         | sequenceowner | data_type | start_value | min_value |      max_value      | increment_by | cycle | cache_size | last_value
------------+------------------------------+---------------+-----------+-------------+-----------+---------------------+--------------+-------+------------+------------
 public     | disbursement_payment_seq_seq | kbank_admin   | bigint    |        6743 |         1 | 9223372036854775807 |            1 | f     |          1 |       6744
(1 row)

kbank=> select currval('disbursement_payment_seq_seq');
 currval
---------
    6744
(1 row)
```


确认序列状态
```
kbank=> \ds
                       List of relations
 Schema |             Name             |   Type   |    Owner
--------+------------------------------+----------+-------------
 public | disbursement_payment_seq_seq | sequence | kbank_admin
(1 row)

kbank=> \d disbursement_payment_seq_seq
                Sequence "public.disbursement_payment_seq_seq"
  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache
--------+-------+---------+---------------------+-----------+---------+-------
 bigint |  6743 |       1 | 9223372036854775807 |         1 | no      |     1

-- pg 12
kbank=> select * from public.disbursement_payment_seq_seq;
 last_value | log_cnt | is_called
------------+---------+-----------
       6744 |      31 | t
(1 row)

-- pg 9.4 
kbank=> select * from kbankv2.disbursement_payment_seq_seq;
        sequence_name         | last_value | start_value | increment_by |      max_value      | min_value | cache_value | log_cnt | is_cycled | is_called
------------------------------+------------+-------------+--------------+---------------------+-----------+-------------+---------+-----------+-----------
 disbursement_payment_seq_seq |       6770 |           1 |            1 | 9223372036854775807 |         1 |           1 |       0 | f         | t
(1 row)


-- 序列说明
不论那个 postgresql 版本，都可以通过 \ds 查看默认用户下，有权限都序列； 可以通过 \d {sequnce_name}  查看序列的基本信息； 通过 select * from {schema.sequnce_name}; 查看序列的 last_value.

注意序列的 last_value 是序列目前使用过的，最后一个值，这个值已经在序列中被使用了；

所以对于使用序列迁移过的 pg 实例，要有如下确认：

select min(payment_seq), max(payment_seq), count(payment_seq) from disbursement;

select last_value from kbankv2.disbursement_payment_seq_seq;

要注意迁移目标端的序列最后使用的值 last_value，需要大于或等于 max(payment_seq) 值。不能小于 max(payment_seq) 值，不然目标端的序列，就会有重复的情况。

增大序列 last_value的方法是：
select nextval("sequence_name");

查看序列当前使用最大值的方法是：
seelct currval("sequence_name");
```

阿里云 DTS 对于 PostgreSQL 的序列同步支持说明
```
https://help.aliyun.com/document_detail/26624.html?spm=a2c4g.11186623.6.644.7f066906LKs8gZ
```

DTS对 PG 的迁移限制

+ 一个数据迁移任务只能对一个数据库进行数据迁移，如果有多个数据库需要迁移，则需要为每个数据库创建数据迁移任务。
+ 待迁移的数据库名称中间不能包含短划线（-），例如dts-testdata。
+ 如果迁移过程中源库发生了主备切换，DTS的增量数据迁移无法实现断点续传。
+ 由于源库的主备节点可能存在同步延迟导致数据不一致，执行数据迁移时请使用源库的主节点作为迁移的数据源.

说明 为避免数据迁移对业务的影响，请在业务低峰期执行数据迁移，您还可以根据源库的读写压力情况调整迁移速率，详情请参见调整全量迁移速率。

+ 增量数据迁移阶段仅支持DML操作（INSERT、DELETE、UPDATE）的同步。
  
说明 如果需要实现DDL操作的同步，请在配置迁移任务前，在源库中创建触发器和函数来捕获DDL信息，详情请参见通过触发器和函数实现PostgreSQL的DDL增量迁移。

+ DTS的校验对象为数据内容，暂不支持Sequence等元数据的校验，您需要自行校验。
 
由于业务切换到目标端后，新写入的Sequence不会按照源库的Sequence最大值作为初始值去递增，您需要在业务切换前，在源库中查询对应Sequence的最大值，然后在目标库中将其作为对应Sequence的初始值。查询源库Sequence值的相关命令如下：

```
do language plpgsql $$
declare
  nsp name;
  rel name;
  val int8;
begin
  for nsp,rel in select nspname,relname from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S'
  loop
    execute format($_$select last_value from %I.%I$_$, nsp, rel) into val;
    raise notice '%',
    format($_$select setval('%I.%I'::regclass, %s);$_$, nsp, rel, val+1);
  end loop;
end;
$$;
```

一个实际执行的例子为：
```
accounting@rm-j6c6hildj3lqlk46h.pg.rds.aliyuncs.com:3433=>do language plpgsql $$
accounting$> declare
accounting$>   nsp name;
accounting$>   rel name;
accounting$>   val int8;
accounting$> begin
accounting$>   for nsp,rel in select nspname,relname from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S'
accounting$>   loop
accounting$>     execute format($_$select last_value from %I.%I$_$, nsp, rel) into val;
accounting$>     raise notice '%',
accounting$>     format($_$select setval('%I.%I'::regclass, %s);$_$, nsp, rel, val+1);
accounting$>   end loop;
accounting$> end;
accounting$> $$;
NOTICE:  select setval('public.seq_accounting_reblance_id'::regclass, 2);
NOTICE:  select setval('public.seq_accounting_manual_adjust_id'::regclass, 2);
DO
accounting@rm-j6c6hildj3lqlk46h.pg.rds.aliyuncs.com:3433=>
```


查询sequence的 last_value
```
select nspname,relname from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S';

select 'select last_value from ' || nspname || '.' ||  relname  || ';' from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S';

\ds

select * from sequence_name;

```

## Get the sequence last value

In pg 9.4 and pg 12, the start value are not the same. In pg 9.4, the start value is 1. In pg 12, the start vaule is the same as the last value.

get the sequece last value

```
do language plpgsql $$
declare
  nsp name;
  rel name;
  val int8;
begin
  for nsp,rel in select nspname,relname from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S'
  loop
    execute format($_$select last_value from %I.%I$_$, nsp, rel) into val;
    raise notice '%',
    format($_$ '%I.%I', %s ;$_$, nsp, rel, val);
  end loop;
end;
$$;
```

reset the sequence last value

```
do language plpgsql $$
declare
  nsp name;
  rel name;
  val int8;
begin
  for nsp,rel in select nspname,relname from pg_class t2 , pg_namespace t3 where t2.relnamespace=t3.oid and t2.relkind='S'
  loop
    execute format($_$select last_value from %I.%I$_$, nsp, rel) into val;
    raise notice '%',
    format($_$select setval('%I.%I'::regclass, %s);$_$, nsp, rel, val+1);
  end loop;
end;
$$;
```



