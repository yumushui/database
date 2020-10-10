# PostgreSQL explain

在关系型数据库中，一般都会使用explain来显示SQL语句的执行计划。只是不同的数据库，这些命令格式，会有一些区别。

PostgreSQL中执行计划的格式为：

```
EXPLAIN — show the execution plan of a statement

EXPLAIN [ ( option [, ...] ) ] statement
EXPLAIN [ ANALYZE ] [ VERBOSE ] statement

where option can be one of:

    ANALYZE [ boolean ]
    VERBOSE [ boolean ]
    COSTS [ boolean ]
    SETTINGS [ boolean ]
    BUFFERS [ boolean ]
    TIMING [ boolean ]
    SUMMARY [ boolean ]
    FORMAT { TEXT | XML | JSON | YAML }

```

+ ANALYZE
analyze 选项通过实际执行SQL语句来得到执行计划，因为SQL语句实际会被执行，所以可以看到执行计划每一步花了多少时间，以及每一步实际返回的行数。
```
由于 analyze 会实际执行SQL语句，如果一个SQL语句是插入、更新、删除，或者 create table as 语句，这些语句会实际修改数据库。
为了在查看执行计划时，不影响实际的数据库，可以将这些语句放在一个事务中，执行完后回滚事务，例如：

BEGIN;
EXPLAIN ANALYZE 
ROLLBACK;
```

+ VERBOSE
verbose 用于显示执行计划的附加信息。这些附加信息有：计划树中每个节点输出的各个列，如果触发器被触发，还会显示触发器的名称。该选项默认为 false。

+ COSTS
costs 显示每个执行计划节点的启动成本和总成本，以及估计行数和每行宽度。该选项默认为 true。

+ BUFFERS
buffers 显示与缓冲区使用有关的信息，该参数只能与 analyze 一起使用。显示缓冲区信息包括 共享块、本地块、临时块 读和写的块数。
共享块、本地块、临时块分别包含表和索引、临时表和临时索引、排序和物化计划中使用的数据块。
上层节点显示的快数，包含其所有下层子节点使用的块数。该选项默认为 false。

+ FORMAT
format可以指定执行计划的输出格式，默认值为 text格式，其他格式包含与text相同的内容，结果更容易被其他程序解析。


##  pg explain 输出结果解释

一个简单查询语句的执行计划
```
=>explain select * from wf_task;
                            QUERY PLAN
------------------------------------------------------------------
 Seq Scan on wf_task  (cost=0.00..20471.50 rows=246250 width=715)
(1 row)
```

结果中 “ Seq Scan on wf_task” 表示 顺序扫描表 wf_task， 顺序扫描表就是全表扫描，即从头到尾地扫描表。
后面 (cost=0.00..20471.50 rows=246250 width=715) 可以分为三部分：
cost=0.00..20471.50 ，cost后有两个数字，中间用..隔开，第一个数字 0.00 表示启动成本，也就是返回第一行需要多少cost值；第二个数字 20471.50 表示返回所有数据的成本。
rows=246250 ，表示会返回 246250 行。
width=715 ，表示每行平均宽度为 715 字节。

