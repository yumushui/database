#!/usr/bin/env python
# -*- conding: utf-8 -*-

print ('''
前言
数据类型是编程语言中，在其数据结构上定义的相同值类型的集合以及对该相同值集合的一组操作.
而数据类型的值存储离不开变量，因此变量的一个作用就是使用它来存储相同值集的数据类型。
数据类型决定了如何将代表这些值的集合存储在计算机的内存中。变量一般遵循先声明后使用的原则。
而在数据库中，变量就是字段，用字段来表示一组相同值类型的集合，其实也是先声明后使用的原则。

PostgreSQL支持丰富的数据类型，包括一般的数据类型和非常规的数据类型。
一般数据类型包括数值型，货币类型，字符类型，日期类型，布尔类型，枚举类型等，
非常规数据类型包括二进制数据类型，几何类型，网络地址类型，位串类型，文本搜索类型，UUID类型,XML类型，JSON类型，数组类型，复合类型，范围类型，Domain类型，OID类型，pg_lsn类型和pseudo-Types类型。

''')
print ('''
   the postgresql data type   

一、数值类型 Number

 1 整型 inerger

PostgreSQL中的整型类型有小整型，整型，大整型，用 smallint,integer,和bigint表示，
虽然三个都可以存储相同的数据类型，但是它们各自的存储大小和存储范围却不相同。


如下示例所示，在PostgreSQL中，smallint，integer，bigint 数据类型可以使用 int2,int4,int8的扩展写法来标识。

--创建整型数据类型的表
CREATE TABLE IF NOT EXISTS tab_num(v1 smallint,v2 smallint,v3 int,v4 int,v5 bigint,v6 bigint);
CREATE TABLE

--表字段注释
COMMENT ON COLUMN tab_num.v1 IS '小整型最小范围';
COMMENT ON COLUMN tab_num.v2 IS '小整型最大范围';
COMMENT ON COLUMN tab_num.v3 IS '整型最小范围';
COMMENT ON COLUMN tab_num.v4 IS '整型最大范围';
COMMENT ON COLUMN tab_num.v5 IS '大整型最小范围';
COMMENT ON COLUMN tab_num.v6 IS '大整型最大范围';

--描述数据类型
\d+ tab_num

 --插入不同整型的范围数值
 INSERT INTO tab_num
 VALUES (-32768,
         32767,
         -2147483648,
         2147483647,
         -9223372036854775808,
         9223372036854775807);

--查询结果
SELECT * FROM  tab_num;


如上所示，查询的结果为插入不同整型范围的最值，也说明不同整型范围的边界都是被包括的。
在实际生产场景中，SMALLINT、INTEGER和BIGINT类型存储各种范围的数字，也就是整数。
当试图存储超出范围以外的数值将会导致错误。

常用的类型是INTEGER，因为它提供了在范围、存储空间、性能之间的最佳平衡。
一般只有取值范围确定不超过SMALLINT的情况下，才会使用SMALLINT类型。
而只有在INTEGER的范围不够的时候才使用BIGINT，因为前者相对要快。

除此之外，创建表也可以使用 int2,int4,int8来代表 smallint,integer,bigint。
如下示例所示：

/*
smallint,integer,bigint
数据类型分别使用
int2,int4,int8代替
*/
CREATE TABLE IF NOT EXISTS tab_numint(v1 int2,v2 int2,v3 int4,v4 int4,v5 int8,v6 int8);
--描述表定义及数据类型
\d+ tab_numint


-----------------------

2 任意精度类型和浮点类型

任意精度类型 numeric、decimal可以存储范围大的数字，存储大小为可变大小，
小数点前最多131072位数字，小数点后最多16383位。它可以使用类似浮点类型，
将小数精确到保留几位，也可以参与计算可以得到准确的值，但是相比于浮点类型，它的计算比较慢。
通常 numeric被推荐使用于存储货币金额或其它要求计算准确的值。

--任意精度类型示例
CREATE TABLE IF NOT EXISTS tab_any_precision(col1 numeric(10,4),col2 decimal(6,4),col3 real,col4 double precision,col5 float4,col6 float8);
--字段注释
COMMENT ON COLUMN tab_any_precision.col1 IS '表示整数最大位数为6,小数仅保留4位';
COMMENT ON COLUMN tab_any_precision.col2 IS '表示整数最大位数为2,小数保留4位';
COMMENT ON COLUMN tab_any_precision.col3 IS '表示可变的6位精度的数值类型';
COMMENT ON COLUMN tab_any_precision.col4 IS '表示可变的15位精度的数值类型';
COMMENT ON COLUMN tab_any_precision.col5 IS '同real';
COMMENT ON COLUMN tab_any_precision.col6 IS '同double precision';
--查看表定义
\d+ tab_any_precision

--插入任意精度测试
INSERT INTO tab_any_precision
VALUES(202004.26,20.2004,20.200426,20.203415341535157,20.200426,20.203415341535157);

INSERT INTO tab_any_precision
VALUES(202004.26105,20.20045,20.2004267,20.2034153415351573,20.2004264,20.2034153415351575);

--可以发现col1和col2小数部分可以超过4位，但是读取仅仅保留4位，并遵循四舍五入的原则,如下结果
SELECT * FROM tab_any_precision;


   /*
    如果 col1 插入的整数最大位数超过6，将会报错。
    如果 col2 插入的整数最大位数超过2，将会报错。
    real 和 double precision 没有限制。
    */
 
 # INSERT INTO tab_any_precision
   VALUES(2020042.610,20.2004,20.2004267,20.2034153415351573,20.2004264,20.2034153415351575);
ERROR:  numeric field overflow
DETAIL:  A field with precision 10, scale 4 must round to an absolute value less than 10^6.

# INSERT INTO tab_any_precision
   VALUES(202004.26105,202.200,20.2004267,20.2034153415351573,20.2004264,20.2034153415351575);
ERROR:  numeric field overflow
DETAIL:  A field with precision 6, scale 4 must round to an absolute value less than 10^2.

----------------------

3 sequence 序列类型

SMALLSERIAL，SERIAL和BIGSERIAL类型不是真正的数据类型，只是为在表中设置唯一标识做的概念上的便利.
因此，创建一个整数字段，并且把它的缺省数值安排为从一个序列发生器读取。
应用了一个NOT NULL约束以确保NULL不会被插入。
在大多数情况下用户可能还希望附加一个UNIQUE或PRIMARY KEY约束避免意外地插入重复的数值，但这个不是自动的。
最后，将序列发生器从属于那个字段，这样当该字段或表被删除的时候也一并删除它。

--创建序列类型表
CREATE TABLE tab_serial(col1 smallserial,col2 serial,col3 bigserial);

--字段注释
COMMENT ON  COLUMN tab_serial.col1 IS '小整型序列，从1开始，最大值为32767';
COMMENT ON  COLUMN tab_serial.col2 IS '小整型序列，从1开始，最大值为2147483647';
COMMENT ON  COLUMN tab_serial.col3 IS '小整型序列，从1开始，最大值为9223372036854775807';

--查看表定义
\d+ tab_serial

 --插入数据
INSERT INTO tab_serial VALUES(1,1,1);
INSERT INTO tab_serial VALUES(32767,2147483647,9223372036854775807);

--如果插入的值大于序列整型值的范围，将会整型类型越界的ERROR
# INSERT INTO tab_serial VALUES(32767,2147483647,9223372036854775808);
ERROR:  bigint out of range
# INSERT INTO tab_serial VALUES(32767,2147483648,9223372036854775807);
ERROR:  integer out of range
# INSERT INTO tab_serial VALUES(32768,2147483647,9223372036854775807);
ERROR:  smallint out of range

--当然，既然是序列类型，那可以插入默认值
INSERT INTO tab_serial
VALUES(default,default,default);


通过上述示例，可以知道 smallserial,serial,bigserial相当于先创建一个序列，
然后在创建表分别指定不同的整型数据类型smallint,integer,bigint。如下示例：

--先创建序列
CREATE SEQUENCE IF NOT EXISTS serial_small
INCREMENT BY 1
START WITH 1 
NO CYCLE;

--再创建表
CREATE TABLE IF NOT EXISTS tab_test_serial(
col1 smallint default nextval('serial_small'),
col2 integer default nextval('serial_small'),
col3 bigint default nextval('serial_small')
);

--插入数据
INSERT INTO tab_test_serial VALUES(default);

--查询数据
SELECT * FROM tab_test_serial ;


''')

