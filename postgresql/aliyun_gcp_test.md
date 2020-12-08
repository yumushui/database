# The postgresql Overtime Testing When Failover on Aliyun and GCP Cloud

##  1. The Document about postgresql instance failover

```
    高可用性自动和手工切换： 
    https://help.aliyun.com/document_detail/96054.html?spm=a2c4g.11186623.2.7.3f2f4c07IASb5e#task-ftz-42j-wdb

    aliyun RDS 变更配置：
    https://help.aliyun.com/document_detail/96061.html?spm=a2c4g.11186623.6.717.56601553kh7rWo

    aliyun RDS postgresql变更配置：
    https://help.aliyun.com/document_detail/96750.html?spm=a2c4g.11186623.2.15.744460b4WDQrFm#concept-efl-pln-wdb

    aliyun RDS PostgreSQL 升级内核小版本：
    https://help.aliyun.com/document_detail/146895.html?spm=a2c4g.11186623.6.1018.701832f07X7ykk

    aliyun RDS postgresql 自动或手动主备切换：
    https://help.aliyun.com/document_detail/96747.html?spm=a2c4g.11186623.6.1020.28c912c0JNkp46

    GCP Cloud SQL for high availability
    https://cloud.google.com/sql/docs/postgres/configure-ha

```

##  2. Failover Test enviroment

```

-- aliyun pg RDS
	数据库类型：PostgreSQL 12.0
    实例ID：pgm-j6czvm5baw66061r
    内网地址：pgm-j6czvm5baw66061r8o.pg.rds.aliyuncs.com
    内网端口：1921


-- gcp cloud sql
airwallex-acquiring-poc:asia-east2:dba-test-cloudsql-pg12-master
34.96.133.132:5432


-- client

dba-test-vm-pg12-replicaiton-test
10.170.0.2

```


-- Test DB and tables
```
-- CREATE 
aliyun_pg12_service=aliyun_pg12_master_cron
gcp_pg12_service=gcp_cloudsql_pg12_app

create database dba_test_db;


drop table if exists public.tab_overtime_test;

CREATE TABLE public.tab_overtime_test (
    id serial,
    time_int bigint,
    radom_char character varying(10),
    datetime character varying(40) DEFAULT now()
);

```


##  3. Test Plan

```
1 execute pg failover when DB are writing on Aliyun Cloud

2 execute pg failover when DB are reading on Aliyun Cloud

3 execute pg failover when DB are writing on GCP Cloud

4 execute pg failover when DB are reading on GCP Cloud

```

##  4. Testing Result

|Cloud|Type|Operate|Times|start_time|end_time|overtime|
|--|--|--|--|--|--|--|
|Aliyun|Write|Failover|01|2020-12-07 20:38:26 |2020-12-07 12:38:58 |32 | 
|Aliyun|Write|Failover|02|2020-12-07 12:50:51 |2020-12-07 12:51:24 |33 |
|Aliyun|Write|Failover|03|2020-12-07 13:04:13 |2020-12-07 13:04:42 |29 |
|Aliyun|Read|Failover|01|2020-12-07 21:19:37 |2020-12-07 21:20:12 |0 |
|GCP|Write|Failover|01|2020-12-07 13:39:39 |2020-12-07 13:40:06 |27 |
|GCP|Write|Failover|02|2020-12-07 13:48:44 |2020-12-07 13:49:29 |45 |
|GCP|Write|Failover|03|2020-12-07 13:53:41 |2020-12-07 13:54:08 |27 |
|GCP|Read|Failover|01|2020-12-07 13:59:02 |2020-12-07 13:59:46 |44 |

From the testing result, we can see:
1. The Aliyun RDS failover will has not effect to read, all read opertion are normal in the prograss.
2. The GCP Cloud SQL for PG can not read and write in failover prograss.
3. The Failover time of Aliyun is about 30 seconds now.
4. The Failover time of GCP is between 27 and 44 seconds now.
5. The Testing result about Aliyun write is not the same as our consider.


The detail shell check log is in 
```
https://github.com/yumushui/database/blob/master/postgresql/aliyun_gcp_test.log
```

##  5. Tesing Detail info



### 5.1 - Test 01: execute pg failover when DB are writing on Aliyun Cloud