```
什么是成本 cost？

成本cost是描述一个SQL执行的代价是多少，默认情况下，不同的操作其成本cost值不同：

顺序扫描一个数据块，cost值定为 1；
随机扫描一个数据块，cost值定为 4；
处理一个数据行的cpu，cost值定为 0.01；
处理一个索引行的cpu，cost值定为 0.005；
每一个操作符的cpu，cost值定为 0.0025；

PostgreSQL根据上面的操作类型，智能地计算出一个SQL的执行代价，虽然计算不是很精确，但多数情况下够用了。

更复杂的执行计划如下：

=>explain SELECT wo.node_operator AS operator, COUNT(1) AS total
airboard_ng_api->         FROM wf_task wf
airboard_ng_api->             LEFT JOIN wf_task_operation wo
airboard_ng_api->             ON wf.id = wo.wf_task_id
airboard_ng_api->                 AND wf.current_node = wo.node_code
airboard_ng_api->         WHERE wf.is_completed = false
airboard_ng_api->             AND wf.wf_code = 'WF_ONBOARDING_KYC'
airboard_ng_api->             AND wo.node_type = 'USER'
airboard_ng_api->         GROUP BY wo.node_operator;
                                             QUERY PLAN
----------------------------------------------------------------------------------------------------
 HashAggregate  (cost=75304.47..75304.66 rows=19 width=9)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=22836.71..75189.79 rows=22934 width=9)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Seq Scan on wf_task_operation wo  (cost=0.00..39497.55 rows=503536 width=24)
               Filter: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=21087.12..21087.12 rows=87972 width=13)
               ->  Seq Scan on wf_task wf  (cost=0.00..21087.12 rows=87972 width=13)
                     Filter: ((NOT is_completed) AND ((wf_code)::text = 'WF_ONBOARDING_KYC'::text))
(9 rows)


```

##  pg explain 使用示例

pg explain 的输出格式，默认为 text，也可以调整为其他格式。
```
airboard_ng_api@rm-j6cd7ue3ndfsaby7a.pg.rds.aliyuncs.com:3433=>explain select * from wf_task;
                            QUERY PLAN
------------------------------------------------------------------
 Seq Scan on wf_task  (cost=0.00..20471.50 rows=246250 width=715)
(1 row)

airboard_ng_api@rm-j6cd7ue3ndfsaby7a.pg.rds.aliyuncs.com:3433=>explain (format json) select * from wf_task;
            QUERY PLAN
-----------------------------------
 [                                +
   {                              +
     "Plan": {                    +
       "Node Type": "Seq Scan",   +
       "Relation Name": "wf_task",+
       "Alias": "wf_task",        +
       "Startup Cost": 0.00,      +
       "Total Cost": 20471.50,    +
       "Plan Rows": 246250,       +
       "Plan Width": 715          +
     }                            +
   }                              +
 ]
(1 row)

airboard_ng_api@rm-j6cd7ue3ndfsaby7a.pg.rds.aliyuncs.com:3433=>explain (format xml) select * from wf_task;
                        QUERY PLAN
----------------------------------------------------------
 <explain xmlns="http://www.postgresql.org/2009/explain">+
   <Query>                                               +
     <Plan>                                              +
       <Node-Type>Seq Scan</Node-Type>                   +
       <Relation-Name>wf_task</Relation-Name>            +
       <Alias>wf_task</Alias>                            +
       <Startup-Cost>0.00</Startup-Cost>                 +
       <Total-Cost>20471.50</Total-Cost>                 +
       <Plan-Rows>246250</Plan-Rows>                     +
       <Plan-Width>715</Plan-Width>                      +
     </Plan>                                             +
   </Query>                                              +
 </explain>
(1 row)

airboard_ng_api@rm-j6cd7ue3ndfsaby7a.pg.rds.aliyuncs.com:3433=>explain (format yaml) select * from wf_task;
          QUERY PLAN
------------------------------
 - Plan:                     +
     Node Type: "Seq Scan"   +
     Relation Name: "wf_task"+
     Alias: "wf_task"        +
     Startup Cost: 0.00      +
     Total Cost: 20471.50    +
     Plan Rows: 246250       +
     Plan Width: 715
(1 row)

```

查看更详细的执行计划
```
-- 查看执行计划和实际执行情况
explain analyze select * from wf_task;

expalin (analyze true) select * from wf_task;

-- 只看查询路径，不看cost
explain （costs false）select * from wf_task;

-- 查看实际执行计划和缓冲区命中情况
explain (analyze true, buffers true) select * from wf_task;

-- 查看 create as 的执行计划
explain create table test_04 as select * from test_03 limit 10000;

-- 查看 DML 语句的执行计划
explain insert into test_04 select * from test_03 limit 10000;

explain delete from test_04;

explain update test_04 set note='abcdefghi';

```

