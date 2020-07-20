
# mysql image on Docker hub

https://hub.docker.com/_/mysql

## Support tags and respective Dockerfile links
```
8.0.21, 8.0, 8, latest
5.7.31, 5.7, 5
5.6.49, 5.6
```

## Quick reference (cont.)
Where to file issues: https://github.com/docker-library/mysql/issues

Supported architectures: (more info) amd64

Published image artifact details: repo-info repo's repos/mysql/ directory (history) (image metadata, transfer size, etc)

Image updates: official-images PRs with label library/mysql
official-images repo's library/mysql file (history)

Source of this description: docs repo's mysql/ directory (history)

## Get and Run mysql 5.7 env

The steps are :
+ get mysql 5.7 docker image
    docker search mysql
    docker pull mysql:5.7.31
+ run mysql 4.7 docker container
    docker run --name mysql5.7.31 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7.31
+ use exec to connect docker container
    docker images
    docker ps -a
    docker container exec -it e4e688bdb75c /bin/bash
+ use mysql to connect mysql instance
    mysql -h 127.0.0.1 -P 3306 -u root -p
+ after testing, use docker container stop to stop the container
    docker container stop e4e688bdb75c
    docker ps -a
+ use docker container rm  to rm the container
    docker container rm e4e688bdb75c
    docker ps -a

