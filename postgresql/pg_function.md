##  Postgresql Function

https://www.postgresql.org/docs/12/sql-createfunction.html

CREATE FUNCTION — define a new function

Synopsis
CREATE [ OR REPLACE ] FUNCTION
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_name column_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | IMMUTABLE | STABLE | VOLATILE | [ NOT ] LEAKPROOF
    | CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT
    | [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SUPPORT support_function
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
  } ...



##  create a function to add partition

the add partition sql:

CREATE TABLE public.historic_price_2020_12  PARTITION OF public.historic_price FOR VALUES FROM (1606780800000::bigint) TO (1609459200000::bigint);

CREATE TABLE public.historic_price_2021_01  PARTITION OF public.historic_price FOR VALUES FROM (1609459200000::bigint) TO (1612137600000::bigint);


CREATE TABLE public.time_series_2020_12  PARTITION OF public.time_series FOR VALUES FROM (1606780800000::bigint) TO (1609459200000::bigint);

CREATE TABLE public.time_series_2021_01  PARTITION OF public.time_series FOR VALUES FROM (1609459200000::bigint) TO (1612137600000::bigint);


CREATE TRIGGER time_series_rolling_insert_trigger BEFORE INSERT ON public.time_series_2020_12 FOR EACH ROW EXECUTE PROCEDURE partitioned.create_timeseries_rolling_insert();

CREATE TRIGGER time_series_rolling_insert_trigger BEFORE INSERT ON public.time_series_2021_01 FOR EACH ROW EXECUTE PROCEDURE partitioned.create_timeseries_rolling_insert();


CREATE FUNCTION partitioned.create_timeseries_rolling_partition_and_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
    DECLARE
      partition_date TEXT;
      partition_suffix TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_1 TEXT;
      partition_date_month_2 TEXT;
      partition_parent_table TEXT;
      partition_column TEXT;

    BEGIN
      -- partition_date := to_char((to_timestamp(NEW.captured_at/1000) AT TIME ZONE 'UTC')::date,'YYYY_MM_DD');
      partition_parent_table := public.historic_price
      partition_column := created_at
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_1 := to_char((now() AT TIME ZONE 'UTC' + interval '1 month')::date,'YYYY_MM');
      partition_date_month_2 := to_char((now() AT TIME ZONE 'UTC' + interval '2 month')::date,'YYYY_MM');

      -- partition_suffix := NEW.series || '_' || partition_date;
      partition := partition_parent_table || '_' || partition_date_month;
      partition_next := partition_parent_table || '_' || partition_date_month_1;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE 'do $$
                        begin IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition || ''')
                        then
                        -- LOCK TABLE partitioned.lock_table_time_series_rolling IN EXCLUSIVE MODE;

                        CREATE TABLE public. ' || partition
                          || 'PARTITION OF ' || partition_parent_table || 'FOR VALUES FROM ( '
                          || '(extract(epoch from (( ''' || partition_date_month || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ') TO ('
                          || '(extract(epoch from (( ''' || partition_date_month_1 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ');
      END IF;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE 'do $$
                        begin IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition_next || ''')
                        then
                        -- LOCK TABLE partitioned.lock_table_time_series_rolling IN EXCLUSIVE MODE;

                        CREATE TABLE public. ' || partition_next
                          || 'PARTITION OF ' || partition_parent_table || 'FOR VALUES FROM ( '
                          || '(extract(epoch from (( ''' || partition_date_month_1 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ') TO ('
                          || '(extract(epoch from (( ''' || partition_date_month_2 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ');

      END IF;
      RETURN NULL;
    END;
  $_$;