##  pg 执行计划常用方法

### 全表扫描 Seq Scan
全表扫描在 PostgreSQL中被称为顺序扫描 seq scan,全表扫描就是把表中所有数据从头到尾顺序读一遍，然后从中找出符合条件的数据块。

全表扫描在explain执行计划中，用 Seq Scan 表示
```
=>explain select * from wf_task;
                            QUERY PLAN
------------------------------------------------------------------
 Seq Scan on wf_task  (cost=0.00..20471.50 rows=246250 width=715)
(1 row)
```

### 索引扫描 Index Scan
索引通常是为了加快数据的查询而添加的。索引扫描，就是在索引中找出需要的数据行的物理位置，然后再到表的数据块中，把相应的数据读出来的过程。

索引扫描在explain执行计划中，用 Index Scan 表示

```
=>explain select * from wf_task where id=10;
                                  QUERY PLAN
------------------------------------------------------------------------------
 Index Scan using wf_task_pkey on wf_task  (cost=0.42..8.44 rows=1 width=715)
   Index Cond: (id = 10)
(2 rows)
```


### 位图扫描 Bitmap Index Scan
位图扫描，也是走索引的一种方式。其方法是，扫描索引，把满足条件的行或数据块，在内存中建立一个位图，扫描完索引后，在根据位图列表的数据文件，把相应的数据读出来。
如果走了两个索引，可以把两个索引形成的位图进行 and 或 or 计算，合并成一个位图，再到数据文件中，把数据读出来。

当执行计划的结果很多时，会执行这种扫描，如 非等值查询，in子句 或 有多个条件都可以走不同的索引时。

```
=>explain select * from wf_task where id>250000;
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Index Scan using wf_task_pkey on wf_task  (cost=0.42..730.64 rows=5775 width=715)
   Index Cond: (id > 250000)
(2 rows)

-- 如果条件是非等值查询，通常会 先进行 Bitmap Index Scan 位图索引查询先在索引中找到符合条件的行，然后在内存只能够建立位图，之后再到表中查询，也就是看到的 Bitmap Heap Scan。


=>explain select * from wf_task where id in (2, 4, 6, 8);
                                  QUERY PLAN
-------------------------------------------------------------------------------
 Index Scan using wf_task_pkey on wf_task  (cost=0.42..21.83 rows=4 width=715)
   Index Cond: (id = ANY ('{2,4,6,8}'::integer[]))
(2 rows)

-- 如果条件是in子句，通常也会先位图索引扫描，建立内存中的位图，然后再到表中查询。

=>explain select * from wf_task where id>255000 or id<10;
                                     QUERY PLAN
-------------------------------------------------------------------------------------
 Bitmap Heap Scan on wf_task  (cost=36.78..4578.48 rows=1492 width=715)
   Recheck Cond: ((id > 255000) OR (id < 10))
   ->  BitmapOr  (cost=36.78..36.78 rows=1492 width=0)
         ->  Bitmap Index Scan on wf_task_pkey  (cost=0.00..31.55 rows=1484 width=0)
               Index Cond: (id > 255000)
         ->  Bitmap Index Scan on wf_task_pkey  (cost=0.00..4.48 rows=8 width=0)
               Index Cond: (id < 10)
(7 rows)

-- 有两个条件都可以走索引，会有两个位图索引扫描，然后在 BitmapOr 进行 or 合并，最后再走 Bitmap Heap Scan 到表中查询数据。

```

### 条件过滤 Filter
条件过滤，一般就是在 where条件上加的过滤条件，当扫描数据行时，会找出满足条件的数据行。

条件过滤在explain执行计划中，显示为 Filter。