Test shell script
```
postgres@dba-test-vm-pg12-replicaiton-test-> cat overtime_write_test.sh
#!/bin/sh


aliyun_pg12_service=aliyun_pg12_master_cron
gcp_pg12_service=gcp_cloudsql_pg12_app

for ((i=1; i<=10000; i++))
do
    echo "-- connect ${i} times: os time is `date '+%Y-%m-%d %H:%M:%S'` "
    time_int=`date '+%Y%m%d%H%M%S'`
    radom_char="croninsert"
    insert_sql=`echo "INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( ${time_int} ,?${radom_char}? );" | sed "s/?/'/g"`

    sql_01="select 'aliyun pg rds',* from public.tab_overtime_test order by id desc limit 1;"
    psql service=${aliyun_pg12_service} -c "${insert_sql}" | sed '$d'
    psql service=${aliyun_pg12_service} -t -c "${sql_01}" | sed '$d'

    sql_02="select 'gcp cloudsql pg',* from public.tab_overtime_test order by id desc limit 1;"
    #psql service=${gcp_pg12_service} -c "${insert_sql}" | sed '$d'
    #psql service=${gcp_pg12_service} -t -c "${sql_02}" | sed '$d'

    #date '+%Y-%m-%d %H:%M:%S'
    sleep 1
    echo
done



postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test-> /bin/sh overtime_write_test.sh >> test.log 2>&1
```

### 5.1.1 - Times 01

Operate time:
```
$ date '+%Y-%m-%d %H:%M:%S'
2020-12-07 20:38:09
```

Check Scripte中记录为：
```

-- connect 36 times: os time is 2020-12-07 12:38:26
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 65 times: os time is 2020-12-07 12:38:57
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 66 times: os time is 2020-12-07 12:38:58
 aliyun pg rds | 67 | 20201207123858 | croninsert | 2020-12-07 20:38:58.936888+08

```

table data status
```
  34 | 20201207123824 | croninsert | 2020-12-07 20:38:24.153533+08
  35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08
  67 | 20201207123858 | croninsert | 2020-12-07 20:38:58.936888+08

  68 | 20201207123859 | croninsert | 2020-12-07 20:39:00.017241+08
  69 | 20201207123901 | croninsert | 2020-12-07 20:39:01.101576+08
```

RDS主备切换记录时间：
|切换事件ID	  |切换开始时间	       |切换结束时间	          |切换原因|
|--|--|--|--|
|SwitchId	|2020-12-07 20:38:24	|2020-12-07 20:39:00	|SwitchOver|


对应 Aliyiun RDS error 日志为：
```
2020-12-07 20:38:25	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 20:38:25	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 20:38:25	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 20:38:25	WARNING: 01000: archive_mode enabled, yet archive_command is not se
2020-12-07 20:38:45	LOG: 00000: postmaster is in PM_STARTUP state.
2020-12-07 20:38:45	LOG: 00000: database system was interrupted; last known up at 2020-12-07 12:29:24 UTC
2020-12-07 20:38:45	LOG: 00000: entering standby mode
2020-12-07 20:38:45	LOG: 00000: database system was not properly shut down; automatic recovery in progress
2020-12-07 20:38:45	LOG: 00000: redo starts at C1/770016E8
2020-12-07 20:38:45	LOG: 00000: postmaster is in PM_RECOVERY state.
2020-12-07 20:38:45	LOG: 00000: invalid record length at C1/790041F8: wanted 24, got 0
2020-12-07 20:38:45	LOG: 00000: consistent recovery state reached at C1/790041F8
2020-12-07 20:38:45	LOG: 00000: database system is ready to accept read only connections
2020-12-07 20:38:45	LOG: 00000: postmaster is in PM_HOT_STANDBY state.
2020-12-07 20:38:45	LOG: 00000: started streaming WAL from primary at C1/79000000 on timeline 3
2020-12-07 20:38:58	LOG: 00000: replication terminated by primary server
2020-12-07 20:38:58	DETAIL: End of WAL reached on timeline 3 at C1/790041F8.
2020-12-07 20:38:58	LOG: 00000: fetching timeline history file for timeline 4 from primary server
2020-12-07 20:38:58	LOG: 00000: new target timeline is 4
2020-12-07 20:38:58	LOG: 00000: restarted WAL streaming at C1/79000000 on timeline 4
```