print ('''

二、货币数据类型

货币类型存储带有固定小数精度的货币金额。

--创建货币数据类型表
CREATE TABLE IF NOT EXISTS tab_money(amounts money);

--字段注释
COMMENT ON COLUMN tab_money.amounts IS '金额';

--插入数值
INSERT INTO tab_money VALUES('20.00');

--查询数据
SELECT * FROM tab_money;

这里需要注意的是，如果插入的货币数据类型的金额没有明确指定货币表示符号，
那么默认输出本区域货币符号，如上示例所示的20.00输出为$20.00。

如果是人民币，那么如何处理呢？

解决方法有两种，第一种，使用translate函数；第二种，修改本地区域货币符号显示参数。

--方法一:直接使用translate函数将 $ 符号转换为 ￥ 符号
SELECT translate(amounts::varchar,'$','￥') FROM tab_money;

--方法二:修改区域货币符号显示参数
--查看本地区域货币符号显示参数
show lc_monetary ;

--修改区域货币符号显示参数
ALTER SYSTEM SET lc_monetary = 'zh_CN.UTF-8';

--重新加载动态参数
SELECT pg_reload_conf();

--重新查看本地区域货币符号显示参数
show lc_monetary;

--重新查询数据
SELECT * FROM tab_money;


货币符号作为特殊的数据类型，需要注意计算方式，以防止发生精度丢失的问题。
这种问题解决方式需要将货币类型转换为 numeric 类型以避免精度丢失。
INSERT INTO tab_money VALUES('20.22');

SELECT * FROM tab_money ;

--货币数据类型避免精度丢失的解决方法
SELECT amounts::numeric::float8 FROM tab_money;

温馨提示：

当一个money类型的值除以另一个money类型的值时，结果是double precision（也就是，一个纯数字，而不是money类型）；在运算过程中货币单位相互抵消。


''')

