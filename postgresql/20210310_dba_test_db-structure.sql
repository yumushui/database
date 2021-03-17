--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: partitioned; Type: SCHEMA; Schema: -; Owner: dba_test_db_admin
--

CREATE SCHEMA partitioned;


ALTER SCHEMA partitioned OWNER TO dba_test_db_admin;

--
-- Name: hstore; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public;


--
-- Name: EXTENSION hstore; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION hstore IS 'data type for storing sets of (key, value) pairs';


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_stat_statements IS 'track execution statistics of all SQL statements executed';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: create_timeseries_rolling_insert(); Type: FUNCTION; Schema: partitioned; Owner: dba_test_db_admin
--

CREATE FUNCTION partitioned.create_timeseries_rolling_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  INSERT into partitioned.time_series_rolling (id, captured_at, series, ccy_pair, style, bid, ask, mid, ref_mid)
  values (new.id, new.captured_at, new.series, new.ccy_pair, new.style, new.bid, new.ask, new.mid, new.ref_mid);

  RETURN new;
END;
$$;


ALTER FUNCTION partitioned.create_timeseries_rolling_insert() OWNER TO dba_test_db_admin;

--
-- Name: add_three_values(anyelement, anyelement, anyelement); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.add_three_values(v1 anyelement, v2 anyelement, v3 anyelement) RETURNS anyelement
    LANGUAGE plpgsql
    AS $_$
DECLARE
    result ALIAS FOR $0;
BEGIN
    result := v1 + v2 + v3;
    RETURN result;
END;
$_$;


ALTER FUNCTION public.add_three_values(v1 anyelement, v2 anyelement, v3 anyelement) OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition(); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition() RETURNS integer
    LANGUAGE plpgsql
    AS $$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
    BEGIN
      parent_table := 'historic_price';
      partition_key := 'created_at';
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval '1 month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
                  CREATE TABLE IF NOT EXISTS public.' || partition
              || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('
                    || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp) ) * 1000)::bigint
              || ') TO (' 
              || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp) ) * 1000)::bigint  
              || ');
          ';
      END IF;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
                  CREATE TABLE IF NOT EXISTS public.' || partition_next
              || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('
                    || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp) ) * 1000)::bigint
              || ') TO (' 
              || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '2 months' ))::timestamp) ) * 1000)::bigint  
              || ');
          ';
      END IF;

      RETURN NULL;
    END;
$$;


ALTER FUNCTION public.create_historic_price_partition() OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition_02(); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition_02() RETURNS integer
    LANGUAGE plpgsql
    AS $$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
    BEGIN
      parent_table := 'historic_price_timestamp';
      partition_key := 'created_at';
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval '1 month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
                  CREATE TABLE IF NOT EXISTS public.' || partition
              || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                    || ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp)
              || ''') TO (''' 
              || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
              || ''');
          ';
      END IF;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
                  CREATE TABLE IF NOT EXISTS public.' || partition_next
              || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                    || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
              || ''') TO ('''
              || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '2 months' ))::timestamp)
              || ''');
          ';
      END IF;

      RETURN NULL;
    END;
$$;


ALTER FUNCTION public.create_historic_price_partition_02() OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition_03(); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition_03() RETURNS integer
    LANGUAGE plpgsql
    AS $$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
    BEGIN
      -- this is the parent partition table name
      parent_table := 'historic_price_timestamp';
      -- this is the partition column name, the type is "timestamp without time zone", such as '2021-02-26 05:26:42'::timestamp without time zone
      partition_key := 'created_at';
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval '1 month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
                CREATE TABLE IF NOT EXISTS public.' || partition
            || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp)
            || ''') TO (''' 
            || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
            || ''');

          CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month 
            || ' ON public.' || partition || ' (value_date, valid_from);
        ';
      END IF;

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
                CREATE TABLE IF NOT EXISTS public.' || partition_next
            || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
            || ''') TO ('''
            || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '2 months' ))::timestamp)
            || ''');
        ';
      END IF;

      RETURN NULL;
    END;
$$;