Shell scripte detail log
```
####################################
# Test 01 Aliyun write and Read
###################################
#
#date '+%Y-%m-%d %H:%M:%S'
#2020-12-07 20:36:09
#


-- connect 1 times: os time is 2020-12-07 12:37:48
 aliyun pg rds |  1 | 20201207123748 | croninsert | 2020-12-07 20:37:48.267839+08

-- connect 2 times: os time is 2020-12-07 12:37:49
 aliyun pg rds |  2 | 20201207123749 | croninsert | 2020-12-07 20:37:49.338193+08

-- connect 3 times: os time is 2020-12-07 12:37:50
 aliyun pg rds |  3 | 20201207123750 | croninsert | 2020-12-07 20:37:50.407646+08

-- connect 4 times: os time is 2020-12-07 12:37:51
 aliyun pg rds |  4 | 20201207123751 | croninsert | 2020-12-07 20:37:51.476111+08

-- connect 5 times: os time is 2020-12-07 12:37:52
 aliyun pg rds |  5 | 20201207123752 | croninsert | 2020-12-07 20:37:52.549553+08

-- connect 6 times: os time is 2020-12-07 12:37:53
 aliyun pg rds |  6 | 20201207123753 | croninsert | 2020-12-07 20:37:53.65908+08

-- connect 7 times: os time is 2020-12-07 12:37:54
 aliyun pg rds |  7 | 20201207123754 | croninsert | 2020-12-07 20:37:54.729642+08

-- connect 8 times: os time is 2020-12-07 12:37:55
 aliyun pg rds |  8 | 20201207123755 | croninsert | 2020-12-07 20:37:55.801741+08

-- connect 9 times: os time is 2020-12-07 12:37:56
 aliyun pg rds |  9 | 20201207123756 | croninsert | 2020-12-07 20:37:56.870385+08

-- connect 10 times: os time is 2020-12-07 12:37:57
 aliyun pg rds | 10 | 20201207123757 | croninsert | 2020-12-07 20:37:57.939782+08

-- connect 11 times: os time is 2020-12-07 12:37:58
 aliyun pg rds | 11 | 20201207123758 | croninsert | 2020-12-07 20:37:59.048608+08

-- connect 12 times: os time is 2020-12-07 12:38:00
 aliyun pg rds | 12 | 20201207123800 | croninsert | 2020-12-07 20:38:00.118559+08

-- connect 13 times: os time is 2020-12-07 12:38:01
 aliyun pg rds | 13 | 20201207123801 | croninsert | 2020-12-07 20:38:01.186474+08

-- connect 14 times: os time is 2020-12-07 12:38:02
 aliyun pg rds | 14 | 20201207123802 | croninsert | 2020-12-07 20:38:02.269471+08

-- connect 15 times: os time is 2020-12-07 12:38:03
 aliyun pg rds | 15 | 20201207123803 | croninsert | 2020-12-07 20:38:03.342371+08

-- connect 16 times: os time is 2020-12-07 12:38:04
 aliyun pg rds | 16 | 20201207123804 | croninsert | 2020-12-07 20:38:04.495824+08

-- connect 17 times: os time is 2020-12-07 12:38:05
 aliyun pg rds | 17 | 20201207123805 | croninsert | 2020-12-07 20:38:05.572181+08

-- connect 18 times: os time is 2020-12-07 12:38:06
 aliyun pg rds | 18 | 20201207123806 | croninsert | 2020-12-07 20:38:06.641224+08

-- connect 19 times: os time is 2020-12-07 12:38:07
 aliyun pg rds | 19 | 20201207123807 | croninsert | 2020-12-07 20:38:07.717562+08

-- connect 20 times: os time is 2020-12-07 12:38:08
 aliyun pg rds | 20 | 20201207123808 | croninsert | 2020-12-07 20:38:08.788769+08

-- connect 21 times: os time is 2020-12-07 12:38:09
 aliyun pg rds | 21 | 20201207123809 | croninsert | 2020-12-07 20:38:09.893611+08

-- connect 22 times: os time is 2020-12-07 12:38:10
 aliyun pg rds | 22 | 20201207123810 | croninsert | 2020-12-07 20:38:11.037108+08

-- connect 23 times: os time is 2020-12-07 12:38:12
 aliyun pg rds | 23 | 20201207123812 | croninsert | 2020-12-07 20:38:12.10846+08

-- connect 24 times: os time is 2020-12-07 12:38:13
 aliyun pg rds | 24 | 20201207123813 | croninsert | 2020-12-07 20:38:13.180285+08

-- connect 25 times: os time is 2020-12-07 12:38:14
 aliyun pg rds | 25 | 20201207123814 | croninsert | 2020-12-07 20:38:14.250297+08

-- connect 26 times: os time is 2020-12-07 12:38:15
 aliyun pg rds | 26 | 20201207123815 | croninsert | 2020-12-07 20:38:15.321217+08

-- connect 27 times: os time is 2020-12-07 12:38:16
 aliyun pg rds | 27 | 20201207123816 | croninsert | 2020-12-07 20:38:16.388051+08

-- connect 28 times: os time is 2020-12-07 12:38:17
 aliyun pg rds | 28 | 20201207123817 | croninsert | 2020-12-07 20:38:17.496443+08

-- connect 29 times: os time is 2020-12-07 12:38:18
 aliyun pg rds | 29 | 20201207123818 | croninsert | 2020-12-07 20:38:18.611667+08

-- connect 30 times: os time is 2020-12-07 12:38:19
 aliyun pg rds | 30 | 20201207123819 | croninsert | 2020-12-07 20:38:19.797758+08

-- connect 31 times: os time is 2020-12-07 12:38:20
 aliyun pg rds | 31 | 20201207123820 | croninsert | 2020-12-07 20:38:20.869894+08

-- connect 32 times: os time is 2020-12-07 12:38:21
 aliyun pg rds | 32 | 20201207123821 | croninsert | 2020-12-07 20:38:21.938563+08

-- connect 33 times: os time is 2020-12-07 12:38:23
 aliyun pg rds | 33 | 20201207123823 | croninsert | 2020-12-07 20:38:23.046391+08

-- connect 34 times: os time is 2020-12-07 12:38:24
 aliyun pg rds | 34 | 20201207123824 | croninsert | 2020-12-07 20:38:24.153533+08

-- connect 35 times: os time is 2020-12-07 12:38:25
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 36 times: os time is 2020-12-07 12:38:26
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 37 times: os time is 2020-12-07 12:38:27
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 38 times: os time is 2020-12-07 12:38:28
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 39 times: os time is 2020-12-07 12:38:29
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 40 times: os time is 2020-12-07 12:38:30
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 41 times: os time is 2020-12-07 12:38:31
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 42 times: os time is 2020-12-07 12:38:32
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 43 times: os time is 2020-12-07 12:38:33
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 44 times: os time is 2020-12-07 12:38:35
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 45 times: os time is 2020-12-07 12:38:36
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 46 times: os time is 2020-12-07 12:38:37
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 47 times: os time is 2020-12-07 12:38:38
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 48 times: os time is 2020-12-07 12:38:39
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 49 times: os time is 2020-12-07 12:38:40
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 50 times: os time is 2020-12-07 12:38:41
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 51 times: os time is 2020-12-07 12:38:42
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 52 times: os time is 2020-12-07 12:38:43
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 53 times: os time is 2020-12-07 12:38:44
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 54 times: os time is 2020-12-07 12:38:45
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 55 times: os time is 2020-12-07 12:38:46
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 56 times: os time is 2020-12-07 12:38:48
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 57 times: os time is 2020-12-07 12:38:49
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 58 times: os time is 2020-12-07 12:38:50
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 59 times: os time is 2020-12-07 12:38:51
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 60 times: os time is 2020-12-07 12:38:52
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 61 times: os time is 2020-12-07 12:38:53
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 62 times: os time is 2020-12-07 12:38:54
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 63 times: os time is 2020-12-07 12:38:55
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 64 times: os time is 2020-12-07 12:38:56
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 65 times: os time is 2020-12-07 12:38:57
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 35 | 20201207123825 | croninsert | 2020-12-07 20:38:25.225612+08

-- connect 66 times: os time is 2020-12-07 12:38:58
 aliyun pg rds | 67 | 20201207123858 | croninsert | 2020-12-07 20:38:58.936888+08

-- connect 67 times: os time is 2020-12-07 12:38:59
 aliyun pg rds | 68 | 20201207123859 | croninsert | 2020-12-07 20:39:00.017241+08

-- connect 68 times: os time is 2020-12-07 12:39:01
 aliyun pg rds | 69 | 20201207123901 | croninsert | 2020-12-07 20:39:01.101576+08

-- connect 69 times: os time is 2020-12-07 12:39:02
 aliyun pg rds | 70 | 20201207123902 | croninsert | 2020-12-07 20:39:02.182775+08

-- connect 70 times: os time is 2020-12-07 12:39:03
 aliyun pg rds | 71 | 20201207123903 | croninsert | 2020-12-07 20:39:03.297124+08

-- connect 71 times: os time is 2020-12-07 12:39:04
 aliyun pg rds | 72 | 20201207123904 | croninsert | 2020-12-07 20:39:04.372773+08
```

