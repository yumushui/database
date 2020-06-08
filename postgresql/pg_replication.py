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
    
    check the paramter sql is 

    select name,setting from pg_settings where name in ('wal_level', 'archive_mode', 'archive_command', 'max_wal_senders', 'max_replication_slots', 'wal_keep_segments', 'hot_standby');

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
