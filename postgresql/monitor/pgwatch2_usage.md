
# pgwatch2

CYBERTEC PostgreSQL International GmbH
Professional PostgreSQL services since year 2000
the company url is :
https://www.cybertec-postgresql.com/de/

## pgwatch2 github url
https://github.com/cybertec-postgresql/pgwatch2

pgwatch2 is a monitor of postgresql.

Flexible self-contained PostgreSQL metrics monitoring/dashboarding solution. Supports monitoring PG versions 9.0 to 12 out of the box.


## pgwatch2 installing

For the fastest installation / setup experience Docker images are provided via Docker Hub (for a Docker quickstart see here). For doing a custom setup see the "Installing without Docker" paragraph below or turn to the "releases" tab for DEB / RPM / Tar packages.

### fetch and run the latest Docker image, exposing Grafana on port 3000 and administrative web UI on 8080
```
docker run -d -p 3000:3000 -p 8080:8080 -e PW2_TESTDB=true --name pw2 cybertec/pgwatch2
```
docker run -d -p 3001:3000 -p 8080:8080 -e PW2_TESTDB=true --name pw2 cybertec/pgwatch2
docker images
docker ps -a
docker exec --help
docker exec -it {container_id} /bin/sh


After some minutes you could open the "db-overview" dashboard and start looking at metrics. For defining your own dashboards you need to log in as admin (admin/pgwatch2admin). NB! If you don't want to add the "test" database (the pgwatch2 configuration db) for monitoring set the NOTESTDB=1 env parameter when launching the image.

For production setups without a container management framework also "--restart unless-stopped" (or custom startup scripts) is highly recommended. Also exposing the config/metrics database ports for backups and usage of volumes is then recommended to enable easier updating to newer pgwatch2 Docker images without going through the backup/restore procedure described towards the end of README. For maximum flexibility, security and update simplicity though, best would to do a custom setup - see paragraph "Installing without Docker" towards the end of README for that.
```
for v in pg influx grafana pw2 ; do docker volume create $v ; done
# with InfluxDB for metrics storage
docker run -d --name pw2 -v pg:/var/lib/postgresql -v influx:/var/lib/influxdb -v grafana:/var/lib/grafana -v pw2:/pgwatch2/persistent-config -p 8080:8080 -p 3000:3000 -e PW2_TESTDB=true cybertec/pgwatch2
# with Postgres for metrics storage
docker run -d --name pw2 -v pg:/var/lib/postgresql -v grafana:/var/lib/grafana -v pw2:/pgwatch2/persistent-config -p 8080:8080 -p 3000:3000 -e PW2_TESTDB=true cybertec/pgwatch2-postgres
```
For more advanced usecases (production setup with backups) or for easier problemsolving you can decide to expose all services

### run with all ports exposed
```
docker run -d --restart unless-stopped -p 3000:3000 -p 5432:5432 -p 8086:8086 -p 8080:8080 -p 8081:8081 -p 8088:8088 -v ... --name pw2 cybertec/pgwatch2
```
NB! For production usage make sure you also specify listening IPs explicitly (-p IP:host_port:container_port), by default Docker uses 0.0.0.0 (all network devices).

For custom options, more security, or specific component versions one could easily build the image themselves, just Docker needed:

docker build .
For a complete list of all supported Docker environment variables see ENV_VARIABLES.md

## Technical details
Dynamic management of monitored databases, metrics and their intervals - no need to restart/redeploy
Safety
+ Up to 2 concurrent queries per monitored database (thus more per cluster) are allowed
+ Configurable statement timeouts per DB
+ SSL connections support for safe over-the-internet monitoring (use "-e PW2_WEBSSL=1 -e PW2_GRAFANASSL=1" when launching Docker)
+ Optional authentication for the Web UI and Grafana (by default freely accessible)

Backup script (take_backup.sh) provided for taking snapshots of the whole Docker setup. To make it easier (run outside the container) one should to expose ports 5432 (Postgres) and 8088 (InfluxDB backup protocol) at least for the loopback address.

Ports exposed by the Docker image:

5432 - Postgres configuration (or metrics storage) DB
8080 - Management Web UI (monitored hosts, metrics, metrics configurations)
8081 - Gatherer healthcheck / statistics on number of gathered metrics (JSON).
3000 - Grafana dashboarding
8086 - InfluxDB API (when using the InfluxDB version)
8088 - InfluxDB Backup port (when using the InfluxDB version)



## Features
```
Non-invasive setup, no extensions nor superuser rights required for the base functionality
非侵入式安装，使用基础功能不需要扩展，也不需要超级权限

Intuitive metrics presentation using the Grafana dashboarding engine with optional Alerting
使用包含可选报警的Grafana仪表盘，直观地显示指标

Lots of pre-configured dashboards and metric configurations covering all Statistics Collector data
大量地预定义仪表盘和指标配置，涵盖了所有地统计收集数据

Easy extensibility by defining metrics in pure SQL (thus they could also be from business domain)
可以在pure SQL中定义指标进行轻松扩展（因此他们也可以是来自业务领域）

4 supported data stores for metrics storage (PostgreSQL, InfluxDB, Graphite, Prometheus)
可以有4中数据源来支持指标的存储（PostgreSQL，influxDB，Graphite，Prometheus）

Multiple configuration options (YAML, PostgreSQL, ENV) supporting both "push" and "pull" models
多种配置选项（YAML，PostgreSQL，ENV），同时支持 push 推模式和 pull 拉模式

Possible to monitoring all or a subset of DBs of a PostgreSQL cluster
可以监控一个PostgreSQL集群的所有DB，或者部分DB

Global or DB level configuration of metrics/intervals
全局的或DB级别的指标和内部信息配置

Kubernetes/OpenShift ready with sample templates and a Helm chart
通过简单的模板和Helm图表支持 Kubernetes/OpenShift

PgBouncer, AWS RDS and Patroni support
支持PgBouncer, AWS RDS and Patroni

Internal health-check API to monitor metrics gathering status
内部的健康检查API可以监控指标的采集状态

Built-in security with SSL connections and passwords encryption
通过SSL连接和密码加密实现内置安全性

Very low resource requirements for the collector even when monitoring hundreds of DBs
即使监控数百个数据库，收集器的资源需求也非常低

Log parsing capabilities when using local / push mode collector setup. See below for details.
当使用本地模式或push模式安装时，设置日志解析功能。可以看下面的细节。

```

## configure your database
#官方说明：https://github.com/cybertec-postgresql/pgwatch2#steps-to-configure-your-database-for-monitoring