### 5.1.2 - Times 02

Operate time
```
$ date '+%Y-%m-%d %H:%M:%S'
2020-12-07 20:49:57
```

Shell check status
```
-- connect 33 times: os time is 2020-12-07 12:50:49
 aliyun pg rds | 176 | 20201207125050 | croninsert | 2020-12-07 20:50:50.105628+08

-- connect 34 times: os time is 2020-12-07 12:50:51
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 176 | 20201207125050 | croninsert | 2020-12-07 20:50:50.105628+08

-- connect 64 times: os time is 2020-12-07 12:51:23
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 176 | 20201207125050 | croninsert | 2020-12-07 20:50:50.105628+08

-- connect 65 times: os time is 2020-12-07 12:51:24
 aliyun pg rds | 199 | 20201207125124 | croninsert | 2020-12-07 20:51:24.709439+08

```

Table check status
```
 174 | 20201207125047 | croninsert | 2020-12-07 20:50:47.884333+08
 175 | 20201207125048 | croninsert | 2020-12-07 20:50:48.95875+08
 176 | 20201207125050 | croninsert | 2020-12-07 20:50:50.105628+08

 199 | 20201207125124 | croninsert | 2020-12-07 20:51:24.709439+08
 200 | 20201207125125 | croninsert | 2020-12-07 20:51:25.783784+08
 201 | 20201207125126 | croninsert | 2020-12-07 20:51:26.894779+08
 202 | 20201207125127 | croninsert | 2020-12-07 20:51:27.964461+08
```