print('''

三、布尔类型

PostgreSQL提供标准的boolean值，boolean的状态为 true或者false和unknown，
如果是unknown状态表示boolean值为null。

--创建boolean类型表
CREATE TABLE IF NOT EXISTS tab_boolean(col1 boolean,col2 boolean);

--插入布尔类型的状态值，状态值可以是以下任意一种
INSERT INTO tab_boolean VALUES(TRUE,FALSE);--规范用法
INSERT INTO tab_boolean VALUES('true','false');
INSERT INTO tab_boolean VALUES('True','False');
INSERT INTO tab_boolean VALUES('TRUE','FALSE');
INSERT INTO tab_boolean VALUES('1','0');
INSERT INTO tab_boolean VALUES('on','off');
INSERT INTO tab_boolean VALUES('ON','OFF');
INSERT INTO tab_boolean VALUES('y','n');
INSERT INTO tab_boolean VALUES('Y','N');
INSERT INTO tab_boolean VALUES('yes','no');
INSERT INTO tab_boolean VALUES('Yes','No');
INSERT INTO tab_boolean VALUES('YES','NO');

SELECT * FROM tab_boolean ;


boolean类型被广泛地使用在业务环境中，例如手机开关机，1表示开机，0表示关机或不在服务区。
手机APP登录登出，1表示登录，0表示登出，微信登陆状态，1表示登录成功，
0表示登录失败（可能由于网络或者密码错误导致）等等，此处不再一一举例。

''')

