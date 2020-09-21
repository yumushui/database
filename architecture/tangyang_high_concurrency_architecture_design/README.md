# 40 Questioins about High Concurrency System Design  

高并发系统设计40问

+ 攻克共并发系统演进中的业务难点

## You will get

+ 高并发设计核心技术点
+ 分布式组件的原理和使用方法
+ 完整的系统演进实战
+ 5个角度带你解决高并发难点

## The author introduction 

唐扬，美图公司技术专家，主要负责美图秀秀社区的研发、优化和运行维护工作。从业十余年，见证了系统从初期构建，到承接高并发大流量的全过程，并参与过三个DAU过千万的大型高并发系统的研发，拥有大量的系统演进经验。

## The course introccution 

“秒杀活动”“抢红包”“微博热搜”“12306抢票”“共享单车拉新”等都是高并发的典型业务场景，那么如何解决这些业务场景背后的难点问题呢？

+ 秒杀系统中，QPS达到10万/s时，如何定位并解决业务瓶颈？
+ 明星婚恋话题不断引爆微博热搜，如何确保永不宕机？
+ 共享单车充值活动，如何保证不超卖？
+ ......

**同一实践、海量用户的高频访问对任何平台都是难题，但可喜的是，虽然业务场景不同，设计和优化的思想 却是万变不离其宗。**如果你掌握了高并发系统设计的核心技术点（缓存、池化、异步化、负载均衡、队列、熔断机制等），深化成自己的 知识体系，解决这些业务问题将不再 话下，应对自如。

在唐扬看来，不少技术能力极强的工程师依旧会被“高并发”所困，这与知识储备不足，无法系统化地掌握核心技术又很大关系。技术人要不断汲取新的营养，更要能将技术知识应用到实际业务中，这样才能提升竞争力，突破职场瓶颈。

在这个课程中，**作者将基于业务场景还原大型互联网技术架构的演进过程，带你攻克不同业务阶段所需的各项和核心技术，解决你的 痛点问题。**除此之外，还将结合资深经验，从课程内容延伸出高频面试题，**还原面试现场，为你的面试助力！**

**课程的讲解思路是：** 先带你建立对高并发系统设计的直观理解，再以最简单架构逐步演进到支撑百万、千万并发的分布式架构为案例，带你解决这个过程中遇到的痛点问题，提升业务处理能力，真正完成一次系统演进，最后结合实战优化整体设计思路。

**基础篇**

一起了解高并发架构的设计理念，建立对高并发系统的初步认知。比如，如何让系统更好地支持高并发、高可用和高扩展 性，带你掌握架构分层的核心技术点。

**演进篇**

从数据库、缓存、消息队列、分布式服务、维护这五个角度，讲解系统支持高并发的方法。该模块将带你分析其中的核心技术点，以及系统演进过程中会遇到的问题，从而针对性地解决。还将了解数据库池化技术、主从分离、分库分表等分布式数据库技术。

**实战篇**

以未读数系统设计和信息流设计为例展开介绍。为读书系统实战，主要讲解如何设计方案来抵挡 每秒几十万次的获取用户未读数的请求；信息流设计实战，讲解如何做通用信息流的推模式和拉模式。实战篇内容操作性强，能检验你对技术点的掌握程度，和灵活运用程度，是完善你知识体系的重要环节。

## The Course Catalog

《高并发系统设计 40 问》

```
https://time.geekbang.org/column/intro/230
```

```
开篇词  为什么你要学习高并发系统设计？
```

###  基础篇
```
01  高并发系统： 它的通用设计方法是什么？

02  架构分层： 我们为什么一定要这么做？

03  系统设计目标（一）：如何提升系统性能？

04  系统设计目标（二）：系统怎样做到高可用？

05  系统设计目标（三）：如何让系统易于扩展？

06  面试线程第一期

```

###  演进篇

#### 数据库篇
```
07  池化技术：如何减少频繁创建数据库连接的性能损耗？

08  数据库优化方案（一）：查询请求增加时，如何做主从分离？

09  数据库优化方案（二）： 写入数据量增加时，如何实现分库分表？

10  发号器： 如何保证分库分表后 ID 的全局唯一性？

11  NoSQL： 在高并发场景下，数据库和 NoSQL 如何做到互补

```


#### 缓存篇
```
12  缓存：数据库成为瓶颈后，动态数据的查询要如何加速？

13  缓存的使用姿势（一）：如何选择缓存的读写策略？

14  缓存的使用姿势（二）：缓存如何做到高可用？

15  缓存的使用姿势（三）：缓存穿透来怎么办？

16  CDN： 每天亿级别静态资源请求要如何加速？

加餐  数据迁移应该如何做？

```


#### 消息队列篇
```
17  消息队列： 秒杀时如何处理每秒上万次的下单请求？

18  消息投递： 如何保证消息仅仅被消费一次？

19  消息队列： 如何降低消息队列系统中消息的延迟？

20  面试现场第二期

用户故事  从“心”出发，我还有无数个可能

高并发系统设计 期中测试（100分）


```

#### 分布式服务篇
```
21  系统架构： 每秒1万次请求的系统要做服务化拆分吗？

22  微服务架构： 微服务化后，系统架构要如何改造？

23  RPC框架： 10万 QPS下如何实现毫秒级的服务调用？

24  注册中心： 分布式系统如何寻址？

25  分布式 Trace： 横跨几十个分布式组件的慢请求要如何排查？

26  负载均衡： 怎么样提升系统的横向扩展能力？

27  API 网关： 系统的门面要作何选择？

28  多数据中心： 跨地域的分布式系统如何做？

29  Service Mesh： 如何屏蔽分布式系统的服务治理细节？


```

#### 维护篇
```
30  给系统加上眼睛： 服务端监控要怎么做？

31  应用性能管理： 用户的使用体验应该如何监控？

32  压力测试： 怎样设计全链路压力测试平台？

33  配置管理： 成千上万的配置项要如何管理？

34  降级： 如何屏蔽非核心系统故障的影响？

35  流量控制： 高并发系统中我们如何操纵流量？

36  面试现场第三期

```

### 实战篇
```
37  计数系统设计（一）： 面对海量数据的计数器要如何做？

38  计数系统设计（二）： 50 万 QPS 下如何设计未读数系统？

39  信息流设计（一）： 通用信息流系统的推模式要如何做？

40  信息流设计（二）： 通用信息流系统的拉模式要如何做？

-- 结束语

结束语  学不可以已

春节特别策划   高并发下如何发现和排查问题？

春节特别策划   我们如何准备抵抗流量峰值？

结课测试   高并发系统设计的相关知识，你都掌握了吗？

```