CREATE FUNCTION partitioned.create_timeseries_rolling_partition_and_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $_$
    DECLARE
      partition_date TEXT;
      partition_suffix TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_1 TEXT;
      partition_date_month_2 TEXT;
      partition_parent_table TEXT;
      partition_column TEXT;

    BEGIN
      -- partition_date := to_char((to_timestamp(NEW.captured_at/1000) AT TIME ZONE 'UTC')::date,'YYYY_MM_DD');
      partition_parent_table := public.historic_price
      partition_column := created_at
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_1 := to_char((now() AT TIME ZONE 'UTC' + interval '1 month')::date,'YYYY_MM');
      partition_date_month_2 := to_char((now() AT TIME ZONE 'UTC' + interval '2 month')::date,'YYYY_MM');

      -- partition_suffix := NEW.series || '_' || partition_date;
      partition := partition_parent_table || '_' || partition_date_month;
      partition_next := partition_parent_table || '_' || partition_date_month_1;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE 'do $$
                        begin IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition || ''')
                        then
                        -- LOCK TABLE partitioned.lock_table_time_series_rolling IN EXCLUSIVE MODE;

                        CREATE TABLE public. ' || partition
                          || 'PARTITION OF ' || partition_parent_table || 'FOR VALUES FROM ( '
                          || '(extract(epoch from (( ''' || partition_date_month || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ') TO ('
                          || '(extract(epoch from (( ''' || partition_date_month_1 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ');

                        IF to_regclass(''partitioned.idx_time_series_at_ccy_series_bid_ask_' || partition_suffix || ''') IS NULL then
                        CREATE INDEX idx_time_series_at_ccy_series_bid_ask_' || partition_suffix ||
                                  ' ON partitioned.' || partition || ' (captured_at, ccy_pair, series, (bid ->> ''type''), (ask ->> ''type'')); end if;
                        end if; end $$';
      END IF;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE 'do $$
                        begin IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition_next || ''')
                        then
                        -- LOCK TABLE partitioned.lock_table_time_series_rolling IN EXCLUSIVE MODE;

                        CREATE TABLE public. ' || partition_next
                          || 'PARTITION OF ' || partition_parent_table || 'FOR VALUES FROM ( '
                          || '(extract(epoch from (( ''' || partition_date_month_1 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ') TO ('
                          || '(extract(epoch from (( ''' || partition_date_month_2 || '-01 00:00:00 ''' || ')::timestamp  AT TIME ZONE 'UTC') ) * 1000)
                          || ');

                        IF to_regclass(''partitioned.idx_time_series_at_ccy_series_bid_ask_' || partition_suffix || ''') IS NULL then
                        CREATE INDEX idx_time_series_at_ccy_series_bid_ask_' || partition_suffix ||
                                  ' ON partitioned.' || partition || ' (captured_at, ccy_pair, series, (bid ->> ''type''), (ask ->> ''type'')); end if;
                        end if; end $$';
      END IF;
      RETURN NULL;
    END;
  $_$;



##  The documentation
https://www.postgresql.org/docs/12/plpgsql.html


Chapter 42. PL/pgSQL - SQL Procedural Language  SQL过程语言
Table of Contents

42.1. Overview  概述
  42.1.1. Advantages of Using PL/pgSQL  使用PL/pgSQL的优势
  42.1.2. Supported Argument and Result Data Types  支持的观点和结果数据类型
42.2. Structure of PL/pgSQL   PL/pgSQL的结构
42.3. Declarations    声明
  42.3.1. Declaring Function Parameters   声明函数参数
  42.3.2. ALIAS    别名
  42.3.3. Copying Types   拷贝类型
  42.3.4. Row Types   行类型
  42.3.5. Record Types  记录类型
  42.3.6. Collation of PL/pgSQL Variables  PL/pgSQL的校对
42.4. Expressions    表达式
42.5. Basic Statements  基础语句
  42.5.1. Assignment   作业
  42.5.2. Executing a Command with No Result  执行一个不返回结果的命令
  42.5.3. Executing a Query with a Single-Row Result  执行一个只有一行结果的查询
  42.5.4. Executing Dynamic Commands    执行动态命令
  42.5.5. Obtaining the Result Status   获得结果状态
  42.5.6. Doing Nothing At All   什么也不做
42.6. Control Structures  控制结构
  42.6.1. Returning from a Function   一个函数的返回
  42.6.2. Returning from a Procedure  一个存储过程的返回
  42.6.3. Calling a Procedure    调用一个存储过程
  42.6.4. Conditionals    有条件的
  42.6.5. Simple Loops    简单的循环
  42.6.6. Looping through Query Results   通过查询结果循环
  42.6.7. Looping through Arrays     通过数组循环
  42.6.8. Trapping Errors      诱捕错误
  42.6.9. Obtaining Execution Location Information   获取执行位置信息
42.7. Cursors   游标
  42.7.1. Declaring Cursor Variables   声明游标变量
  42.7.2. Opening Cursors   打开游标
  42.7.3. Using Cursors     使用游标
  42.7.4. Looping through a Cursor's Result  通过一个游标的结果进行循环
42.8. Transaction Management  事务管理
42.9. Errors and Messages   错误和信息
  42.9.1. Reporting Errors and Messages   提示错误和信息
  42.9.2. Checking Assertions    检查断言
42.10. Trigger Functions    触发器函数
  42.10.1. Triggers on Data Changes   在数据改变时的触发器
  42.10.2. Triggers on Events     事件上的触发器
42.11. PL/pgSQL under the Hood   在帽子下的 PL/pgSQL 
  42.11.1. Variable Substitution  参数替代
  42.11.2. Plan Caching    计划缓存
42.12. Tips for Developing in PL/pgSQL   在 PL/pgSQL开发中的注意点
  42.12.1. Handling of Quotation Marks   括号的处理 
  42.12.2. Additional Compile-Time and Run-Time Checks  其他编译时和运行时的检查
42.13. Porting from Oracle PL/SQL   移植Oracle的 PL/SQL
  42.13.1. Porting Examples   移植示例
  42.13.2. Other Things to Watch For  其他需要注意的事情
  42.13.3. Appendix   附录

  