print('''

四、字符类型

SQL定义了两种主要的字符类型:character varying(n) 和 character(n)。
该处的n是一个正数。这两种字符类型都可以存储n（非字节）个长度的字符串。
如果存储的字符长度超过了字符类型约束的长度会引起错误，除非多出的字符是空格。

--创建字符类型表
CREATE TABLE IF NOT EXISTS tab_chartype(
col1 char(15),
col2 varchar(15),
col3 text,
col4 name,
col5 "char" );

--字段注释
COMMENT ON COLUMN tab_chartype.col1 IS '表示定长为15的字符串';
COMMENT ON COLUMN tab_chartype.col2 IS '表示变长为15的字符串';
COMMENT ON COLUMN tab_chartype.col3 IS '表示变长字符串，为varchar的扩展字符串';
COMMENT ON COLUMN tab_chartype.col4 IS '用于对象名的内部类型';
COMMENT ON COLUMN tab_chartype.col5 IS '表示单字节类型';

--插入数据
INSERT INTO tab_chartype
VALUES('sungsasong','sungsasong','sungsasong','tab_chartype','s');

--插入包含空格的数据
INSERT INTO tab_chartype
VALUES('sungsa song','sung sas ong','sung sa song ','tab_chartype','s');

--计算不同数据类型存储的字符串的长度
SELECT char_length(col1),char_length(col2),char_length(col3),char_length(col4),char_length(col5)
FROM tab_chartype ;

馨提示：
在上面示例中，虽然统计的col1的定长为15的字符存储的字符长度为10个和11个，但是实际上，在存储中col1列占用的长度为15个。
并且，在计算长度的时候，空格也被当作一个字符来对待。

''')

print('''

五、二进制数据类型

在PostgreSQL中，二进制数据类型有两种，一种为 bytea hex格式，一种为 bytea escape格式。

注意：除了每列的大小限制以外，每个元组的总大小也不可超过1G-8203字节。

--创建两种bytea格式的表
CREATE TABLE IF NOT EXISTS tab_bytea(col1 bytea,col2 bytea);

--字段注释
COMMENT ON COLUMN tab_bytea.col1 IS 'bytea hex 格式的二进制串';
COMMENT ON COLUMN tab_bytea.col2 IS 'bytea escape 格式的二进制串';

--插入数据,第一个值代表单引号，输出16进制的值为\x27,第二个为转义16进制的值f
INSERT INTO tab_bytea
VALUES('\047',E'\xF');

--插入数据,第一个值代表反斜杠，输出16禁止的值为\x5c,第二个值为转义16进制的值fc
INSERT INTO tab_bytea
VALUES('\134',E'\\xFC');

--查看结果
SELECT * FROM tab_bytea;

注意：

实际上bytea多个十六进制值使用E’\xFC’ 类似于Oracle中的rawtohex函数。
只不过Oracle中的rawtohex函数转换后的值为大写十六进制字符串。
实际上如果要在上表中的col2中插入E’\xFG’时，会提示G不是一个有效的十六进制字符。

同时需要注意的是，如果使用E’\xF’只包含单个十六进制字符时，使用一个反斜杠，
如果有多个十六进制字符，需要两个反斜杠，如E’\xFE’。

如下:此处的hextoraw函数为我自定义实现的一个UDF函数。
SELECT hextoraw('FCd');

INSERT INTO tab_bytea
VALUES('\134',E'\\xFG');

''')