ALTER FUNCTION public.create_historic_price_partition_03() OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition_04(integer); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition_04(next_month_number integer DEFAULT 1) RETURNS integer
    LANGUAGE plpgsql
    AS $_$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
      number ALIAS FOR $1;
      number_02 int;
    BEGIN
      -- this is the parent partition table name
      parent_table := 'historic_price_timestamp';
      -- this is the partition column name, the type is "timestamp without time zone", such as '2021-02-26 05:26:42'::timestamp without time zone
      partition_key := 'created_at';
      number := 12;
      number_02 := number + 1;
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval ' || 12 || month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;
      

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
                CREATE TABLE IF NOT EXISTS public.' || partition
            || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp)
            || ''') TO (''' 
            || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
            || ''');

          CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month 
            || ' ON public.' || partition || ' (value_date, valid_from);
        ';
      END IF;
      
      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
                CREATE TABLE IF NOT EXISTS public.' || partition_next
            || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC' + ' || 12 || months' ))::timestamp)
            || ''') TO ('''
            || ((date_trunc('month',now() AT TIME ZONE 'UTC' + ' || 13 || months' ))::timestamp)
            || ''');
        ';
      END IF;

      RETURN NULL;
    END;
$_$;


ALTER FUNCTION public.create_historic_price_partition_04(next_month_number integer) OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition_05(); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition_05() RETURNS integer
    LANGUAGE plpgsql
    AS $_$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
    BEGIN
      -- this is the parent partition table name
      parent_table := 'historic_price_timestamp';
      -- this is the partition column name, the type is "timestamp without time zone", such as '2021-02-26 05:26:42'::timestamp without time zone
      partition_key := 'created_at';
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval ' 12 month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;
      

      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
          DO $$
            BEGIN
              -- create new partition table 
              IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition || ''') THEN
                      CREATE TABLE IF NOT EXISTS public.' || partition
                  || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                        || ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp)
                  || ''') TO (''' 
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp)
                  || ''');
              END IF;

              -- check and create other db objects of the new partition table 
              IF to_regclass(''public.idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month || ''') IS NULL THEN
                CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month 
                  || ' ON public.' || partition || ' (value_date, valid_from);
              END IF;

            END
          $$;
        ';
      END IF;
      
      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
          DO $$
            BEGIN
              -- create new partition table 
              IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition_next || ''') THEN
                      CREATE TABLE IF NOT EXISTS public.' || partition_next
                  || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('''
                        || ((date_trunc('month',now() AT TIME ZONE 'UTC' + ' 12 months' ))::timestamp)
                  || ''') TO ('''
                  || ((date_trunc('month',now() AT TIME ZONE 'UTC' + ' 13 months' ))::timestamp)
                  || ''');
              END IF;

              -- check and create other db objects of the new partition table 
              IF to_regclass(''public.idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month_next || ''') IS NULL THEN
                CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month_next 
                  || ' ON public.' || partition_next || ' (value_date, valid_from);
              END IF;

            END
          $$;
        ';
      END IF;

      RETURN NULL;
    END;
$_$;


ALTER FUNCTION public.create_historic_price_partition_05() OWNER TO dba_test_db_admin;

--
-- Name: create_historic_price_partition_06(); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.create_historic_price_partition_06() RETURNS integer
    LANGUAGE plpgsql
    AS $_$
    DECLARE
      parent_table TEXT;
      partition_key TEXT;
      partition TEXT;
      partition_next TEXT;
      partition_date_month TEXT;
      partition_date_month_next TEXT;
    BEGIN
      -- this is the parent partition table name
      parent_table := 'historic_price';
      -- this is the partition column name, the type is "bigint", such as 1614556800000::bigint
      partition_key := 'created_at';
      partition_date_month := to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
      partition_date_month_next := to_char((now() AT TIME ZONE 'UTC' + interval ' 1 month')::date,'YYYY_MM');
      partition := parent_table || '_' || partition_date_month;
      partition_next := parent_table || '_' || partition_date_month_next;
      
      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition) THEN
        EXECUTE '
          DO $$
            BEGIN
              -- create new partition table 
              IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition || ''') THEN
                      CREATE TABLE IF NOT EXISTS public.' || partition
                  || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('
                        || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC'))::timestamp) ) * 1000)::bigint
                  || ') TO (' 
                  || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp) ) * 1000)::bigint  
                  || ');
              END IF;

              -- check and create other db objects of the new partition table 
              IF to_regclass(''public.idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month || ''') IS NULL THEN
                CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month 
                  || ' ON public.' || partition || ' (value_date, valid_from);
              END IF;

              IF to_regclass(''time_series_rolling_insert_trigger_' || partition_date_month || ''') IS NULL THEN
                CREATE TRIGGER time_series_rolling_insert_trigger' || partition_date_month
                  || ' BEFORE INSERT ON public.' || partition || ' FOR EACH ROW EXECUTE PROCEDURE partitioned.create_timeseries_rolling_insert();
              END IF;

            END
          $$;
        ';
      END IF;
      
      IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname=partition_next) THEN
        EXECUTE '
          DO $$
            BEGIN
              -- create new partition table 
              IF NOT EXISTS (SELECT * from INFORMATION_SCHEMA.Tables WHERE Table_name = ''' || partition_next || ''') THEN
                      CREATE TABLE IF NOT EXISTS public.' || partition_next
                  || ' PARTITION OF public.' || parent_table || ' FOR VALUES FROM ('
                  || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '1 months' ))::timestamp) ) * 1000)::bigint  
                  || ') TO ('
                  || (extract(epoch from ((date_trunc('month',now() AT TIME ZONE 'UTC' + '2 months' ))::timestamp) ) * 1000)::bigint  
                  || ');
              END IF;

              -- check and create other db objects of the new partition table 
              IF to_regclass(''public.idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month_next || ''') IS NULL THEN
                CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_' || partition_date_month_next 
                  || ' ON public.' || partition_next || ' (value_date, valid_from);
              END IF;

              IF to_regclass(''time_series_rolling_insert_trigger_' || partition_date_month_next || ''') IS NULL THEN
                CREATE TRIGGER time_series_rolling_insert_trigger' || partition_date_month_next
                  || ' BEFORE INSERT ON public.' || partition_next || ' FOR EACH ROW EXECUTE PROCEDURE partitioned.create_timeseries_rolling_insert();
              END IF;
              
            END
          $$;
        ';
      END IF;

      RETURN NULL;
    END;