```
=>explain select * from wf_task where wf_code like 'abdc%' limit 3;
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.42..2.27 rows=3 width=832)
   ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task  (cost=0.42..8.44 rows=13 width=832)
         Index Cond: (((wf_code)::text >= 'abdc'::text) AND ((wf_code)::text < 'abdd'::text))
         Filter: ((wf_code)::text ~~ 'abdc%'::text)
(4 rows)

-- 如果条件列上有索引，可能会走索引，不走过滤

=>explain select * from wf_task where id> 10000 limit 3;
                               QUERY PLAN
------------------------------------------------------------------------
 Limit  (cost=0.00..0.41 rows=3 width=832)
   ->  Seq Scan on wf_task  (cost=0.00..64958.19 rows=474853 width=832)
         Filter: (id > 10000)
(3 rows)

=>explain select * from wf_task where id< 10000 limit 3;
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Limit  (cost=0.42..1.24 rows=3 width=832)
   ->  Index Scan using wf_task_pkey on wf_task  (cost=0.42..2404.65 rows=8842 width=832)
         Index Cond: (id < 10000)
(3 rows)
```

### 嵌套循环连接 Nestloop Join
嵌套循环连接 NestLoop Join，是两个表在做连接时候，最朴素的一种连接方式。
在嵌套循环中，内表被外表驱动，外表返回的每一行，都需要在内表中检索到它对应匹配的行，因此整体查询结果集不能太大（>10000不适合），要把返回子集较少的表，作为外表，而且在内表的连接字段上，要有索引，否则会很慢。

执行过程为：确定一个外表驱动表 outer table，另一个表为内表 inner table，驱动表中的每一行与inner表中相应的积累 join类似一个嵌套的循环。
适用于驱动表比较小（<10000）而且inner表有有效的访问方法（index）。需要注意的时候，join的顺序很重要，驱动表的记录数一定要少，这样返回结果集的时间是最快的。

### 哈希表连接 Hash Join

优化器中，使用两个表中较小的表，并利用连接列在内存中建立散列表，然后扫描较大的表并探测散列表，找出与散列表匹配的行。

这种方式比较适合较小的表，可以完全放在内存中的情况，这样总成本就是访问两个表的成本之和。
但是如果表很大，不能完全放入内存中，优化器会将它们分割成若干不同的分区，把不能放入内存的部分写入磁盘临时段，此时要有较大的临时段，以便尽量提高IO的性能。

```
=>explain analyze select count(*) from wf_task wf, wf_task_operation wo where wf.id = wo.wf_task_id AND wf.current_node = wo.node_code ;
                                                                 QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------
 Aggregate  (cost=156688.62..156688.64 rows=1 width=0) (actual time=1591.767..1591.767 rows=1 loops=1)
   ->  Hash Join  (cost=73366.38..156677.35 rows=4510 width=0) (actual time=400.954..1588.086 rows=43187 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Seq Scan on wf_task_operation wo  (cost=0.00..37262.15 rows=1762115 width=12) (actual time=0.004..301.223 rows=1814085 loops=1)
         ->  Hash  (cost=63748.95..63748.95 rows=483695 width=9) (actual time=400.823..400.823 rows=472255 loops=1)
               Buckets: 16384  Batches: 8  Memory Usage: 2408kB
               ->  Seq Scan on wf_task wf  (cost=0.00..63748.95 rows=483695 width=9) (actual time=0.003..288.519 rows=544671 loops=1)
 Planning time: 0.291 ms
 Execution time: 1592.321 ms
(9 rows)

-- 这是一个 hash join的例子， wf_task表比 wf_task_operation 表下，所以在较小的表 wf_task 上建立散列表，然后扫描较大的表 wf_task_operation 并探测散列表，找出与散列表匹配的行。

```

### 合并表连接 Merge Join

通常情况下，散列连接 hash join 的效果，比合并连接 merge join 好.但如果源数据上有索引，或者结果已经排过序了，在执行排序合并的时候就不需要在排序，这时合并排序的性能会由于散列连接的性能。