print('''

六、日期时间数据类型

PostgreSQL支持丰富的日期时间数据类型如下表：

6.1日期输入

日期和时间的输入可以是任何合理的格式，包括ISO-8601格式、SQL-兼容格式、传统POSTGRES格式或者其它的形式。系统支持按照日、月、年的顺序自定义日期输入。如果把DateStyle参数设置为MDY就按照“月-日-年”解析，设置为DMY就按照“日-月-年”解析，设置为YMD就按照“年-月-日”解析。

日期的文本输入需要加单引号包围，语法如下：
type [ ( p ) ] ‘value’

可选的精度声明中的p是一个整数，表示在秒域中小数部分的位数。
--创建日期输入表
CREATE TABLE tab_datetype(col1 date);

--字段注释
COMMENT ON COLUMN tab_datetype.col1 IS '日期类型，默认遵循datestyle风格(MDY)';

--插入数据
INSERT INTO tab_datetype VALUES(date '04-26-2020');

--在MDY风格下，也支持YMD的输入方式，但是不支持DMY或者其它格式的输入，如下会报错
INSERT INTO tab_datetype VALUES(date '22-04-2020');
ERROR:  date/time field value out of range: "22-04-2020"
LINE 1: INSERT INTO tab_datetype VALUES(date '22-04-2020');
                                             ^
HINT:  Perhaps you need a different "datestyle" setting.

--解决办法,修改datestyle的格式
 --查看当前数据库的datestyle的格式
show datestyle;
 DateStyle 
-----------
 ISO, MDY
(1 row)

--会话级别修改datestyle格式
SET datestyle = 'DMY';

--再次插入 22-04-2020
INSERT INTO tab_datetype VALUES(date '22-04-2020');

--查询数据
SELECT * FROM tab_datetype ;

6.2时间输入

时间类型包括

time [ § ] without time zone 和time [ § ] with time zone。

如果只写time等效于time without time zone。即不带时区的时间格式

如果在time without time zone类型的输入中声明了时区，则会忽略这个时区。

--不带时区的时间
SELECT time '13:22:25';

SELECT time without time zone '20:20:18';

SELECT time with time zone '18:20:20';

6.3特殊时间类型

特殊时间类型以reltime表示，表示真实的时间计算值，如100将会使用00:01:40来表示。

--创建reltime时间数据类型表
CREATE TABLE tab_reltime(col1 varchar,col2 reltime);

--字段注释
COMMENT ON COLUMN tab_reltime.col1 IS '原始时间文本时间';
COMMENT ON COLUMN tab_reltime.col2 IS 'reltime表示的时间以实际时间计算得到显示结果';

--插入数据
INSERT INTO tab_reltime VALUES('125','125');
INSERT INTO tab_reltime VALUES('10 DAYS','10 DAYS');
INSERT INTO tab_reltime VALUES('420 DAYS 12:00:23','420 DAYS 12:00:23');

--查询数据
SELECT * FROM tab_reltime;

温馨提示：

对于 reltime 时间的输入，需要使用文本类型的输入，也就是说使用单引号引起来。

6.4其它时间类型

其它时间类型包含时间戳及间隔时间数据类型，示例如下：

--创建时间戳和间隔时间表
CREATE TABLE tab_timestamp_interval(col1 timestamp with time zone,col2 timestamp without time zone,col3 interval day to second);

--字段注释
COMMENT ON COLUMN tab_timestamp_interval.col1 IS '带时区的时间戳';
COMMENT ON COLUMN tab_timestamp_interval.col2 IS '不带时区的时间戳';
COMMENT ON COLUMN tab_timestamp_interval.col1 IS '间隔时间类型';

--插入数据
INSERT INTO tab_timestamp_interval
VALUES('2020-04-26 13:20:34.234322 CST',
       '2020-04-08 14:40:12.234231+08',
       '165');

INSERT INTO tab_timestamp_interval
VALUES('2020-04-25 14:56:34.223421',
       '2020-04-09 18:54:12.645643 CST',
       '10 YEAR 3 MONTH 25 DAYS 14 HOUR 32 MINUTE 19 SECOND');

--查询数据
SELECT * FROM  tab_timestamp_interval;




''')