$_$;


ALTER FUNCTION public.create_historic_price_partition_06() OWNER TO dba_test_db_admin;

--
-- Name: sales_tax(real); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.sales_tax(real) RETURNS real
    LANGUAGE plpgsql
    AS $_$
DECLARE
    subtotal ALIAS FOR $1;
BEGIN
    RETURN subtotal + 1;
END;
$_$;


ALTER FUNCTION public.sales_tax(real) OWNER TO dba_test_db_admin;

--
-- Name: sales_tax_02(real); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.sales_tax_02(real) RETURNS real
    LANGUAGE plpgsql
    AS $_$
DECLARE
    subtotal ALIAS FOR $1;
    month_name TEXT;
BEGIN
    subtotal := subtotal + 1;
    month_name = to_char((now() AT TIME ZONE 'UTC')::date,'YYYY_MM');
    -- RETURN subtotal;
    RETURN month_name;
END;
$_$;


ALTER FUNCTION public.sales_tax_02(real) OWNER TO dba_test_db_admin;

--
-- Name: sum_n_product(integer, integer); Type: FUNCTION; Schema: public; Owner: dba_test_db_admin
--

CREATE FUNCTION public.sum_n_product(x integer, y integer, OUT sum integer, OUT prod integer) RETURNS record
    LANGUAGE plpgsql
    AS $$
BEGIN
    sum := x + y;
    prod := x * y;
END;
$$;


ALTER FUNCTION public.sum_n_product(x integer, y integer, OUT sum integer, OUT prod integer) OWNER TO dba_test_db_admin;

SET default_tablespace = '';

--
-- Name: historic_price; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price (
    id character varying(64) NOT NULL,
    created_at bigint NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
)
PARTITION BY RANGE (created_at);


ALTER TABLE public.historic_price OWNER TO dba_test_db_admin;

SET default_table_access_method = heap;

--
-- Name: historic_price_2021_03; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price_2021_03 (
    id character varying(64) NOT NULL,
    created_at bigint NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
);
ALTER TABLE ONLY public.historic_price ATTACH PARTITION public.historic_price_2021_03 FOR VALUES FROM ('1614556800000') TO ('1617235200000');


ALTER TABLE public.historic_price_2021_03 OWNER TO dba_test_db_admin;

--
-- Name: historic_price_2021_04; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price_2021_04 (
    id character varying(64) NOT NULL,
    created_at bigint NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
);
ALTER TABLE ONLY public.historic_price ATTACH PARTITION public.historic_price_2021_04 FOR VALUES FROM ('1617235200000') TO ('1619827200000');


