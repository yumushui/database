#!/usr/bin/env python
#-*- conding:utf-8 -*-

''' The file is used to describe and prictise postgresql replication .'''
print(''' 
    ----------------------------
    # Basic concept 

## Physical Replication
Postgresql support  physical replication begin pg 9.0 , physical replication is also called "Streaming Repication".   
    Streaming Replication use stream to create a same pg instance like primary instance on instance level.
    Streaming Replication has two nodes , Primary Database or Master, Standby Database of Slave .
    Streaming Replication has two type : sync and nosync.

## Logical Replication
Logical Replication is also called Choice Replication, can replicate on table level, but not all tables in database.
    Before pg 10 , the pg not support logical replication. You need the the thired tools, like Slony-I,Londiste,pglogical as so on. PG support logical replication begin pg 10.0 version.

## WAL log
WAL is Write-Ahead Logging logs , is used to record all change of databases.Wal is binary style. When instance is shutdown not normal , the instance can reexecute the change in WAL logs.
    Physical replication and Logical replication is both based on wal log, but they are different. Streaming replication is based on WAL physical replication, but Logical replication is based on WAL logical resolve, resove the wal log to a cleaner and understanding style.

      
''')

''' The compare between phyiscal and logical replication '''
print (''' 
    --------------------------------------------------------------
    ##  The diffrence between Phycial and Logical replicaiton are

    1 the principle different
    physical replication is based wal phycial replication, redo the wal log in standby database.
    logical replication is based wal logical resove, the standby database execute the resolve reuslt sql.

    2 the level different
    the physical replication is the instance level, and the logical can table level.

    3 the DDL different 
    the physical replication can send the DDL on master to slave , and slave can execute DDL automatic. The logical replication will not send DDL to slave.

    4 the Read/Write different
    The physical replication can only read on standby database, but not write on slave . The logical can read and write on standby database.

    5 the Version requst different
    The physical replication must have same big version in master and slave . The logical replication can have different version in master and slave .


''')