print('''

七、网络地址类型

PostgreSQL也提供网络地址类型，以用于存储两大IP家族(IPv4 IPv6地址)地址和MAC地址的数据类型。

cidr（无类别域间路由，Classless Inter-Domain Routing）类型，保存一个IPv4或IPv6网络地址。声明网络格式为address/y，address表示IPv4或者IPv6地址，y表示子网掩码的二进制位数。如果省略y，则掩码部分使用已有类别的网络编号系统进行计算，但要求输入的数据已经包括了确定掩码所需的所有字节。

inet类型在一个数据区域内保存主机的IPv4或IPv6地址，以及一个可选子网。主机地址中网络地址的位数表示子网（“子网掩码”）。如果子网掩码是32并且地址是IPv4，则这个值不表示任何子网，只表示一台主机。在IPv6里，地址长度是128位，因此128位表示唯一的主机地址。

该类型的输入格式是address/y，address表示IPv4或者IPv6地址，y是子网掩码的二进制位数。如果省略/y，则子网掩码对IPv4是32，对IPv6是128，所以该值表示只有一台主机。如果该值表示只有一台主机，/y将不会显示。

inet和cidr类型之间的基本区别是inet接受子网掩码，而cidr不接受。

macaddr类型存储MAC地址，也就是以太网卡硬件地址（尽管MAC地址还用于其它用途）。

--创建IP地址及MAC地址表
CREATE TABLE tab_icm(col1 cidr,col2 inet,col3 macaddr);

--字段注释
COMMENT ON COLUMN tab_icm.col1 IS '存储IPv4或IPv6网络地址类型';
COMMENT ON COLUMN tab_icm.col2 IS '存储IPv4或IPv6网络地址类型及子网';
COMMENT ON COLUMN tab_icm.col3 IS '存储设备MAC地址';

--插入数据
INSERT INTO tab_icm VALUES('10.10.20.10/32','10.10.20.10','00-50-56-C0-00-08');
INSERT INTO tab_icm VALUES('10.10.20/24','10.10.20.10','00-50-56-C0-00-08');
INSERT INTO tab_icm VALUES('10.10/16','10.10.20.10','00-50-56-C0-00-08');
INSERT INTO tab_icm VALUES('10/8','10.10.20.10','00-50-56-C0-00-08');
INSERT INTO tab_icm VALUES('fe80::81a7:c17c:788c:7723/128','fe80::81a7:c17c:788c:7723','00-50-56-C0-00-01');

--查询数据                                                                                                  
SELECT * FROM  tab_icm;




''')

print('''

八、几何数据类型

PostgreSQL支持集合数据类型，用于存储GIS（地理信息系统）环境中的几何数据，用于地图测绘，城市交通轨迹，地图圈图等场景。

PostgreSQL支持以下几何数据类型：

点
线(射线)
线段
矩形
路径(包含开放路径【开放路径类似多边形】和闭合路径)
多边形
圆
对于以上几何类型而言，点是其它几何类型的基础。
对于所有的几何数据类型，都是使用二维坐标上面的横坐标和纵坐标来实现的。计算也是在二维坐标中进行的。

--创建几何数据类型表
CREATE TABLE tab_geometric(col1 point,col2 lseg,col3 box,col4 path,col5 path,col6 polygon,col7 circle);

--字段注释
COMMENT ON COLUMN tab_geometric.col1 IS '二维几何的基本构造点(x,y)';
COMMENT ON COLUMN tab_geometric.col2 IS '线段((x1,y1),(x2,y2))';
COMMENT ON COLUMN tab_geometric.col3 IS '矩形((x1,y1),(x1,y2),(x2,y1),(x2,y1)),';
COMMENT ON COLUMN tab_geometric.col4 IS '开放路径((x1,y1),(x2,y2),(x3,y3),...)';

drop table tab_geometric ;

--创建几何数据类型表
CREATE TABLE tab_geometric(col1 point,col2 lseg,col3 box,col4 path,col5 path,col6 polygon,col7 circle);

--字段注释
COMMENT ON COLUMN tab_geometric.col1 IS '二维几何的基本构造点(x,y)';
COMMENT ON COLUMN tab_geometric.col2 IS '线段[(x1,y1),(x2,y2)]';
COMMENT ON COLUMN tab_geometric.col3 IS '矩形((x1,y1),(x1,y2)),';
COMMENT ON COLUMN tab_geometric.col4 IS '开放路径[(x1,y1),(x2,y2),(x3,y3),...]';
COMMENT ON COLUMN tab_geometric.col5 IS '闭合路径[(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)]';
COMMENT ON COLUMN tab_geometric.col6 IS '多边形,相当于闭合路径((x1,y1),(x2,y2),(x3,y3),...,(xn,yn)';
COMMENT ON COLUMN tab_geometric.col7 IS '一组坐标点作为圆心和半径r构成<(x,y),r>';

--插入数据 
INSERT INTO tab_geometric
hVALUES('(1,2)',
       '[(1,2),(2,3)]',
       '((1,2),(1,3))',
       '[(1,2),(2,3),(2,4),(1,3),(0,2)]',
       '[(1,2),(2,3),(3,4)]',
       '((1,2),(2,3),(2,4),(1,3),(0,2))',
       '<(2,3),3>');

--查询数据
SELECT * FROM tab_geometric;



''')

