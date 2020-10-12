# Slow log tuning

##  Slog log
The Slow log is
```
SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code 
WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
GROUP BY wo.node_operator;
```

##  table and data info
The table and data info
```
导出测试库后，确认表状态

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>\dt
               List of relations
 Schema |       Name        | Type  |   Owner
--------+-------------------+-------+-----------
 public | wf_task           | table | airwallex
 public | wf_task_operation | table | airwallex
(2 rows)

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>select count(*) from wf_task;
 count
--------
 545478
(1 row)

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>
dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>select count(*) from wf_task_operation;
  count
---------
 1817246
(1 row)

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>\d+ wf_task
                                                             Table "public.wf_task"
     Column     |           Type           | Collation | Nullable |               Default               | Storage  | Stats target | Description
----------------+--------------------------+-----------+----------+-------------------------------------+----------+--------------+-------------
 id             | integer                  |           | not null | nextval('wf_task_id_seq'::regclass) | plain    |              |
 task_id        | character varying(255)   |           | not null |                                     | extended |              |
 wf_code        | character varying(255)   |           | not null |                                     | extended |              |
 current_node   | character varying(255)   |           |          |                                     | extended |              |
 is_completed   | boolean                  |           | not null |                                     | plain    |              |
 creator        | character varying(255)   |           |          |                                     | extended |              |
 created_at     | timestamp with time zone |           |          |                                     | plain    |              |
 updated_at     | timestamp with time zone |           |          |                                     | plain    |              |
 timer_start_at | timestamp with time zone |           |          |                                     | plain    |              |
 timer_hours    | real                     |           |          |                                     | plain    |              |
 deleted        | boolean                  |           |          | false                               | plain    |              |
 wf_data        | jsonb                    |           |          |                                     | extended |              |
 comments       | json                     |           |          |                                     | extended |              |
 version        | integer                  |           | not null | 0                                   | plain    |              |
Indexes:
    "wf_task_pkey" PRIMARY KEY, btree (id)
    "wf_task_task_id" btree (task_id)
    "wf_task_wf_code_current_node_updated_at" btree (wf_code, current_node, updated_at)

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>
dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>\d+ wf_task_operation
                                                              Table "public.wf_task_operation"
    Column     |            Type             | Collation | Nullable |                    Default                    | Storage  | Stats target | Description
---------------+-----------------------------+-----------+----------+-----------------------------------------------+----------+--------------+-------------
 id            | integer                     |           | not null | nextval('wf_task_operation_id_seq'::regclass) | plain    |              |
 wf_task_id    | integer                     |           | not null |                                               | plain    |              |
 node_code     | character varying(255)      |           | not null |                                               | extended |              |
 node_type     | character varying(255)      |           |          |                                               | extended |              |
 node_operator | character varying(255)      |           |          |                                               | extended |              |
 created_at    | timestamp without time zone |           |          |                                               | plain    |              |
 updated_at    | timestamp without time zone |           |          |                                               | plain    |              |
Indexes:
    "wf_task_operation_pkey" PRIMARY KEY, btree (id)
    "wf_task_operation_wf_task_id_node_code" btree (wf_task_id, node_code)

确认此时的执行计划：

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db->         WHERE wf.is_completed = false
dba_temp_db->             AND wf.wf_code = 'WF_ONBOARDING_KYC'
dba_temp_db->             AND wo.node_type = 'USER'
dba_temp_db->         GROUP BY wo.node_operator;
                                                                                  QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=87141.39..87141.41 rows=2 width=10) (actual time=35856.134..35856.144 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Merge Join  (cost=55011.15..87141.38 rows=2 width=10) (actual time=623.139..35850.690 rows=2522 loops=1)
         Merge Cond: ((wf.current_node)::text = (wo.node_code)::text)
         Join Filter: (wf.id = wo.wf_task_id)
         Rows Removed by Join Filter: 146127202
         ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task wf  (cost=0.42..121258.59 rows=3913 width=9) (actual time=0.068..196.593 rows=34231 loops=1)
               Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Rows Removed by Filter: 4340
         ->  Materialize  (cost=54136.85..54777.43 rows=128116 width=22) (actual time=423.709..9284.598 rows=146139485 loops=1)
               ->  Sort  (cost=54136.85..54457.14 rows=128116 width=22) (actual time=423.706..451.295 rows=126052 loops=1)
                     Sort Key: wo.node_code
                     Sort Method: external merge  Disk: 3152kB
                     ->  Seq Scan on wf_task_operation wo  (cost=0.00..40639.57 rows=128116 width=22) (actual time=0.014..285.332 rows=126052 loops=1)
                           Filter: ((node_type)::text = 'USER'::text)
                           Rows Removed by Filter: 1691194
 Planning time: 0.497 ms
 Execution time: 35858.726 ms
(19 rows)

此时仍然是对 wf_task_operation 表有 sort 操作，还有 Masterialize  
```