ALTER TABLE public.historic_price_2021_04 OWNER TO dba_test_db_admin;

--
-- Name: historic_price_timestamp; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price_timestamp (
    id character varying(64) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
)
PARTITION BY RANGE (created_at);


ALTER TABLE public.historic_price_timestamp OWNER TO dba_test_db_admin;

--
-- Name: historic_price_timestamp_2021_03; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price_timestamp_2021_03 (
    id character varying(64) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
);
ALTER TABLE ONLY public.historic_price_timestamp ATTACH PARTITION public.historic_price_timestamp_2021_03 FOR VALUES FROM ('2021-03-01 00:00:00') TO ('2021-04-01 00:00:00');


ALTER TABLE public.historic_price_timestamp_2021_03 OWNER TO dba_test_db_admin;

--
-- Name: historic_price_timestamp_2022_03; Type: TABLE; Schema: public; Owner: dba_test_db_admin
--

CREATE TABLE public.historic_price_timestamp_2022_03 (
    id character varying(64) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    ccy_pair character varying(6) NOT NULL,
    style character varying(16) NOT NULL,
    product character varying(16) NOT NULL,
    type character varying(16) NOT NULL,
    value_date date,
    tenor character varying(16),
    bid jsonb NOT NULL,
    ask jsonb NOT NULL,
    mid numeric(16,8),
    source jsonb NOT NULL,
    cross_source jsonb,
    valid_from bigint NOT NULL,
    valid_to bigint NOT NULL,
    carded_price_data jsonb,
    volume_band numeric(16,0)
);
ALTER TABLE ONLY public.historic_price_timestamp ATTACH PARTITION public.historic_price_timestamp_2022_03 FOR VALUES FROM ('2022-03-01 00:00:00') TO ('2022-04-01 00:00:00');


ALTER TABLE public.historic_price_timestamp_2022_03 OWNER TO dba_test_db_admin;

--
-- Data for Name: historic_price_2021_03; Type: TABLE DATA; Schema: public; Owner: dba_test_db_admin
--

COPY public.historic_price_2021_03 (id, created_at, ccy_pair, style, product, type, value_date, tenor, bid, ask, mid, source, cross_source, valid_from, valid_to, carded_price_data, volume_band) FROM stdin;
\.


--
-- Data for Name: historic_price_2021_04; Type: TABLE DATA; Schema: public; Owner: dba_test_db_admin
--

COPY public.historic_price_2021_04 (id, created_at, ccy_pair, style, product, type, value_date, tenor, bid, ask, mid, source, cross_source, valid_from, valid_to, carded_price_data, volume_band) FROM stdin;
\.


--
-- Data for Name: historic_price_timestamp_2021_03; Type: TABLE DATA; Schema: public; Owner: dba_test_db_admin
--

COPY public.historic_price_timestamp_2021_03 (id, created_at, ccy_pair, style, product, type, value_date, tenor, bid, ask, mid, source, cross_source, valid_from, valid_to, carded_price_data, volume_band) FROM stdin;
\.


--
-- Data for Name: historic_price_timestamp_2022_03; Type: TABLE DATA; Schema: public; Owner: dba_test_db_admin
--

COPY public.historic_price_timestamp_2022_03 (id, created_at, ccy_pair, style, product, type, value_date, tenor, bid, ask, mid, source, cross_source, valid_from, valid_to, carded_price_data, volume_band) FROM stdin;
\.


--
-- Name: idx_historic_price_timestamp_value_date_valid_from_2021_03; Type: INDEX; Schema: public; Owner: dba_test_db_admin
--

CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_2021_03 ON public.historic_price_timestamp_2021_03 USING btree (value_date, valid_from);


--
-- Name: idx_historic_price_timestamp_value_date_valid_from_2021_04; Type: INDEX; Schema: public; Owner: dba_test_db_admin
--

CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_2021_04 ON public.historic_price_2021_04 USING btree (value_date, valid_from);


--
-- Name: idx_historic_price_timestamp_value_date_valid_from_2022_03; Type: INDEX; Schema: public; Owner: dba_test_db_admin
--

CREATE INDEX idx_historic_price_timestamp_value_date_valid_from_2022_03 ON public.historic_price_timestamp_2022_03 USING btree (value_date, valid_from);