```
feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker search mysql
NAME                              DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
mysql                             MySQL is a widely used, open-source relation…   9740                [OK]
mariadb                           MariaDB is a community-developed fork of MyS…   3554                [OK]
mysql/mysql-server                Optimized MySQL Server Docker images. Create…   713                                     [OK]
centos/mysql-57-centos7           MySQL 5.7 SQL database server                   77
mysql/mysql-cluster               Experimental MySQL Cluster Docker images. Cr…   73
centurylink/mysql                 Image containing mysql. Optimized to be link…   61                                      [OK]
bitnami/mysql                     Bitnami MySQL Docker Image                      44                                      [OK]
deitch/mysql-backup               REPLACED! Please use http://hub.docker.com/r…   41                                      [OK]
tutum/mysql                       Base docker image to run a MySQL database se…   35
schickling/mysql-backup-s3        Backup MySQL to S3 (supports periodic backup…   30                                      [OK]
prom/mysqld-exporter                                                              29                                      [OK]
databack/mysql-backup             Back up mysql databases to... anywhere!         27
linuxserver/mysql                 A Mysql container, brought to you by LinuxSe…   25
centos/mysql-56-centos7           MySQL 5.6 SQL database server                   19
circleci/mysql                    MySQL is a widely used, open-source relation…   19
mysql/mysql-router                MySQL Router provides transparent routing be…   16
arey/mysql-client                 Run a MySQL client from a docker container      14                                      [OK]
fradelg/mysql-cron-backup         MySQL/MariaDB database backup using cron tas…   8                                       [OK]
openshift/mysql-55-centos7        DEPRECATED: A Centos7 based MySQL v5.5 image…   6
genschsa/mysql-employees          MySQL Employee Sample Database                  5                                       [OK]
devilbox/mysql                    Retagged MySQL, MariaDB and PerconaDB offici…   3
ansibleplaybookbundle/mysql-apb   An APB which deploys RHSCL MySQL                2                                       [OK]
jelastic/mysql                    An image of the MySQL database server mainta…   1
widdpim/mysql-client              Dockerized MySQL Client (5.7) including Curl…   1                                       [OK]
monasca/mysql-init                A minimal decoupled init container for mysql    0

 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS              PORTS                                                                                              NAMES
1d4122714460        cybertec/pgwatch2                               "/pgwatch2/docker-la…"   5 hours ago         Up 5 hours          5432/tcp, 8081/tcp, 8086/tcp, 8088/tcp, 9187/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:3001->3000/tcp   pw2
5a598b8dc65c        registry.airwallex.com/awx-postgres-dev:10.6    "docker-entrypoint.s…"   43 hours ago        Up 43 hours         5432/tcp, 0.0.0.0:8432->8432/tcp                                                                   my_postgres_10
0dcbfadfb5fa        registry.airwallex.com/awx-postgres-dev:9.6.8   "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:7432->7432/tcp                                                                   my_postgres
f4ded355e787        postgres                                        "docker-entrypoint.s…"   46 hours ago        Up 46 hours         5432/tcp                                                                                           5d1c525ad2d5
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 

 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker images
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
cybertec/pgwatch2                         latest              9ee3aefae9ca        6 days ago          1.2GB
registry.airwallex.com/awx-postgres-dev   10.6                394cde18ba1b        2 weeks ago         230MB
postgres                                  latest              b97bae343e06        5 weeks ago         313MB
asia.gcr.io/airwallex/alpine              3                   cc0abc535e36        6 months ago        5.59MB
registry.airwallex.com/awx-postgres-dev   9.6.8               5d1c525ad2d5        13 months ago       234MB
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 

 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 

 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker run --name mysql5.7.31 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7.31
Unable to find image 'mysql:5.7.31' locally
5.7.31: Pulling from library/mysql
8559a31e96f4: Already exists
d51ce1c2e575: Pull complete
c2344adc4858: Pull complete
fcf3ceff18fc: Pull complete
16da0c38dc5b: Pull complete
b905d1797e97: Pull complete
4b50d1c6b05c: Pull complete
0a52a5c57cd9: Pull complete
3b816a39d367: Pull complete
13ee22d6b3bb: Pull complete
e517c3d2ba35: Pull complete
Digest: sha256:ea560da3b6f2f3ad79fd76652cb9031407c5112246a6fb5724ea895e95d74032
Status: Downloaded newer image for mysql:5.7.31
e4e688bdb75c0568bc3290a70c5427e8c757540f7b68eeafedfc211d89e438b8
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 


 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker images
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
mysql                                     5.7.31              d05c76dbbfcf        3 days ago          448MB
cybertec/pgwatch2                         latest              9ee3aefae9ca        6 days ago          1.2GB
registry.airwallex.com/awx-postgres-dev   10.6                394cde18ba1b        2 weeks ago         230MB
postgres                                  latest              b97bae343e06        5 weeks ago         313MB
asia.gcr.io/airwallex/alpine              3                   cc0abc535e36        6 months ago        5.59MB
registry.airwallex.com/awx-postgres-dev   9.6.8               5d1c525ad2d5        13 months ago       234MB
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS              PORTS                                                                                              NAMES
e4e688bdb75c        mysql:5.7.31                                    "docker-entrypoint.s…"   25 seconds ago      Up 25 seconds       3306/tcp, 33060/tcp                                                                                mysql5.7.31
1d4122714460        cybertec/pgwatch2                               "/pgwatch2/docker-la…"   5 hours ago         Up 5 hours          5432/tcp, 8081/tcp, 8086/tcp, 8088/tcp, 9187/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:3001->3000/tcp   pw2
5a598b8dc65c        registry.airwallex.com/awx-postgres-dev:10.6    "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:8432->8432/tcp                                                                   my_postgres_10
0dcbfadfb5fa        registry.airwallex.com/awx-postgres-dev:9.6.8   "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:7432->7432/tcp                                                                   my_postgres
f4ded355e787        postgres                                        "docker-entrypoint.s…"   46 hours ago        Up 46 hours         5432/tcp                                                                                           5d1c525ad2d5
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker container exec -it e4e688bdb75c /bin/bash
root@e4e688bdb75c:/# df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  4.3G   52G   8% /
tmpfs            64M     0   64M   0% /dev
tmpfs           996M     0  996M   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
/dev/vda1        59G  4.3G   52G   8% /etc/hosts
tmpfs           996M     0  996M   0% /proc/acpi
tmpfs           996M     0  996M   0% /sys/firmware
root@e4e688bdb75c:/# mysql
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
root@e4e688bdb75c:/# ps -ef|grep mysql
bash: ps: command not found
root@e4e688bdb75c:/# mysql -h localhost -P 3306 -u root
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
root@e4e688bdb75c:/# mysql -h localhost -P 3306 -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.31 MySQL Community Server (GPL)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql>
mysql> exit
Bye

root@e4e688bdb75c:/# exit
exit
 ✘ feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 ✘ feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  ls
README.md admin     dev       img       misc      mon       pit       sql       src       test      tools

 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS              PORTS                                                                                              NAMES
e4e688bdb75c        mysql:5.7.31                                    "docker-entrypoint.s…"   9 minutes ago       Up 9 minutes        3306/tcp, 33060/tcp                                                                                mysql5.7.31
1d4122714460        cybertec/pgwatch2                               "/pgwatch2/docker-la…"   5 hours ago         Up 5 hours          5432/tcp, 8081/tcp, 8086/tcp, 8088/tcp, 9187/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:3001->3000/tcp   pw2
5a598b8dc65c        registry.airwallex.com/awx-postgres-dev:10.6    "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:8432->8432/tcp                                                                   my_postgres_10
0dcbfadfb5fa        registry.airwallex.com/awx-postgres-dev:9.6.8   "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:7432->7432/tcp                                                                   my_postgres
f4ded355e787        postgres                                        "docker-entrypoint.s…"   46 hours ago        Up 46 hours         5432/tcp                                                                                           5d1c525ad2d5
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker container stop e4e688bdb75c
e4e688bdb75c
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS                     PORTS                                                                                              NAMES
e4e688bdb75c        mysql:5.7.31                                    "docker-entrypoint.s…"   9 minutes ago       Exited (0) 6 seconds ago                                                                                                      mysql5.7.31
1d4122714460        cybertec/pgwatch2                               "/pgwatch2/docker-la…"   5 hours ago         Up 5 hours                 5432/tcp, 8081/tcp, 8086/tcp, 8088/tcp, 9187/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:3001->3000/tcp   pw2
5a598b8dc65c        registry.airwallex.com/awx-postgres-dev:10.6    "docker-entrypoint.s…"   44 hours ago        Up 44 hours                5432/tcp, 0.0.0.0:8432->8432/tcp                                                                   my_postgres_10
0dcbfadfb5fa        registry.airwallex.com/awx-postgres-dev:9.6.8   "docker-entrypoint.s…"   44 hours ago        Up 44 hours                5432/tcp, 0.0.0.0:7432->7432/tcp                                                                   my_postgres
f4ded355e787        postgres                                        "docker-entrypoint.s…"   46 hours ago        Up 46 hours                5432/tcp                                                                                           5d1c525ad2d5
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker container rm e4e688bdb75c
e4e688bdb75c
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master  docker ps -a
CONTAINER ID        IMAGE                                           COMMAND                  CREATED             STATUS              PORTS                                                                                              NAMES
1d4122714460        cybertec/pgwatch2                               "/pgwatch2/docker-la…"   5 hours ago         Up 5 hours          5432/tcp, 8081/tcp, 8086/tcp, 8088/tcp, 9187/tcp, 0.0.0.0:8080->8080/tcp, 0.0.0.0:3001->3000/tcp   pw2
5a598b8dc65c        registry.airwallex.com/awx-postgres-dev:10.6    "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:8432->8432/tcp                                                                   my_postgres_10
0dcbfadfb5fa        registry.airwallex.com/awx-postgres-dev:9.6.8   "docker-entrypoint.s…"   44 hours ago        Up 44 hours         5432/tcp, 0.0.0.0:7432->7432/tcp                                                                   my_postgres
f4ded355e787        postgres                                        "docker-entrypoint.s…"   46 hours ago        Up 46 hours         5432/tcp                                                                                           5d1c525ad2d5
 feixiang.zhao@KZYH-PC-000213  ~/My_github/pg   master 
```

## Get and Run mysql 8.0 env

The steps are :
+ get mysql 5.7 docker image
    docker search mysql
    docker pull mysql:5.7.31
+ run mysql 4.7 docker container
    docker run --name mysql5.7.31 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7.31
+ use exec to connect docker container
    docker images
    docker ps -a
    docker container exec -it e4e688bdb75c /bin/bash
+ use mysql to connect mysql instance
    mysql -h 127.0.0.1 -P 3306 -u root -p
+ after testing, use docker container stop to stop the container
    docker container stop e4e688bdb75c
    docker ps -a
+ use docker container rm  to rm the container
    docker container rm e4e688bdb75c
    docker ps -a