RDS主备切换日志：
|切换事件ID	|切换开始时间	|切换结束时间	|切换原因 |
|--|--|--|--|
|SwitchId	|2020-12-07 20:50:49	|2020-12-07 20:51:26	|SwitchOver|

Aliyun RDS error log:
```

2020-12-07 20:50:51	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:50:51	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125051 ,'croninsert' );
2020-12-07 20:50:52	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:50:52	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125052 ,'croninsert' );
2020-12-07 20:50:53	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:50:53	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125053 ,'croninsert' );
2020-12-07 20:50:54	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:50:54	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125054 ,'croninsert' );
2020-12-07 20:50:55	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:50:55	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125055 ,'croninsert' );
2020-12-07 20:51:08	FATAL: XX000: could not receive data from WAL stream: SSL SYSCALL error: EOF detected
2020-12-07 20:51:08	LOG: 00000: record with incorrect prev-link 0/21 at C1/7B001DA8
2020-12-07 20:51:08	FATAL: XX000: could not connect to the primary server: server closed the connection unexpectedly	This probably means the server terminated abnormally before or while processing the request.
2020-12-07 20:51:08	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:51:08	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125108 ,'croninsert' );
2020-12-07 20:51:21	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 20:51:21	STATEMENT: INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( 20201207125121 ,'croninsert' );
```

### 5.1.3 - Times 03

Operate Time:
```
$ date '+%Y-%m-%d %H:%M:%S'
2020-12-07 21:03:18
```

Shell check status
```
-- connect 34 times: os time is 2020-12-07 13:04:12
 aliyun pg rds | 275 | 20201207130412 | croninsert | 2020-12-07 21:04:12.461877+08

-- connect 35 times: os time is 2020-12-07 13:04:13
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 275 | 20201207130412 | croninsert | 2020-12-07 21:04:12.461877+08

-- connect 61 times: os time is 2020-12-07 13:04:41
ERROR:  cannot execute INSERT in a read-only transaction
 aliyun pg rds | 275 | 20201207130412 | croninsert | 2020-12-07 21:04:12.461877+08

-- connect 62 times: os time is 2020-12-07 13:04:42
 aliyun pg rds | 298 | 20201207130442 | croninsert | 2020-12-07 21:04:42.877442+08

```

Table check status
```
 273 | 20201207130410 | croninsert | 2020-12-07 21:04:10.323775+08
 274 | 20201207130411 | croninsert | 2020-12-07 21:04:11.393753+08
 275 | 20201207130412 | croninsert | 2020-12-07 21:04:12.461877+08

 298 | 20201207130442 | croninsert | 2020-12-07 21:04:42.877442+08
 299 | 20201207130443 | croninsert | 2020-12-07 21:04:43.959244+08
 300 | 20201207130445 | croninsert | 2020-12-07 21:04:45.03847+08
```

RDS 主备切换日志看：
|切换事件ID	|切换开始时间	|切换结束时间	|切换原因 |
|--|--|--|--|
|SwitchId	|2020-12-07 21:04:11	|2020-12-07 21:04:42	|SwitchOver |

Aliyun RDS error log
```
2020-12-07 21:04:13	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 21:04:13	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 21:04:13	FATAL: 57P01: terminating connection due to administrator command
2020-12-07 21:04:23	WARNING: 01000: archive_mode enabled, yet archive_command is not set
2020-12-07 21:04:32	LOG: 00000: postmaster is in PM_STARTUP state.
2020-12-07 21:04:32	LOG: 00000: database system was interrupted; last known up at 2020-12-07 12:51:28 UTC
2020-12-07 21:04:32	LOG: 00000: entering standby mode
2020-12-07 21:04:32	LOG: 00000: database system was not properly shut down; automatic recovery in progress
2020-12-07 21:04:32	LOG: 00000: redo starts at C1/7B001DD8
2020-12-07 21:04:32	LOG: 00000: invalid record length at C1/7D004C10: wanted 24, got 0
2020-12-07 21:04:32	LOG: 00000: postmaster is in PM_RECOVERY state.
2020-12-07 21:04:32	LOG: 00000: consistent recovery state reached at C1/7D004C10
2020-12-07 21:04:32	LOG: 00000: database system is ready to accept read only connections
2020-12-07 21:04:32	LOG: 00000: postmaster is in PM_HOT_STANDBY state.
2020-12-07 21:04:32	LOG: 00000: started streaming WAL from primary at C1/7D000000 on timeline 5

```