--
-- Name: historic_price_2021_03 time_series_rolling_insert_trigger2021_03; Type: TRIGGER; Schema: public; Owner: dba_test_db_admin
--

CREATE TRIGGER time_series_rolling_insert_trigger2021_03 BEFORE INSERT ON public.historic_price_2021_03 FOR EACH ROW EXECUTE FUNCTION partitioned.create_timeseries_rolling_insert();


--
-- Name: historic_price_2021_04 time_series_rolling_insert_trigger2021_04; Type: TRIGGER; Schema: public; Owner: dba_test_db_admin
--

CREATE TRIGGER time_series_rolling_insert_trigger2021_04 BEFORE INSERT ON public.historic_price_2021_04 FOR EACH ROW EXECUTE FUNCTION partitioned.create_timeseries_rolling_insert();


--
-- Name: TABLE historic_price; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price TO airwallex;
GRANT SELECT ON TABLE public.historic_price TO airwallex_r;
GRANT ALL ON TABLE public.historic_price TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price TO dba_test_db_r;


--
-- Name: TABLE historic_price_2021_03; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price_2021_03 TO airwallex;
GRANT SELECT ON TABLE public.historic_price_2021_03 TO airwallex_r;
GRANT ALL ON TABLE public.historic_price_2021_03 TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price_2021_03 TO dba_test_db_r;


--
-- Name: TABLE historic_price_2021_04; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price_2021_04 TO airwallex;
GRANT SELECT ON TABLE public.historic_price_2021_04 TO airwallex_r;
GRANT ALL ON TABLE public.historic_price_2021_04 TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price_2021_04 TO dba_test_db_r;


--
-- Name: TABLE historic_price_timestamp; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price_timestamp TO airwallex;
GRANT SELECT ON TABLE public.historic_price_timestamp TO airwallex_r;
GRANT ALL ON TABLE public.historic_price_timestamp TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price_timestamp TO dba_test_db_r;


--
-- Name: TABLE historic_price_timestamp_2021_03; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price_timestamp_2021_03 TO airwallex;
GRANT SELECT ON TABLE public.historic_price_timestamp_2021_03 TO airwallex_r;
GRANT ALL ON TABLE public.historic_price_timestamp_2021_03 TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price_timestamp_2021_03 TO dba_test_db_r;


--
-- Name: TABLE historic_price_timestamp_2022_03; Type: ACL; Schema: public; Owner: dba_test_db_admin
--

GRANT ALL ON TABLE public.historic_price_timestamp_2022_03 TO airwallex;
GRANT SELECT ON TABLE public.historic_price_timestamp_2022_03 TO airwallex_r;
GRANT ALL ON TABLE public.historic_price_timestamp_2022_03 TO dba_test_db_rw;
GRANT SELECT ON TABLE public.historic_price_timestamp_2022_03 TO dba_test_db_r;


--
-- Name: TABLE pg_stat_statements; Type: ACL; Schema: public; Owner: airwallex
--

GRANT ALL ON TABLE public.pg_stat_statements TO dba_test_db_admin;
GRANT ALL ON TABLE public.pg_stat_statements TO dba_test_db_rw;
GRANT SELECT ON TABLE public.pg_stat_statements TO dba_test_db_r;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: dba_test_db_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public REVOKE ALL ON SEQUENCES  FROM dba_test_db_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public GRANT SELECT,USAGE ON SEQUENCES  TO dba_test_db_rw;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: airwallex
--

ALTER DEFAULT PRIVILEGES FOR ROLE airwallex IN SCHEMA public REVOKE ALL ON TABLES  FROM airwallex;
ALTER DEFAULT PRIVILEGES FOR ROLE airwallex IN SCHEMA public GRANT ALL ON TABLES  TO dba_test_db_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE airwallex IN SCHEMA public GRANT ALL ON TABLES  TO dba_test_db_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE airwallex IN SCHEMA public GRANT SELECT ON TABLES  TO dba_test_db_r;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: dba_test_db_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public GRANT ALL ON TABLES  TO airwallex;
ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public GRANT SELECT ON TABLES  TO airwallex_r;
ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public GRANT ALL ON TABLES  TO dba_test_db_rw;
ALTER DEFAULT PRIVILEGES FOR ROLE dba_test_db_admin IN SCHEMA public GRANT SELECT ON TABLES  TO dba_test_db_r;


--
-- PostgreSQL database dump complete
--