##  index tesing

Adding index in tables and checking explain info

```

-- 1 添加与 node_code 有关的索引

已有索引：
ALTER TABLE ONLY public.wf_task_operation
    ADD CONSTRAINT wf_task_operation_pkey PRIMARY KEY (id);

CREATE INDEX wf_task_operation_wf_task_id_node_code ON public.wf_task_operation USING btree (wf_task_id, node_code);

添加索引：
CREATE INDEX wf_task_operation_node_code_node_type_node_operator ON public.wf_task_operation USING btree (node_code,node_type,node_operator);

=>CREATE INDEX wf_task_operation_node_code_node_type_node_operator ON public.wf_task_operation USING btree (node_code,node_type,node_operator);
CREATE INDEX
Time: 24026.212 ms (00:24.026)

在此确认执行计划

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db->         WHERE wf.is_completed = false
dba_temp_db->             AND wf.wf_code = 'WF_ONBOARDING_KYC'
dba_temp_db->             AND wo.node_type = 'USER'
dba_temp_db->         GROUP BY wo.node_operator;
                                                                                 QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=87141.39..87141.41 rows=2 width=10) (actual time=35559.036..35559.047 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Merge Join  (cost=55011.15..87141.38 rows=2 width=10) (actual time=484.741..35553.483 rows=2522 loops=1)
         Merge Cond: ((wf.current_node)::text = (wo.node_code)::text)
         Join Filter: (wf.id = wo.wf_task_id)
         Rows Removed by Join Filter: 146127202
         ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task wf  (cost=0.42..121258.59 rows=3913 width=9) (actual time=0.017..42.668 rows=34231 loops=1)
               Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Rows Removed by Filter: 4340
         ->  Materialize  (cost=54136.85..54777.43 rows=128116 width=22) (actual time=421.649..9086.058 rows=146139485 loops=1)
               ->  Sort  (cost=54136.85..54457.14 rows=128116 width=22) (actual time=421.646..450.442 rows=126052 loops=1)
                     Sort Key: wo.node_code
                     Sort Method: external merge  Disk: 3152kB
                     ->  Seq Scan on wf_task_operation wo  (cost=0.00..40639.57 rows=128116 width=22) (actual time=0.009..283.931 rows=126052 loops=1)
                           Filter: ((node_type)::text = 'USER'::text)
                           Rows Removed by Filter: 1691194
 Planning time: 0.368 ms
 Execution time: 35560.642 ms
(19 rows)

Time: 35562.918 ms (00:35.563)

添加索引：
CREATE INDEX wf_task_operation_node_type ON public.wf_task_operation USING btree (node_type);

=>CREATE INDEX wf_task_operation_node_type ON public.wf_task_operation USING btree (node_type);
CREATE INDEX
Time: 11921.886 ms (00:11.922)

确认执行计划

SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code
		WHERE wf.is_completed = false
			AND wf.wf_code = 'WF_ONBOARDING_KYC'
			AND wo.node_type = 'USER'
		GROUP BY wo.node_operator

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db->         WHERE wf.is_completed = false
dba_temp_db->             AND wf.wf_code = 'WF_ONBOARDING_KYC'
dba_temp_db->             AND wo.node_type = 'USER'
dba_temp_db->         GROUP BY wo.node_operator;
                                                                                 QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=68600.60..68600.62 rows=2 width=10) (actual time=35226.603..35226.613 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Merge Join  (cost=36470.35..68600.59 rows=2 width=10) (actual time=277.328..35220.822 rows=2522 loops=1)
         Merge Cond: ((wf.current_node)::text = (wo.node_code)::text)
         Join Filter: (wf.id = wo.wf_task_id)
         Rows Removed by Join Filter: 146127202
         ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task wf  (cost=0.42..121258.59 rows=3913 width=9) (actual time=0.017..43.882 rows=34231 loops=1)
               Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Rows Removed by Filter: 4340
         ->  Materialize  (cost=35596.06..36236.64 rows=128116 width=22) (actual time=212.360..8892.834 rows=146139485 loops=1)
               ->  Sort  (cost=35596.06..35916.35 rows=128116 width=22) (actual time=212.357..240.938 rows=126052 loops=1)
                     Sort Key: wo.node_code
                     Sort Method: external merge  Disk: 3152kB
                     ->  Bitmap Heap Scan on wf_task_operation wo  (cost=2573.33..22098.78 rows=128116 width=22) (actual time=20.439..71.883 rows=126052 loops=1)
                           Recheck Cond: ((node_type)::text = 'USER'::text)
                           Heap Blocks: exact=14663
                           ->  Bitmap Index Scan on wf_task_operation_node_type  (cost=0.00..2541.30 rows=128116 width=0) (actual time=17.679..17.679 rows=126052 loops=1)
                                 Index Cond: ((node_type)::text = 'USER'::text)
 Planning time: 0.476 ms
 Execution time: 35228.171 ms
(21 rows)

Time: 35230.491 ms (00:35.230)

-- 增加另外一个表的字符列索引
已有索引：
ALTER TABLE ONLY public.wf_task
    ADD CONSTRAINT wf_task_pkey PRIMARY KEY (id);
CREATE INDEX wf_task_task_id ON public.wf_task USING btree (task_id);
CREATE INDEX wf_task_wf_code_current_node_updated_at ON public.wf_task USING btree (wf_code, current_node, updated_at);

新建索引：
CREATE INDEX wf_task_current_node ON public.wf_task USING btree (current_node);

=>CREATE INDEX wf_task_current_node ON public.wf_task USING btree (current_node);
CREATE INDEX
Time: 2452.097 ms (00:02.452)

确认执行计划




SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code GROUP BY wo.node_operator;


=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code GROUP BY wo.node_operator;
                                                                 QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=165145.61..165146.45 rows=84 width=10) (actual time=1872.784..1872.796 rows=74 loops=1)
   Group Key: wo.node_operator
   ->  Hash Right Join  (cost=75054.95..162418.22 rows=545478 width=10) (actual time=310.657..1781.810 rows=545478 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Seq Scan on wf_task_operation wo  (cost=0.00..36096.46 rows=1817246 width=22) (actual time=0.007..333.133 rows=1817246 loops=1)
         ->  Hash  (cost=64208.78..64208.78 rows=545478 width=9) (actual time=310.536..310.536 rows=545478 loops=1)
               Buckets: 16384  Batches: 8  Memory Usage: 2730kB
               ->  Seq Scan on wf_task wf  (cost=0.00..64208.78 rows=545478 width=9) (actual time=0.005..191.160 rows=545478 loops=1)
 Planning time: 0.345 ms
 Execution time: 1872.859 ms
(10 rows)

Time: 1875.046 ms (00:01.875)


SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code 
WHERE wo.node_type = 'USER'
GROUP BY wo.node_operator;


=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER'
dba_temp_db-> GROUP BY wo.node_operator;
                                                                          QUERY PLAN
---------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=103246.55..103246.61 rows=6 width=10) (actual time=465.961..465.969 rows=69 loops=1)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=77628.28..103244.86 rows=339 width=10) (actual time=315.663..463.328 rows=9434 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Bitmap Heap Scan on wf_task_operation wo  (cost=2573.33..22098.78 rows=128116 width=22) (actual time=17.450..69.175 rows=126052 loops=1)
               Recheck Cond: ((node_type)::text = 'USER'::text)
               Heap Blocks: exact=14663
               ->  Bitmap Index Scan on wf_task_operation_node_type  (cost=0.00..2541.30 rows=128116 width=0) (actual time=14.716..14.716 rows=126052 loops=1)
                     Index Cond: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=64208.78..64208.78 rows=545478 width=9) (actual time=296.886..296.886 rows=473016 loops=1)
               Buckets: 16384  Batches: 8  Memory Usage: 2412kB
               ->  Seq Scan on wf_task wf  (cost=0.00..64208.78 rows=545478 width=9) (actual time=0.004..187.476 rows=545478 loops=1)
 Planning time: 0.393 ms
 Execution time: 466.039 ms
(14 rows)

Time: 468.292 ms


SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code 
WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC'
GROUP BY wo.node_operator;

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC'
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                  QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=86917.99..86918.05 rows=6 width=10) (actual time=171.512..171.518 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=64829.76..86917.84 rows=31 width=10) (actual time=84.387..170.652 rows=2603 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Bitmap Heap Scan on wf_task_operation wo  (cost=2573.33..22098.78 rows=128116 width=22) (actual time=17.368..60.353 rows=126052 loops=1)
               Recheck Cond: ((node_type)::text = 'USER'::text)
               Heap Blocks: exact=14663
               ->  Bitmap Index Scan on wf_task_operation_node_type  (cost=0.00..2541.30 rows=128116 width=0) (actual time=14.681..14.681 rows=126052 loops=1)
                     Index Cond: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=61497.13..61497.13 rows=50620 width=9) (actual time=66.950..66.950 rows=34584 loops=1)
               Buckets: 8192  Batches: 1  Memory Usage: 1551kB
               ->  Bitmap Heap Scan on wf_task wf  (cost=1708.73..61497.13 rows=50620 width=9) (actual time=15.332..58.223 rows=50691 loops=1)
                     Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     Heap Blocks: exact=27057
                     ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=10.054..10.054 rows=50691 loops=1)
                           Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
 Planning time: 0.412 ms
 Execution time: 171.593 ms
(18 rows)

Time: 173.858 ms

# 添加索引
CREATE INDEX wf_task_current_node_is_completed ON public.wf_task USING btree (current_node,is_completed);

=>CREATE INDEX wf_task_current_node_is_completed ON public.wf_task USING btree (current_node,is_completed);
CREATE INDEX
Time: 2831.464 ms (00:02.831)

添加索引后的执行计划为：

SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code 
WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
GROUP BY wo.node_operator;

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                     QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=48683.81..48683.83 rows=2 width=10) (actual time=283.376..283.384 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=27236.59..48683.80 rows=2 width=10) (actual time=109.011..282.453 rows=2522 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Bitmap Heap Scan on wf_task_operation wo  (cost=2573.33..22098.78 rows=128116 width=22) (actual time=17.717..61.255 rows=126052 loops=1)
               Recheck Cond: ((node_type)::text = 'USER'::text)
               Heap Blocks: exact=14663
               ->  Bitmap Index Scan on wf_task_operation_node_type  (cost=0.00..2541.30 rows=128116 width=0) (actual time=14.962..14.962 rows=126052 loops=1)
                     Index Cond: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=24604.62..24604.62 rows=3910 width=9) (actual time=91.146..91.146 rows=34230 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 1534kB
               ->  Bitmap Heap Scan on wf_task wf  (cost=12297.79..24604.62 rows=3910 width=9) (actual time=54.030..84.190 rows=34244 loops=1)
                     Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     Filter: (NOT is_completed)
                     Heap Blocks: exact=20383
                     ->  BitmapAnd  (cost=12297.79..12297.79 rows=3910 width=0) (actual time=50.041..50.041 rows=0 loops=1)
                           ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=10.281..10.281 rows=50691 loops=1)
                                 Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                           ->  Bitmap Index Scan on wf_task_current_node_is_completed  (cost=0.00..10599.51 rows=42129 width=0) (actual time=35.490..35.490 rows=43026 loops=1)
                                 Index Cond: (is_completed = false)
 Planning time: 0.524 ms
 Execution time: 283.461 ms
(22 rows)

Time: 285.930 ms

-- 删除重复的索引，确认达到优化效果需要添加的最小索引情况

DROP INDEX index_name;

-- 删除 wf_task 表上的索引

DROP INDEX wf_task_current_node;

=>DROP INDEX wf_task_current_node;
DROP INDEX
Time: 7.592 ms

确认删除这个重复索引后，执行计划没有改变，效率仍然很快；

-- 删除 wf_task_operation 表上的索引

DROP INDEX wf_task_operation_node_type;

=>DROP INDEX wf_task_operation_node_type;
DROP INDEX
Time: 16.262 ms

确认执行计划：

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                  QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=52822.78..52822.80 rows=2 width=10) (actual time=2179.020..2179.029 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Nested Loop  (cost=12298.22..52822.77 rows=2 width=10) (actual time=38.696..2177.188 rows=2522 loops=1)
         ->  Bitmap Heap Scan on wf_task wf  (cost=12297.79..24604.62 rows=3910 width=9) (actual time=38.521..76.330 rows=34244 loops=1)
               Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Heap Blocks: exact=20383
               ->  BitmapAnd  (cost=12297.79..12297.79 rows=3910 width=0) (actual time=34.537..34.537 rows=0 loops=1)
                     ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=9.982..9.982 rows=50691 loops=1)
                           Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     ->  Bitmap Index Scan on wf_task_current_node_is_completed  (cost=0.00..10599.51 rows=42129 width=0) (actual time=20.811..20.811 rows=43026 loops=1)
                           Index Cond: (is_completed = false)
         ->  Index Scan using wf_task_operation_wf_task_id_node_code on wf_task_operation wo  (cost=0.43..7.21 rows=1 width=22) (actual time=0.061..0.061 rows=0 loops=34244)
               Index Cond: ((wf_task_id = wf.id) AND ((node_code)::text = (wf.current_node)::text))
               Filter: ((node_type)::text = 'USER'::text)
               Rows Removed by Filter: 1
 Planning time: 0.458 ms
 Execution time: 2179.101 ms
(18 rows)

Time: 2181.476 ms (00:02.181)

这时执行计划又发生了改变： wf_task 表的位图索引查询没有发生改变； 
但 wf_task_operation 表中由位图索引，变成了索引扫描，使用的是已有的 task_id， node_code 的索引；
同时表连接方式，由 wf_task 表先一次hash连接，两个表一起 Hash Join连接，变成了 Nested Loop嵌套循环。
整体耗时，增加了10倍。

-- 删除以 node_code 开头的符合索引

DROP INDEX wf_task_operation_node_code_node_type_node_operator;

=>DROP INDEX wf_task_operation_node_code_node_type_node_operator;
DROP INDEX
Time: 25.772 ms

此时对应的执行计划为：
dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                  QUERY PLAN
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=52822.78..52822.80 rows=2 width=10) (actual time=175.733..175.741 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Nested Loop  (cost=12298.22..52822.77 rows=2 width=10) (actual time=38.298..174.840 rows=2522 loops=1)
         ->  Bitmap Heap Scan on wf_task wf  (cost=12297.79..24604.62 rows=3910 width=9) (actual time=38.250..68.271 rows=34244 loops=1)
               Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Heap Blocks: exact=20383
               ->  BitmapAnd  (cost=12297.79..12297.79 rows=3910 width=0) (actual time=34.278..34.278 rows=0 loops=1)
                     ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=9.485..9.485 rows=50691 loops=1)
                           Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     ->  Bitmap Index Scan on wf_task_current_node_is_completed  (cost=0.00..10599.51 rows=42129 width=0) (actual time=20.793..20.793 rows=43026 loops=1)
                           Index Cond: (is_completed = false)
         ->  Index Scan using wf_task_operation_wf_task_id_node_code on wf_task_operation wo  (cost=0.43..7.21 rows=1 width=22) (actual time=0.003..0.003 rows=0 loops=34244)
               Index Cond: ((wf_task_id = wf.id) AND ((node_code)::text = (wf.current_node)::text))
               Filter: ((node_type)::text = 'USER'::text)
               Rows Removed by Filter: 1
 Planning time: 0.376 ms
 Execution time: 175.805 ms
(18 rows)

Time: 177.992 ms


-- 添加一个索引

CREATE INDEX wf_task_operation_node_type_node_operator ON public.wf_task_operation USING btree (node_type, node_operator);

=>CREATE INDEX wf_task_operation_node_type_node_operator ON public.wf_task_operation USING btree (node_type, node_operator);

CREATE INDEX
Time: 18284.386 ms (00:18.284)

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                     QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=49375.81..49375.83 rows=2 width=10) (actual time=269.054..269.063 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=27928.59..49375.80 rows=2 width=10) (actual time=100.143..268.086 rows=2522 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Bitmap Heap Scan on wf_task_operation wo  (cost=3265.33..22790.78 rows=128116 width=22) (actual time=24.120..67.215 rows=126052 loops=1)
               Recheck Cond: ((node_type)::text = 'USER'::text)
               Heap Blocks: exact=14663
               ->  Bitmap Index Scan on wf_task_operation_node_type_node_operator  (cost=0.00..3233.30 rows=128116 width=0) (actual time=21.372..21.372 rows=126052 loops=1)
                     Index Cond: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=24604.62..24604.62 rows=3910 width=9) (actual time=75.870..75.870 rows=34230 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 1534kB
               ->  Bitmap Heap Scan on wf_task wf  (cost=12297.79..24604.62 rows=3910 width=9) (actual time=39.328..69.123 rows=34244 loops=1)
                     Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     Filter: (NOT is_completed)
                     Heap Blocks: exact=20383
                     ->  BitmapAnd  (cost=12297.79..12297.79 rows=3910 width=0) (actual time=35.401..35.401 rows=0 loops=1)
                           ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=10.164..10.164 rows=50691 loops=1)
                                 Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                           ->  Bitmap Index Scan on wf_task_current_node_is_completed  (cost=0.00..10599.51 rows=42129 width=0) (actual time=21.735..21.735 rows=43026 loops=1)
                                 Index Cond: (is_completed = false)
 Planning time: 0.423 ms
 Execution time: 269.136 ms
(22 rows)

Time: 271.438 ms
```

