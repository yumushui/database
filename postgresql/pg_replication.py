#!/usr/bin/env python
#-*- conding:utf-8 -*-

''' The file is used to describe and prictise postgresql replication .'''
print(''' 
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
       The diffrence between Phycial and Logical replicaiton are
    1 the principle different
    physical replication is based wal phycial replication, redo the wal log in standby database.
    logical replication is based wal logical resove, the standby database execute the resolve reuslt sql.

    2 the level different
    the physical replication is the instance level, and the logical can table level.

    3 the DDL different 
    the physical replication can send the DDL on master to slave , and slave can execute DDL automatic. The logical replication will not send DDL to slave.

    4 the Read/Write different
    The physical replication can only read on standby database, but not write on salve . The logical can read and write on standby database.

    5 the Version requst different
    The physical replication must have same big version in master and slave . The logical replication can have different version in master and slave .


''')