##  5.2 - Test 02: execute pg failover when DB are reading on Aliyun Cloud

Test shell script
```
postgres@dba-test-vm-pg12-replicaiton-test-> cat overtime_write_test.sh
#!/bin/sh


aliyun_pg12_service=aliyun_pg12_master_cron
gcp_pg12_service=gcp_cloudsql_pg12_app

for ((i=1; i<=10000; i++))
do
    echo "-- connect ${i} times: os time is `date '+%Y-%m-%d %H:%M:%S'` "
    time_int=`date '+%Y%m%d%H%M%S'`
    radom_char="croninsert"
    insert_sql=`echo "INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( ${time_int} ,?${radom_char}? );" | sed "s/?/'/g"`

    sql_01="select 'aliyun pg rds',* from public.tab_overtime_test order by id desc limit 1;"
    psql service=${aliyun_pg12_service} -c "${insert_sql}" | sed '$d'
    psql service=${aliyun_pg12_service} -t -c "${sql_01}" | sed '$d'

    sql_02="select 'gcp cloudsql pg',* from public.tab_overtime_test order by id desc limit 1;"
    #psql service=${gcp_pg12_service} -c "${insert_sql}" | sed '$d'
    #psql service=${gcp_pg12_service} -t -c "${sql_02}" | sed '$d'

    #date '+%Y-%m-%d %H:%M:%S'
    sleep 1
    echo
done



postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test-> /bin/sh overtime_write_test.sh >> test.log 2>&1
```

### 5.2.1 - Times 01

Operate Time
```
$ date '+%Y-%m-%d %H:%M:%S'
2020-12-07 21:18:37
```

Shell Check status
```
```

RDS主备切换日志：
|切换事件ID	|切换开始时间	|切换结束时间	|切换原因 |
|--|--|--|--|
|SwitchId	|2020-12-07 21:19:37	|2020-12-07 21:20:12	|SwitchOver |

RDS错误日志：
```
2020-12-07 21:20:00	FATAL: XX000: could not receive data from WAL stream: SSL SYSCALL error: EOF detected
2020-12-07 21:20:00	LOG: 00000: record with incorrect prev-link C1/3A001C58 at C1/80001C80
2020-12-07 21:20:00	FATAL: XX000: could not connect to the primary server: server closed the connection unexpectedly	This probably means the server terminated abnormally before or while processing the request.
2020-12-07 21:20:01	ERROR: 25006: cannot execute INSERT in a read-only transaction
2020-12-07 21:20:01	STATEMENT: INSERT INTO tab_cron (time_int, radom_char) VALUES( 07212001 ,'croninsert' );
2020-12-07 21:20:05	LOG: 00000: started streaming WAL from primary at C1/80000000 on timeline 6
2020-12-07 21:20:10	LOG: 00000: promote trigger file found: /data/postgresql.trigger
2020-12-07 21:20:10	FATAL: 57P01: terminating walreceiver process due to administrator command
2020-12-07 21:20:10	LOG: 00000: redo done at C1/80001C48
2020-12-07 21:20:10	LOG: 00000: last completed transaction was at log time 2020-12-07 21:19:42.319675+08
2020-12-07 21:20:10	LOG: 00000: selected new timeline ID: 7
2020-12-07 21:20:10	LOG: 00000: archive recovery complete
2020-12-07 21:20:10	LOG: 00000: checkpoint starting: force
2020-12-07 21:20:10	LOG: 00000: postmaster is in PM_RUN state.
2020-12-07 21:20:10	LOG: 00000: database system is ready to accept connections
2020-12-07 21:20:10	WARNING: 01000: archive_mode enabled, yet archive_command is not set
2020-12-07 21:20:12	LOG: 00000: checkpoint complete: wrote 19 buffers (0.0%); 0 WAL file(s) added, 0 removed, 5 recycled; write=1.905 s, sync=0.003 s, total=1.913 s; sync files=14, longest=0.000 s, average=0.000 s; distance=81919 kB, estimate=81919 kB
2020-12-07 21:21:10	WARNING: 01000: archive_mode enabled, yet archive_command is not set
```


##  5.3 - Test 03: execute pg failover when DB are writing on GCP Cloud