```
=>explain analyze select count(*) from wf_task wf, wf_task_operation wo where wf.id = wo.wf_task_id ;
                                                                                           QUERY PLAN

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
-
 Aggregate  (cost=107264.57..107264.58 rows=1 width=0) (actual time=1134.260..1134.260 rows=1 loops=1)
   ->  Merge Join  (cost=3.75..102957.36 rows=1722881 width=0) (actual time=0.048..1005.156 rows=1814093 loops=1)
         Merge Cond: (wf.id = wo.wf_task_id)
         ->  Index Only Scan using wf_task_pkey on wf_task wf  (cost=0.42..17647.85 rows=483695 width=4) (actual time=0.028..84.255 rows=544675 loops=1)
               Heap Fetches: 1967
         ->  Index Only Scan using wf_task_operation_wf_task_id_node_code on wf_task_operation wo  (cost=0.43..62895.64 rows=1762115 width=4) (actual time=0.015..558.621 rows=1814105 loops=1)
               Heap Fetches: 381998
 Planning time: 0.244 ms
 Execution time: 1134.306 ms
(9 rows)

-- 这个查询中，两个表的 id 和 wf_task_id 上都已经有索引了，且从索引扫描的数据，是已经排过序的了，可以直接走 Merge join。



=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
airboard_ng_api->         FROM wf_task wf, wf_task_operation wo
airboard_ng_api->         WHERE wf.id = wo.wf_task_id
airboard_ng_api->                 AND wf.current_node = wo.node_code and wf.is_completed = false
airboard_ng_api->             AND wf.wf_code = 'WF_ONBOARDING_KYC'
airboard_ng_api->             AND wo.node_type = 'USER'
airboard_ng_api->         GROUP BY wo.node_operator;
                                                                                 QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=82543.42..82543.44 rows=2 width=10) (actual time=35091.682..35091.693 rows=54 loops=1)
   Group Key: wo.node_operator
   ->  Merge Join  (cost=54187.72..82543.41 rows=2 width=10) (actual time=498.574..35085.840 rows=2452 loops=1)
         Merge Cond: ((wf.current_node)::text = (wo.node_code)::text)
         Join Filter: (wf.id = wo.wf_task_id)
         Rows Removed by Join Filter: 141674108
         ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task wf  (cost=0.42..111712.65 rows=3512 width=9) (actual time=0.024..50.774 rows=34111 loops=1)
               Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Rows Removed by Filter: 4340
         ->  Materialize  (cost=54187.30..54784.36 rows=119413 width=22) (actual time=427.377..8898.423 rows=141686321 loops=1)
               ->  Sort  (cost=54187.30..54485.83 rows=119413 width=22) (actual time=427.374..456.288 rows=125728 loops=1)
                     Sort Key: wo.node_code
                     Sort Method: external merge  Disk: 3136kB
                     ->  Seq Scan on wf_task_operation wo  (cost=0.00..41667.44 rows=119413 width=22) (actual time=0.005..285.481 rows=125728 loops=1)
                           Filter: ((node_type)::text = 'USER'::text)
                           Rows Removed by Filter: 1688327
 Planning time: 0.356 ms
 Execution time: 35094.063 ms
(19 rows)

-- 这个查询中， wo.node_code 列并没有索引，所以需要在先进行 sort排序，然后再走 合并连接，这样性能就比较慢了。
Sort Key: wo.node_code  执行计划中的这个排序键，可以看到是对表 wf_task_operation 的 node_code 列进行排序的。

```


##  与执行计划有关的配置

ENABLE_*  参数

COST基准值 参数

基因查询优化参数

其他执行计划配置项


##  统计信息的收集

PgStat 子进程是 PostgreSQL中专门收集统计信息的子进程。收集的统计信息，主要用于查询优化时的代价估算，这些统计信息对于数据库的监控和性能分析也有很大的帮助。
表和索引的行数、块数等统计信息，记录在系统表 pg_class中； 其他的统计信息，主要收集在系统表 pg_statistics 中。


统计信息收集器的配置项

SQL执行的统计信息输出

手工收集统计信息


