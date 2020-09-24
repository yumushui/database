# Kafka core technology and actual combat

Kafka核心技术与实战

+ 全面提升你的Kafka实战能力

##  You will get 

+ Kafka 集群环境的监控和管理；
+ 消息系统常见疑难问题解析；
+ Kafka 内核原理剖析；
+ 流式处理平台应用案例。

##  The author introduction

胡夕，Apache Kafka Committer， 老虎证券用户增长团队负责人，著有 《Apache Kafka实战》一书，曾任任职于 IBM、搜狗和新浪微博等公司。胡夕对 Kafka及其他开源流处理框架和技术有深刻理解，精通Kafka原理，主导郭多个 十亿级/天的消息引擎业务系统的设计和搭建，具有丰富的线上环境定位和诊断调优经验，曾给多家大型公司提供企业级 Kafka培训。

##  The course introduction

Kafka是 LikedIn 开发并开源的一套分布式的高性能消息引擎服务，后来被越来越多的公司应用在自己的系统中，可以说，Kafka是大数据时代数据管道技术的首选。在设计的时候，它就is hi 线了高可靠、高吞吐、高可用和可伸缩，得益于这些特性，加上活跃的社区，Kafka成为了一个完备的分布式消息引擎解决方案。

历经多年发展，Kafka 的功能和特性也在不断迭代，如今的 Kafka集消息系统、存储系统和流式处理平台于一身，并作为连接着各种业务前台和数据后台的消息中间件，在线上环境承担了非常重要的作用。

但在Kafka的实际使用中，几乎所有人都或多或少会遇到一些问题，比如：

+ 棘手的线上问题难于定位和解决，怎么办？
+ 在Kafka版本的演进过程中，各种新功能层出不穷，导致各种兼容性问题接踵而至，怎么办？
+ 当集群规模扩展到一定程度后，所追求的高性能和有限的资源之间的矛盾又变得日益尖锐起来，怎么办？

如何顺利填补这些“坑”，是摆在每个Kafka学习者面前最需要解决的问题。


kafka_core_tech_actual_combat

![kafka_core_tech_actual_combat.jpg](https://github.com/yumushui/database/blob/master/message_queue/huxi_kafka_core_tech_combat/kafka_core_tech_actual_combat.jpg  "kafka_core_tech_actual_combat.jpg")


专栏分为六部分。

+ 第一部分，**Kafka入门**。

作为正式学习前的热身，将介绍消息引擎这类系统的原理和用途，以及作为优秀的消息引擎代表，Kafka是如何“脱颖而出”的。

+ 第二部分，**Kafka的基本使用。**

重点探讨 Kafka 如何用于生产环境，特别是线上环境的方案该如何制定。

+ 第三部分，**客户端实践及原理剖析。**

学习Kafka客户端的方方面面，既有生产者的实操讲解，也有消费者的原理剖析，是专栏的重点内容。

+ 第四部分，**深入Kafka内核。**

将着重介绍 Kafka 最核心的设计原理，包括 Controller 的设计机制、请求处理的全流程等。

+ 第五部分，**管理和监控。**

这部分涵盖Kafka运维和监控的内容，讨论如何高效运维Kafka集群，并分享有效监控Kafka的实战经验。

+ 第六部分，**高级Kafka应用之流处理。**

这一部分将会介绍Kafka流处理组件 Kafka Streams 的实战应用，并从头开发一个 demo项目。


##  The course catalog

《Kafka 核心技术与实战》

```
https://time.geekbang.org/column/intro/191
```

```
开篇词  为什么要学习Kafka？

```

###  Kafka 入门

```
01  消息引擎系统 ABC

02  一篇文章带你快速搞定 Kafka 术语

03  Apache Kafka 真的只是消息引擎系统吗？

04  我应该选择哪种 Kafka？

05  聊聊 Kafka 的版本号

```

###  Kafka 的基本使用

```
06  Kafka 线上集群部署方案怎么做？

07  最最最重要的集群参数配置（上）

08  最最最重要的集群参数配置（下）

```

###  客户端实践及原理剖析

```
09  生产者消息分区机制原理剖析

10  生产者压缩算法面面观

11  无消息丢失配置怎么实现？

12  客户端都有哪些不常见但是很高级的功能？

13  Java 生产者是如何管理 TCP 连接的？

14  幂等生产者和事务生产者是一回事吗？

15  消费者组到底是什么？

16  揭开神秘的“位移主题”面纱

17  消费者组重平衡能避免吗？

18  Kafka中位移提交那些事儿

19  CommitFailedException 异常怎么处理？

20  多线程开发消费者实例

21  Java 消费者是如恶化管理 TCP 连接的？

22  消费者消费进度监控都怎么实现？

```

###  深入 Kafka 内核

```
23  Kafka 备份机制详解

24  请求是怎么被处理的？

25  消费者组重平衡全流程解析

26  你一定不能错过的 Kafka 控制器

27  关于高水位和 Leader Epoch 的讨论

```

###  管理与监控

```
28  主题管理知多少？

29  Kafka 动态配置了解下？

30  怎么重设消息者组位移？

31  常见工具脚本大汇总

32  KafkaAdminClient： Kafka 的运维利器

33  Kafka 认证机制用哪家？

34  运环境下的授权该怎么做？

35  跨集群备份解决方案 MirrorMaker

36  你应该这么监控 Kafka？

37  主流监控框架你知道多少？

38  调优 Kafka 你做到了吗？

39  从0搭建基于 Kafka 的企业级实时日志流处理平台

```

###  高级 Kafka 应用之流处理

```
40  Kafka Streams 与其他流处理平台的差异在哪？

41  Kafka Streams DDL 开发实例

42  Kafka Streams 在金融领域的应用


--  特别放送

加餐  搭建开发环境、阅读源码方法、经典学习资料大揭秘

用户故事   黄云：行百里者半九十

--  结束语

结束语  以梦为马，莫负韶华！

期末测试  这些 Kafka 核心要点，你都掌握了吗？

```