Test shell script
```
postgres@dba-test-vm-pg12-replicaiton-test-> cat overtime_write_test.sh
#!/bin/sh


aliyun_pg12_service=aliyun_pg12_master_cron
gcp_pg12_service=gcp_cloudsql_pg12_app

for ((i=1; i<=10000; i++))
do
    echo "-- connect ${i} times: os time is `date '+%Y-%m-%d %H:%M:%S'` "
    time_int=`date '+%Y%m%d%H%M%S'`
    radom_char="croninsert"
    insert_sql=`echo "INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( ${time_int} ,?${radom_char}? );" | sed "s/?/'/g"`

    sql_01="select 'aliyun pg rds',* from public.tab_overtime_test order by id desc limit 1;"
    #psql service=${aliyun_pg12_service} -c "${insert_sql}" | sed '$d'
    #psql service=${aliyun_pg12_service} -t -c "${sql_01}" | sed '$d'

    sql_02="select 'gcp cloudsql pg',* from public.tab_overtime_test order by id desc limit 1;"
    psql service=${gcp_pg12_service} -c "${insert_sql}" | sed '$d'
    psql service=${gcp_pg12_service} -t -c "${sql_02}" | sed '$d'

    #date '+%Y-%m-%d %H:%M:%S'
    sleep 1
    echo
done



postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test-> /bin/sh overtime_write_test.sh >> test.log 2>&1
```

### 5.3.1 - Times 01

Failover operation in progress. This may take a few minutes. While this operation is running, you may continue to view information about the instance.

Shell Check status
```
-- connect 27 times: os time is 2020-12-07 13:39:39
 gcp cloudsql pg | 46 | 20201207133939 | croninsert | 2020-12-07 13:39:39.646454+00

-- connect 28 times: os time is 2020-12-07 13:39:40
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 37 times: os time is 2020-12-07 13:39:49
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 38 times: os time is 2020-12-07 13:39:50
 gcp cloudsql pg | 47 | 20201207133950 | croninsert | 2020-12-07 13:40:06.028518+00

-- connect 39 times: os time is 2020-12-07 13:40:07
 gcp cloudsql pg | 48 | 20201207134007 | croninsert | 2020-12-07 13:40:07.113807+00

```

Table Check status
```
 43 | 20201207133936 | croninsert | 2020-12-07 13:39:36.492415+00
  44 | 20201207133937 | croninsert | 2020-12-07 13:39:37.542102+00
  45 | 20201207133938 | croninsert | 2020-12-07 13:39:38.595612+00
  46 | 20201207133939 | croninsert | 2020-12-07 13:39:39.646454+00

  47 | 20201207133950 | croninsert | 2020-12-07 13:40:06.028518+00
  48 | 20201207134007 | croninsert | 2020-12-07 13:40:07.113807+00
  49 | 20201207134008 | croninsert | 2020-12-07 13:40:08.178932+00
  50 | 20201207134009 | croninsert | 2020-12-07 13:40:09.237362+00
  51 | 20201207134010 | croninsert | 2020-12-07 13:40:10.291813+00
  52 | 20201207134011 | croninsert | 2020-12-07 13:40:11.345+00
```

GCP log
|Creation Time |Type |Status |
|--|--|--|
|Dec 7, 2020, 9:39:33 PM	|Failover	|Failover finished |


### 5.3.2 - Times 02

Failover Operate
```
dba-test-cloudsql-pg12-master
 dba-test-cloudsql-pg12-master
PostgreSQL 12
Failover operation in progress. This may take a few minutes. While this operation is running, you may continue to view information about the instance.
```

Shell check status
```

-- connect 31 times: os time is 2020-12-07 13:48:44
 gcp cloudsql pg | 176 | 20201207134844 | croninsert | 2020-12-07 13:48:44.396033+00

-- connect 32 times: os time is 2020-12-07 13:48:45
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 44 times: os time is 2020-12-07 13:48:57
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 45 times: os time is 2020-12-07 13:48:58
 gcp cloudsql pg | 177 | 20201207134858 | croninsert | 2020-12-07 13:49:29.832244+00

-- connect 46 times: os time is 2020-12-07 13:49:30
 gcp cloudsql pg | 178 | 20201207134930 | croninsert | 2020-12-07 13:49:30.917551+00

```

Table Check Status
```

 174 | 20201207134842 | croninsert | 2020-12-07 13:48:42.287553+00
 175 | 20201207134843 | croninsert | 2020-12-07 13:48:43.343623+00
 176 | 20201207134844 | croninsert | 2020-12-07 13:48:44.396033+00

 177 | 20201207134858 | croninsert | 2020-12-07 13:49:29.832244+00
 178 | 20201207134930 | croninsert | 2020-12-07 13:49:30.917551+00
 179 | 20201207134931 | croninsert | 2020-12-07 13:49:31.97159+00
 180 | 20201207134933 | croninsert | 2020-12-07 13:49:33.027944+00
 181 | 20201207134934 | croninsert | 2020-12-07 13:49:34.085486+00

```