''' The asynchronous streaming replication'''
print (''' 
    -------------------------------
    ##  The Asynchoronous streaming replication

    The Asynchoronous streaming replication is means, the master commit the trasacitons not need waiting for the slave give the wal get message.

    To build a steaming replication , You need a full backup on master.
    It has two methods:
    1 copy data file to get master files.
    2 use pg_basebackup command to get master files.

    The setps are:
    
    step 1: add os use and directories
    groupadd postgres
    useradd postgres -g postgres
    passwd postgres
    mkdir -p /u01/pg12/pg_root
    mkdir -p /u01/pg12/pg_tbs
    chown -R postgres.postgres /database/pg12

    setp 2: add postgre use bash_profile
vim /home/postgres/.bash_profile

export PGPORT=5432
export PGUSER=postgres
export PGDATA=/mnt/pg12/pg_root
export LANG=en_US.utf8
export PG_HOME=/opt/pgsql
export LD_LIBRARY_PATH=$PGHOME/lib:/lib64:/usr/lib64:/usr/local/lib64:/lib/:/usr/lib:/usr/local/lib
export PATH=$PGHOME/bin:$PATH:.
export MANPATH=$PGHOME/share/man:$MANPATH
alias rm='rm -i'
alias ll='ls -lh'

the info inf .bash_profile can be changed base the effect.

    step 3: install postgresql software
    yum install -y zlib readline
    tar -zxvf posttresql-12.0.tar.gz
    cd postgresql-12.0
    ./configure --prefix=/opt/pgsql_10.0 --with-pgport=5432
    gmake world
    gmake install-world

    ln -s /opt/pgsql_12.0 /opt/pgsql
    chown -R postgres.postgres /opt/pgsql

    step 4: init the database
    initdb -D /u01/pg12/pg_root -E UTF8 --locale=C -U postgres -W

    step 5: config the paramter

    #wal_level = replica			# minimal, replica, or logical
    #archive_mode = off		# enables archiving; off, on, or always
    #archive_command = ''		# command to use to archive a logfile segment
    #max_wal_senders = 10		# max number of walsender processes
    #max_replication_slots = 10	# max number of replication slots
    #wal_keep_segments = 0		# in logfile segments; 0 disables   #hot_standby = on			# "off" disallows queries during recovery
    #synchronous_commit = on		# synchronization level;
    
    check the paramter sql is 

    select name,setting from pg_settings where name in ('wal_level', 'archive_mode', 'archive_command', 'max_wal_senders', 'max_replication_slots', 'wal_keep_segments', 'hot_standby', 'synchronous_commit');

    after change paramter ,the status is :
local_12_db=# select name,setting from pg_settings where name in ('wal_level', 'archive_mode', 'archive_command', 'max_wal_senders', 'max_replication_slots', 'wal_keep_segments', 'hot_standby');
         name          |  setting
-----------------------+-----------
 archive_command       | /bin/date
 archive_mode          | on
 hot_standby           | on
 max_replication_slots | 30
 max_wal_senders       | 30
 wal_keep_segments     | 128
 wal_level             | logical
(7 rows)

    step 6 : config pg_hab.conf
    add all master and slave configs

    vim pg_hba.conf

# replication privileges.
host    replication repuser 192.168.1.100/32    md5
host    replication repuser 192.168.1.101/32    md5

    step 7 : start and  create replication user
    pg_ctl start -D /u01/pg12/data

    CREATE USER repuser REPLICATION LOGIN CONNECTION LMIMIT 30 ENCRYPTED PASSWORD 're12a345';

    step 8 : online backup master instance

    execute the sql on master to begin backup
    SELECT pg_start_backup('francs_bak1');

    tar -czvf pg_root.tar.gz pg_root --exclude=pg_root/pg_wal
    scp pg_root.tar.gz postgres@192.168.1.101:/u01/pg12
    tar -zxvf pg_root.tar.gz

    after scp the backup, excute the sql on master
    SELECT pg_stop_backup();

    step 9 : create recovery.conf on Slave

    on slave create a new file 
    cp $PGHOME/share/reovery.conf.sample $PGDATA/recovery.conf

    vim recovery.conf

recovery_target_timeline = 'latset'
standby_mode = on
primary_connifo = 'host=192.168.1.100 port=5432 user=repuser'

    the master user password can set in file .pgpass

touch .pgpass
chmod 0600 .pgpass
192.168.1.100:5432:replication:repuser:re12a345
192.168.1.101:5432:replication:repuser:re12a345

    step 10 : start slave instance and check replication
    on slave:
    pg_ctl start -D /u01/pg12/data

    ps -ef|grep post | grep streaming

    on master 
    CREATE TABLE test_replication(id int);
    INSERT INTO test_replication VALUES (1);

    on slave
    SELECT * FROM test_replication;

    if slave can select ,the hot_standby must set on.



''')

''' Use pg_basebackup command to backup and recover database.'''
print (''' 
    the step 8 , backup and scop data files ,can also use pg_basebackup command to commplete.

    on slave 
    pg_ctl stop -m fast
    rm -fr /u01/pg12

    use pg_basebackup tool to make basic bakcup
    pg_basebackup -D /u01/pg12/data -Fp -Xs -v -P -h 192.168.1.100 -p 5432 -U repuser

    on the log , you can get the basebakcup process info.
    cp ~/recovery.conf  $PGDATA
    pg_ctl start

''')

''' Check the replication status '''
print('''
    ---------------------------------
    ## the replication status 

    check info in pg_stat_replication

    SELECT usename, application_name, client, client_addr, sync_state
    FROM pg_stat_replication;

    the sync_state have four choices 
    async : means the slave is asyanc style
    potenital : means the slave is asyanc , if sync node down ,the node can become sync slave
    sync : means the slave is sync style
    quorum : means the slave is quorum standby style
''')