print)('''

九、JSON数据类型

JSON数据类型可以用来存储JSON（JavaScript Object Notation）数据。
数据可以存储为text，但是JSON数据类型更有利于检查每个存储的数值是可用的JSON值。

在 PostgreSQL中，JSON数据类型有两种，原生JSON和JSONB。
最主要的区别就是效率不同。JSON 数据类型对于输入文本进行复制，因此在解析时需要进行转换，输入速度块。
而JSONB是对输入文本进行分解并以二进制存储，因此在解析时不需要进行转换，处理速度块，但是输入速度相对会慢。除此之外，JSONB数据类型还支持索引。

--创建JSON数据类型表
CREATE TABLE tab_json(col1 json,col2 jsonb);

--字段注释
COMMENT ON COLUMN tab_json.col1 IS '存储json输入文本';
COMMENT ON COLUMN tab_json.col1 IS '存储json转换后的二进制文本';

--插入数据
--插入数据
INSERT INTO tab_json
VALUES('{"江苏省":"南京市","甘肃省":"兰州市","北京市":"北京市"}',
       '{"湖北省":"武汉市","四川省":"成都市","陕西省":"西安市"}');

--给col1创建索引，将会不被支持。col2支持索引
=> CREATE INDEX idx_col1 ON tab_json USING GIN(col1);
ERROR:  data type json has no default operator class for access method "gin"
HINT:  You must specify an operator class for the index or define a default operator class for the data type.
=> CREATE INDEX idx_col2 ON tab_json USING GIN(col2);
CREATE INDEX

--查询数据
SELECT * FROM tab_json;

温馨提示：

使用jsonb类型，可以使用PL/PYTHON映射为Python中表示的字典，列表等。



''')

print('''

十、数组数据类型

PostgreSQL支持数组数据类型，同时支持多维数组。
数组最大的优点就是按照数组下标访问，此时下标相当于一个索引，处理速度快。
但是同时数组也有劣势，比如在删除或者添加数组元素需要对数组中的元素进行向前或者向后移动，这样导致删除或者添加数组元组时比较慢。

--创建数组表
CREATE TABLE tab_array(col1 text[],col2 integer[][],col3 integer ARRAY[3]);

--字段注释
COMMENT ON COLUMN tab_array.col1 IS '文本类型一维数组';
COMMENT ON COLUMN tab_array.col2 IS '整型类型二维数组';
COMMENT ON COLUMN tab_array.col3 IS '声明长度为3的数组';

--插入数据
INSERT INTO tab_array
VALUES('{"江苏省","甘肃省","北京市"}',
       '{1,2,3,4,5}',
       '{21,22,31}');

INSERT INTO tab_array
VALUES('{"天津市","湖北省","陕西市"}',
       '{5,4,3,2,1}',
       '{21,22,31,44}');

--查询数据
SELECT * FROM tab_array;

--访问指定列中某个数组的元素
SELECT col1[1],col2[3],col3[4] FROM tab_array;

通过上述示例，可以发现，在PostgreSQL中，虽然声明了数组的长度，但是PostgreSQL对于数组的长度不会做任何限制。

同时访问数组元素从下标1开始，并且在PostgreSQL中并不会出现数组越界异常，如果数组的下标访问超过元素的长度，那么PostgreSQL便会返回一行空值。

以上就是常用数据类型介绍。但是在PostgreSQL中，除了上述数据类型外，还有其它的数据类型，比如XML数据类型，文本搜索数据类型，UUID数据类型，复合数据类型，范围类型，伪类型如any,anyelement,internal等等，在此不做一一介绍。
————————————————
版权声明：本文为CSDN博主「SSsandata」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_45694422/article/details/106016203

''')