GCP Cloud SQL log
|Creation Time |Type |Status |
|--|--|--|
|Dec 7, 2020, 9:48:41 PM	|Failover	|Failover finished |



### 5.3.3 - Times 03

Shell check status
```
-- connect 32 times: os time is 2020-12-07 13:53:41
 gcp cloudsql pg | 257 | 20201207135341 | croninsert | 2020-12-07 13:53:41.347685+00

-- connect 33 times: os time is 2020-12-07 13:53:42
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 43 times: os time is 2020-12-07 13:53:52
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 44 times: os time is 2020-12-07 13:53:53
 gcp cloudsql pg | 258 | 20201207135353 | croninsert | 2020-12-07 13:54:08.87221+00
```

Table check status
```
 254 | 20201207135338 | croninsert | 2020-12-07 13:53:38.174928+00
 255 | 20201207135339 | croninsert | 2020-12-07 13:53:39.23311+00
 256 | 20201207135340 | croninsert | 2020-12-07 13:53:40.291614+00
 257 | 20201207135341 | croninsert | 2020-12-07 13:53:41.347685+00
 
 258 | 20201207135353 | croninsert | 2020-12-07 13:54:08.87221+00
 259 | 20201207135409 | croninsert | 2020-12-07 13:54:09.967082+00
 260 | 20201207135411 | croninsert | 2020-12-07 13:54:11.02103+00
 261 | 20201207135412 | croninsert | 2020-12-07 13:54:12.095931+00
 262 | 20201207135413 | croninsert | 2020-12-07 13:54:13.195584+00
```

GCP Cloud SQL log
|Creation Time |Type |Status |
|--|--|--|
|Dec 7, 2020, 9:53:35 PM	|Failover	|Failover operation in progress |
|Dec 7, 2020, 9:53:35 PM	|Failover	|Failover finished |

##  5.4 - Test 04: execute pg failover when DB are reading on GCP Cloud


Test shell script
```
postgres@dba-test-vm-pg12-replicaiton-test-> cat overtime_write_test.sh
#!/bin/sh


aliyun_pg12_service=aliyun_pg12_master_cron
gcp_pg12_service=gcp_cloudsql_pg12_app

for ((i=1; i<=10000; i++))
do
    echo "-- connect ${i} times: os time is `date '+%Y-%m-%d %H:%M:%S'` "
    time_int=`date '+%Y%m%d%H%M%S'`
    radom_char="croninsert"
    insert_sql=`echo "INSERT INTO public.tab_overtime_test (time_int, radom_char) VALUES( ${time_int} ,?${radom_char}? );" | sed "s/?/'/g"`

    sql_01="select 'aliyun pg rds',* from public.tab_overtime_test order by id desc limit 1;"
    psql service=${aliyun_pg12_service} -c "${insert_sql}" | sed '$d'
    psql service=${aliyun_pg12_service} -t -c "${sql_01}" | sed '$d'

    sql_02="select 'gcp cloudsql pg',* from public.tab_overtime_test order by id desc limit 1;"
    #psql service=${gcp_pg12_service} -c "${insert_sql}" | sed '$d'
    psql service=${gcp_pg12_service} -t -c "${sql_02}" | sed '$d'

    #date '+%Y-%m-%d %H:%M:%S'
    sleep 1
    echo
done



postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test->
postgres@dba-test-vm-pg12-replicaiton-test-> /bin/sh overtime_write_test.sh >> test.log 2>&1
```

### 5.4.1 - Times 01

Failover
```
PostgreSQL 12
Failover operation in progress. This may take a few minutes. While this operation is running, you may continue to view information about the instance.
```

Shell Check status
```

-- connect 27 times: os time is 2020-12-07 13:59:02
 gcp cloudsql pg | 300 | 20201207135453 | croninsert | 2020-12-07 13:54:53.44431+00

-- connect 28 times: os time is 2020-12-07 13:59:03
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 37 times: os time is 2020-12-07 13:59:13
psql: error: could not connect to server: could not connect to server: Connection refused
	Is the server running on host "34.96.133.132" and accepting
	TCP/IP connections on port 5432?

-- connect 38 times: os time is 2020-12-07 13:59:14
 gcp cloudsql pg | 300 | 20201207135453 | croninsert | 2020-12-07 13:54:53.44431+00

```

GCP Cloud SQL log
|Creation Time |Type |Status |
|--|--|--|
|Dec 7, 2020, 9:58:57 PM	|Failover	|Failover operation in progress |
|Dec 7, 2020, 9:58:57 PM	|Failover	|Failover finished |