''' The sync replication  '''
print ('''
    ---------------------------------
    ## the synchronous config

    The async and sync replication is different in master commit trasaction, if not waiting the slave has got wal message.

    The main step is the same as async replication ,but same paramter need check and set.

    synchronous_commit 
    the parameter has five choice :
    on
    off
    local
    remote_apply
    remote_write

    IN sigle instance env:
    on : means the local commit need wait the wal log write complete message
    local : means as the on
    off : means will commit not wait the wal log write message, it apply to the data is not very accurate and need more performance.

    IN streaming replication env:
    on : the local wal and the remote wal all complete, the time high
    remote_write : the local wal wait the remote write complete ,the timenot very high
    remote_apply : the local and the remote wal all commplte, the time high

    -- the sync replication config
    ON slave 

    vim recovery.conf
primary_connifo = 'host=192.168.1.100  port=5432 user=repuser application_name=node2'

    ON master

    vim posgresql.conf
synchronous_commit = on / remote_apply
synchronous_standby_names = 'node2'

    pg_ctl relaod
    pg_ctl restart -m fast

    SELECT usename, application_name, client_addr, sync_state
    FROM pg_stat_replication;

    the sync_state is : sync

    The prod instance , synchronous_commit should set : off

      
''')

''' The practise on Mac OS '''
print ('''
    The pg 12 install step also can be :
    Steps to set up Streaming Replication in PostgreSQL 12

install software

step 1
init the primary instance
## Preparing the environment
$ sudo su - postgres
$ echo "export PATH=/usr/pgsql-12/bin:$PATH PAGER=less" >> ~/.pgsql_profile
$ source ~/.pgsql_profile
 
## As root, initialize and start PostgreSQL 12 on the Master
$ /usr/pgsql-12/bin/postgresql-12-setup initdb
$ systemctl start postgresql-12

step 2 
set the primary listen_addresses
# as postgres
$ psql -c "ALTER SYSTEM SET listen_addresses TO '*'";
ALTER SYSTEM
 
# as root, restart the service
$ systemctl restart postgresql-12

step 3
create replication use 
postgres=# CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secret';
CREATE ROLE

step 4
add replication rules in pg_hba.conf
$ echo "host replication replicator 192.168.0.107/32 md5" >> $PGDATA/pg_hba.conf
 
## Get the changes into effect through a reload.
 
$ psql -c "select pg_reload_conf()"

step 5
use pg_basebackup to get the primary instance

## This command must be executed on the standby server.
$ pg_basebackup -h 192.168.0.108 -U replicator -p 5432 -D $PGDATA -Fp -Xs -P -R
Password:
25314/25314 kB (100%), 1/1 tablespace
$ touch $PGDATA/standby.signal

$ ls -l $PGDATA

$ cat $PGDATA/postgresql.auto.conf
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.
listen_addresses = '*'
primary_conninfo = 'user=replicator password=secret host=192.168.0.108 port=5432 sslmode=prefer sslcompression=0 gssencmode=prefe


-- In fact, I execute the command like this :
pg_basebackup -D /Users/feixiang.zhao/My_data/pgdata_12_6432/data -Fp -Xs -v -P -R -h 10.10.138.28 -p 5432 -U rep_user 
re12a345

sed -i 's/5432/6432/g' ${PG_DATA}/postgresql.conf

step 6
start the standby instance
$ pg_ctl -D $PGDATA start

step 7
check the preplication status
$ psql -x -c "select * from pg_stat_replication"

      
In the install process , there is serval errors.
--  出现问题时，从谷歌搜索了创建过程
https://www.percona.com/blog/2019/10/11/how-to-set-up-streaming-replication-in-postgresql-12/

对比发现两个问题，
replication 搭建到要点  pg_basebackup 备份时要加 -R参数，
这样在 pg 12之前会自动生成备份恢复文件 recover.conf
在 pg 12版本，会增加两个修改： 产生一个标志为 standby到空文件 standby.signal 表示为从库；
将 primary_conninfo 参数，自动修改到 postgresql.conf 中；
如果备份时没有使用 -R 参数，则 standby.signal 要手动创建， primary_conninfo 参数手动修改。
有了这两个条件，在启动 pg 12的新实例时，才会自动创建replication关系。

-- 从库关系创建后，复制未成功，有报错
在从库的日志中，有下面的提示：
2020-06-09 11:19:29.634 CST [41240]    2020-06-09 11:19:29 CSTLOG:  started streaming WAL from primary at 0/8000000 on timeline 1
2020-06-09 11:19:29.635 CST [41240]    2020-06-09 11:19:29 CSTFATAL:  could not receive data from WAL stream: ERROR:  requested starting point 0/8000000 is ahead of the WAL flush position of this server 0/6000148

google 上给你的解决方案是，重做

''')