##  The last SQL tuning

The last SQL tuning mehtod is 

```

需要增加的索引为：

## wf_task

-- 索引增加语句
CREATE INDEX wf_task_current_node_is_completed ON public.wf_task USING btree (current_node,is_completed);

-- 索引结构变化
Indexes:
    "wf_task_pkey" PRIMARY KEY, btree (id)
    "wf_task_task_id" btree (task_id)
    "wf_task_wf_code_current_node_updated_at" btree (wf_code, current_node, updated_at)

Indexes:
    "wf_task_pkey" PRIMARY KEY, btree (id)
    "wf_task_current_node_is_completed" btree (current_node, is_completed)
    "wf_task_task_id" btree (task_id)
    "wf_task_wf_code_current_node_updated_at" btree (wf_code, current_node, updated_at)


## wf_task_operation

-- 索引增加语句
CREATE INDEX wf_task_operation_node_type_node_operator ON public.wf_task_operation USING btree (node_type, node_operator);

-- 索引结构变化
Indexes:
    "wf_task_operation_pkey" PRIMARY KEY, btree (id)
    "wf_task_operation_wf_task_id_node_code" btree (wf_task_id, node_code)

Indexes:
    "wf_task_operation_pkey" PRIMARY KEY, btree (id)
    "wf_task_operation_node_type_node_operator" btree (node_type, node_operator)
    "wf_task_operation_wf_task_id_node_code" btree (wf_task_id, node_code)

##  执行计划对比为

-- 查询SQL
SELECT wo.node_operator AS operator, COUNT(1) AS total
		FROM wf_task wf
			LEFT JOIN wf_task_operation wo
			ON wf.id = wo.wf_task_id
				AND wf.current_node = wo.node_code 
WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
GROUP BY wo.node_operator;

-- 调整前执行计划

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>
dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                 QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=87094.59..87094.61 rows=2 width=10) (actual time=35785.517..35785.527 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Merge Join  (cost=55010.54..87094.58 rows=2 width=10) (actual time=492.537..35779.109 rows=2522 loops=1)
         Merge Cond: ((wf.current_node)::text = (wo.node_code)::text)
         Join Filter: (wf.id = wo.wf_task_id)
         Rows Removed by Join Filter: 146127202
         ->  Index Scan using wf_task_wf_code_current_node_updated_at on wf_task wf  (cost=0.42..121191.12 rows=3910 width=9) (actual time=0.021..44.677 rows=34231 loops=1)
               Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
               Filter: (NOT is_completed)
               Rows Removed by Filter: 4340
         ->  Materialize  (cost=54136.85..54777.43 rows=128116 width=22) (actual time=427.843..9241.811 rows=146139485 loops=1)
               ->  Sort  (cost=54136.85..54457.14 rows=128116 width=22) (actual time=427.839..455.301 rows=126052 loops=1)
                     Sort Key: wo.node_code
                     Sort Method: external merge  Disk: 3152kB
                     ->  Seq Scan on wf_task_operation wo  (cost=0.00..40639.57 rows=128116 width=22) (actual time=0.017..289.090 rows=126052 loops=1)
                           Filter: ((node_type)::text = 'USER'::text)
                           Rows Removed by Filter: 1691194
 Planning time: 0.618 ms
 Execution time: 35787.166 ms
(19 rows)

Time: 35789.772 ms (00:35.790)

-- 调整后执行计划

dba_temp_db@rm-j6c55xiu84647efg4.pg.rds.aliyuncs.com:3433=>explain analyze SELECT wo.node_operator AS operator, COUNT(1) AS total
dba_temp_db->         FROM wf_task wf
dba_temp_db->             LEFT JOIN wf_task_operation wo
dba_temp_db->             ON wf.id = wo.wf_task_id
dba_temp_db->                 AND wf.current_node = wo.node_code
dba_temp_db-> WHERE wo.node_type = 'USER' and wf.wf_code = 'WF_ONBOARDING_KYC' and wf.is_completed = false
dba_temp_db-> GROUP BY wo.node_operator;
                                                                                     QUERY PLAN
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=49375.81..49375.83 rows=2 width=10) (actual time=269.054..269.063 rows=56 loops=1)
   Group Key: wo.node_operator
   ->  Hash Join  (cost=27928.59..49375.80 rows=2 width=10) (actual time=100.143..268.086 rows=2522 loops=1)
         Hash Cond: ((wo.wf_task_id = wf.id) AND ((wo.node_code)::text = (wf.current_node)::text))
         ->  Bitmap Heap Scan on wf_task_operation wo  (cost=3265.33..22790.78 rows=128116 width=22) (actual time=24.120..67.215 rows=126052 loops=1)
               Recheck Cond: ((node_type)::text = 'USER'::text)
               Heap Blocks: exact=14663
               ->  Bitmap Index Scan on wf_task_operation_node_type_node_operator  (cost=0.00..3233.30 rows=128116 width=0) (actual time=21.372..21.372 rows=126052 loops=1)
                     Index Cond: ((node_type)::text = 'USER'::text)
         ->  Hash  (cost=24604.62..24604.62 rows=3910 width=9) (actual time=75.870..75.870 rows=34230 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 1534kB
               ->  Bitmap Heap Scan on wf_task wf  (cost=12297.79..24604.62 rows=3910 width=9) (actual time=39.328..69.123 rows=34244 loops=1)
                     Recheck Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                     Filter: (NOT is_completed)
                     Heap Blocks: exact=20383
                     ->  BitmapAnd  (cost=12297.79..12297.79 rows=3910 width=0) (actual time=35.401..35.401 rows=0 loops=1)
                           ->  Bitmap Index Scan on wf_task_wf_code_current_node_updated_at  (cost=0.00..1696.08 rows=50620 width=0) (actual time=10.164..10.164 rows=50691 loops=1)
                                 Index Cond: ((wf_code)::text = 'WF_ONBOARDING_KYC'::text)
                           ->  Bitmap Index Scan on wf_task_current_node_is_completed  (cost=0.00..10599.51 rows=42129 width=0) (actual time=21.735..21.735 rows=43026 loops=1)
                                 Index Cond: (is_completed = false)
 Planning time: 0.423 ms
 Execution time: 269.136 ms
(22 rows)

Time: 271.438 ms


```



