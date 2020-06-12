#!/usr/bin/env python
# -*- conding:utf-8 -*-

''' pg_dump dump usage '''
print ('''
On a running postgresql instance, there are to backup method :
1 logical backup , dump the data to a sql file
2 use transaction log 

''')

''' execue the pg_dump command '''
print ('''
if dump a postgresql instance：
# pg_dump test > /tmp/dump.sql

# pg_dump -U backup_user test > /tmp/dump.sql
pg_dump --help


''')

''' give the user info method '''
print ('''
    when use pg_dump of psql connect the pg instance , the use info can have three method :
    1 use the envirement parameter
    2 use .pgpass
    3 use servcie file


## 1 use the envirement parameter

export PGHOST=
expprt PGPORT=
export PGUSER=
export PGPASSWORD=
export PGDATEABASE=

psql
pgdump


##  2 use .pgpass

vim ~/.pgpass

hostname:port:database:username:password
192.168.1.100:5432:mydb:user01:123456

chmod 0600 ~/.pgpass

Windows OS :  %APPDATEA%\postgresql\pgpass.conf


##  3 use  .pg_service.conf

vim .pg_service.conf

# a sample service
[handservice]
host=localhost
port=5432
dbname=test
user=hs
password=abc

[paulservice]
host=192.168.1.100
port=5432
dbname=xyz
user=paul
password=cde

export PGSERVICE=handservice
psql

psql service=handservice


''')

''' the pg_dump option '''
print ('''
       pg_dump dump specifice objects:
-a  : only dump data not dump structure
-s  : only dump structure not dump data
-n  : only dump the specifice schema
-N  : only not dump the specifice schema
-t  : only dump the specifice table
-T  : dump all things but not the specifice table

    pu_dump outfile format :
  -F, --format=c|d|t|p         output file format (custom, directory, tar,
                               plain text (default))

-Fc : the outfile is custom format , can not read ,but have samller space and can use more process 
-Fd : the outfile is a directory
-Ft : the outfile is a tar file
-Fp : the outfile is plain sql file , but pg_dump only can word on a signal process


pg_dump -Fc test > /tmp/dump.fc
pg_dump -Fc test -f > /tmp/dump.fc

pg_restore --list /tmp/dump.fc
''')


''' redo the backup '''
print ('''
    ## restore the backup file

       if the dump file is sql file ,restore is :
psql new_db < dump_file.sql

       if the dump file is Fc file ,resotre is :
pg_restore -d new_db -j 4 /tmp/dump.fc


''')

''' dump the pg instance global data '''
print (''' 
    pg_dump on work on database level , if backup the whole instance , must use pg_dumpall . but pg_dumpall can only work in one single instance.

    -- pg_dumpall all things
pg_dumpall > /tmp/all.sql

    -- pg_dumpall only dump global info
pg_dumpall -g > /tmp/global_info.sql

    -- at the most case , use pg_dumpall backup global ,pg_dump backup db

#/bin/sh

BACKUP_DIR=/tmp/
pg_dumpall -g > ${BACKUP_DIR}/global.sql

db_list=`psql -A -t postgres -c "SELECT datname FROM pg_database
       WHERE datname NOT IN ('postgres', 'template0', 'template1')"`

fox x in ${db_list}
do
    pg_dump -Fc -${x} > ${BACKUP_DIR}/${x}.fc
done

''')