print(
'''
复制延迟监控
注意9.6和10之间有明显的差别

# Database replication statistics
# Add more labels & more metrics, compatible with default metrics
pg_replication:
  query: "SELECT
            client_addr,
            application_name,
            sent_lsn - '0/0'                AS sent_lsn,
            write_lsn - '0/0'               AS write_lsn,
            flush_lsn - '0/0'               AS flush_lsn,
            replay_lsn - '0/0'              AS replay_lsn,
            extract(EPOCH FROM write_lag)   AS write_lag,
            extract(EPOCH FROM flush_lag)   AS flush_lag,
            extract(EPOCH FROM replay_lag)  AS replay_lag,
            CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) :: FLOAT END AS replay_diff,
            CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) :: FLOAT END AS  flush_diff,
            CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) :: FLOAT END AS  write_diff,
            sync_priority
          FROM pg_stat_replication;"


-- 在  .psqlrc 中的格式为

复制延迟监控
注意9.6和10之间有明显的差别

# Database replication statistics
# Add more labels & more metrics, compatible with default metrics
pg_replication:
  query: "
  
SELECT client_addr, application_name, sent_lsn - '0/0' AS sent_lsn, write_lsn - '0/0' AS write_lsn, flush_lsn - '0/0' AS flush_lsn, replay_lsn - '0/0' AS replay_lsn, extract(EPOCH FROM write_lag) AS write_lag, extract(EPOCH FROM flush_lag)  AS flush_lag, extract(EPOCH FROM replay_lag)  AS replay_lag, CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) :: FLOAT END AS replay_diff, CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) :: FLOAT END AS  flush_diff, CASE WHEN pg_is_in_recovery() THEN NULL ELSE pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) :: FLOAT END AS  write_diff, sync_priority FROM pg_stat_replication;
          
          "
postgresql 10.x 叫做 wal、lsn
postgresql 9.x 叫做 xlog、location

在实际应用中经常需要根据 lsn/location 获取 wal/xlog 文件名

postgresql 10.x
postgres=# select pg_current_wal_lsn();
 pg_current_wal_lsn 
--------------------
 0/1656FE0
(1 row)

postgres=# select pg_current_wal_lsn(),
                  pg_walfile_name(pg_current_wal_lsn()),
                  pg_walfile_name_offset(pg_current_wal_lsn());

 pg_current_wal_lsn |     pg_walfile_name      |       pg_walfile_name_offset   
    
--------------------+--------------------------+------------------------------------
 0/1656FE0          | 000000010000000000000001 | (000000010000000000000001,6647776)
(1 row)


postgresql 9.x
postgres=# select pg_current_xlog_location();
 pg_current_xlog_location 
--------------------------
 596/C4DA2000
(1 row)

postgres=# select pg_current_xlog_location(),
                  pg_xlogfile_name(pg_current_xlog_location()),
                  pg_xlogfile_name_offset(pg_current_xlog_location());
                  
 pg_current_xlog_location |     pg_xlogfile_name     |       pg_xlogfile_name_offset       
--------------------------+--------------------------+-------------------------------------
 596/C4DA2000             | 0000000100000596000000C4 | (0000000100000596000000C4,14295040)

(1 row)


pg日志与日志号，可参考文章：
https://www.it610.com/article/1282854545679990784.htm

postgres--流复制

从库查询
SELECT pg_is_in_recovery();
SELECT pg_is_wal_replay_paused();
SELECT pg_last_wal_receive_lsn();
SELECT pg_last_wal_replay_lsn();
SELECT * FROM pg_stat_get_wal_receiver();
SELECT * FROM pg_stat_wal_receiver ;


设置
\set wal_receiver 'SELECT pg_is_in_recovery(); SELECT pg_is_wal_replay_paused(); SELECT pg_last_wal_receive_lsn(); SELECT pg_last_wal_replay_lsn(); SELECT * FROM pg_stat_get_wal_receiver(); SELECT * FROM pg_stat_wal_receiver;'


'''
)