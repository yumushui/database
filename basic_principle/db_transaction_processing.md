# Database Transaction processing

## The Art of Database Transaction processing

Transaction Management and Concurrency Control

数据库事务处理的艺术： 事务管理与并发控制

```
目录
推荐序一
推荐序二
推荐序三
推荐序四
推荐序五
推荐序六
前言

第一篇　事务管理与并发控制基础理论

第1章　数据库管理系统的事务原理 2
1.1　事务模型要解决的问题 2
1.1.1　为什么需要事务处理机制 2
1.1.2　事务机制要处理的问题——事务故障、系统故障、介质故障 4
1.1.3　并发带来的问题椚 常见的读数据异常现象 4
1.1.4　并发带来的问题——写并发操作引发的数据异常现象 8
1.1.5　语义约束引发的数据异常现象 9
1.1.6　其他的异常 11
1.1.7　深入探讨三种读数据异常现象 13

1.2　事务处理技术的原理 17
1.2.1　什么是事务 17
1.2.2　事务的属性 20
1.2.3　ACID的实现技术 24

1.3　事务的模型 26

1.4　并发控制技术 27
1.4.1　并发控制技术的实现策略 27
1.4.2　并发控制技术的实现技术 28

1.5　日志技术与恢复子系统31
1.6　本章小结 32

第2章　深入理解事务管理和并发控制技术 33
2.1　在正确性和效率之间平衡 33
2.1.1　隔离级别 34
2.1.2　快照隔离 36
2.1.3　理解可见性 39

2.2　并发控制 40
2.2.1　基于锁的并发控制方法 42
2.2.2　基于时间戳的并发控制方法 47
2.2.3　基于有效性检查的并发控制方法 52
2.2.4　基于MVCC的并发控制方法 53
2.2.5　基于MVCC的可串行化快照隔离并发控制方法 56
2.2.6　再深入探讨三种读数据异常现象 60

2.3　并发控制技术的比较 62
2.3.1　并发控制技术整体比较 62
2.3.2　S2PL和SS2PL的比较 64
2.3.3　事务属性与并发控制技术的关系 65
2.3.4　SCO和SS2PL的比较 66
2.3.5　TO和SS2PL的比较 67

2.4　深入探讨隔离级别 68
2.4.1　隔离级别与基于锁的并发控制方法 68
2.4.2　隔离级别与各种并发控制技术 69

2.5　事务的管理 70
2.5.1　事务的开始 71
2.5.2　事务的提交 71
2.5.3　事务的中止与回滚 72
2.5.4　子事务与SAVEPOINT 72
2.5.5　长事务的管理 73
2.5.6　XA 74

2.6　事务相关的实战问题讨论 75
2.7　本章小结 76


第二篇　事务管理与并发控制应用实例研究

第3章　Informix事务管理与并发控制 78
3.1　Informix的事务操作 78
3.1.1　开始事务 78
3.1.2　提交事务 79
3.1.3　回滚事务 80
3.1.4　XA事务 80
3.1.5　事务模型 82

3.2 Informix的封锁技术 83
3.2.1 锁的级别 83
3.2.2　锁的粒度 84

3.3　隔离级别与数据异常 85
3.3.1　Informix支持的隔离级别 85
3.3.2　隔离级别与日志的模式 86
3.3.3　写偏序异常 87

3.4　本章小结 88

第4章　PostgreSQL事务管理与并发控制 89
4.1　PostgreSQL事务操作 89
4.1.1　开始事务 90
4.1.2　提交事务 90
4.1.3　回滚事务 90
4.1.4　XA事务 91
4.1.5　自动控制事务 91

4.2　SQL操作与锁 92
4.2.1　锁的研究准备 92
4.2.2　INSERT操作触发的锁 94
4.2.3　SELECT操作触发的锁 94
4.2.4　SELECT FOR UPDATE操作触发的锁 97
4.2.5　UPDATE操作触发的锁 100
4.2.6　DELETE操作触发的锁 103
4.2.7　ANALYZE操作触发的锁 106
4.2.8　CREATE INDEX操作触发的锁 106
4.2.9　CREATE TRIGGER操作触发的锁 107
4.2.10　锁的相关参数 108

4.3　隔离级别与数据异常 108
4.3.1　SQL标准定义的三种读异常 108
4.3.2　写偏序异常 115

4.4　本章小结 118

第5章　InnoDB事务管理与并发控制 119
5.1　InnoDB的事务模型 119
5.1.1　开始事务 120
5.1.2　提交事务与回滚事务 121
5.1.3　MySQL的XA 122

5.2　InnoDB基于锁的并发控制 123
5.2.1　基于封锁技术实现基本的并发控制 123
5.2.2　锁的种类 124
5.2.3　锁的施加规则 127
5.2.4　获取InnoDB行锁争用情况 129
5.2.5　死锁 129

5.3　InnoDB基于MVCC的并发控制 130

5.4　隔离级别与数据异常 131
5.4.1　SQL标准定义的三种读异常 131
5.4.2　写偏序异常 134

5.5　本章小结 138

第6章　Oracle事务管理与并发控制 139
6.1　Oracle的事务操作 139
6.1.1　事务管理 139
6.1.2　事务属性和隔离级别 140
6.1.3　XA事务 141

6.2　Oracle的封锁技术 142
6.2.1　元数据锁的级别 142
6.2.2　用户数据锁的级别 143

6.3　MVCC技术 145
6.3.1　MVCC的历史 145
6.3.2　深入理解MVCC 147
6.3.3　Oracle的MVCC 149

6.4　隔离级别与数据异常 157
6.4.1　Oracle支持的隔离级别 157
6.4.2　写偏序异常 158

6.5　本章小结 160


第三篇　PostgreSQL事务管理与并发控制源码分析

第7章　PostgreSQL事务系统的实现 162
7.1　架构概述 162
7.1.1　事务和并发控制相关的文件 162
7.1.2　事务相关的整体架构 164

7.2　事务管理的基础 166
7.2.1　事务状态 166
7.2.2　事务体 171
7.2.3　事务运行的简略过程 172

7.3　事务操作 173
7.3.1　开始事务 173
7.3.2　事务提交 177
7.3.3　日志落盘 179
7.3.4　事务回滚 180
7.3.5　clog 185

7.4　子事务的管理 186
7.4.1　子事务与父事务的区别 186
7.4.2　保存点 187

7.5　本章小结 188

第8章　PostgreSQL并发控制系统的实现—封锁 189
8.1　锁的概述 189
8.1.1　锁操作的本质 189
8.1.2　与锁相关的文件 190
8.1.3　与锁相关的内存初始化 191

8.2　系统锁 192
8.2.1　SpinLock 192
8.2.2　LWLock 198
8.2.3　SpinLock与LWLock比较 213

8.3　事务锁 214
8.3.1　锁的基本信息 214
8.3.2　ReguarLock 221
8.3.3　行级锁 232
8.3.4　Advisory lock（劝告锁） 237

8.4　事务锁的管理 239
8.4.1　获取锁 239
8.4.2　锁查找或创建 242
8.4.3　释放锁 243
8.4.4　锁冲突检测 244

8.5　死锁检测 247
8.5.1　数据结构 247
8.5.2　等待获取锁与死锁处理 248
8.5.3　死锁检测 251
8.5.4　进程唤醒 252

8.6　从锁的角度看用法 254
8.6.1　AccessShareLock 254
8.6.2　RowShareLock 256
8.6.3　RowExclusiveLock 257
8.6.4　ExclusiveLock 258
8.6.5　其他的锁 260

8.7　本章小结 262

第9章　PostgreSQL并发控制系统的实现—MVCC 263
9.1　快照 264
9.1.1　相关文件 264
9.1.2　数据结构 265
9.1.3　快照的类型 268
9.1.4　快照的管理 268
9.1.5　可串行化隔离级别的快照 271

9.2　可见性判断与多版本 273
9.2.1　可见性判断 273
9.2.2　多版本实现 282

9.3　可串行化快照原理 285
9.3.1　理论基础 285
9.3.2　算法实现 287

9.4　PostgreSQL可串行化快照的实现 289
9.4.1　PostgreSQL的状况 289
9.4.2　PostgreSQL实现SSI的理论基础 289
9.4.3　谓词锁数据结构 297
9.4.4　谓词锁操作 306
9.4.5　冲突检测 321

9.5　隔离级别 336
9.5.1　隔离级别 336
9.5.2　各种隔离级别的实现 337

9.6　本章小结 340


第四篇　InnoDB事务管理与并发控制源码分析

第10章　InnoDB事务系统的实现 342
10.1　架构概述 342
10.1.1　事务和并发控制相关的文件 342
10.1.2　事务相关的整体架构 344

10.2　事务管理的基础 346
10.2.1　事务状态 346
10.2.2　表示事务的数据结构 348
10.2.3　UNDO日志与回滚 349
10.2.4　REDO日志 350
10.2.5　内部事务的处理 352
10.2.6　Mini-Transaction 352

10.3　事务操作 353
10.3.1　InnoDB的初始化 354
10.3.2　开始事务 354
10.3.3　提交事务 359
10.3.4　日志落盘 364
10.3.5　回滚事务 367
10.3.6　Mini-Transaction的提交 371
10.3.7　Mini-Transaction的回滚 373
10.3.8　SAVEPOINT 373
10.3.9　XA 375
10.3.10　事务的其他内容 375

10.4　InnoDB事务模型 378

10.5　本章小结 382

第11章　InnoDB并发控制系统的实现—两阶段锁 383
11.1　锁的概述 383
11.1.1　锁操作的本质 383
11.1.2　全局锁表 384
11.1.3　封锁系统的架构 384

11.2　系统锁 386
11.2.1　读写锁 386
11.2.2　Mutex锁 394
11.2.3　其他锁 401

11.3　事务锁之记录锁 401
11.3.1　记录锁的基本数据结构 402
11.3.2　记录锁 408
11.3.3　记录锁与隔离级别 423

11.4　事务锁之元数据锁 433
11.4.1　元数据锁的数据结构 433
11.4.2　元数据锁的管理与使用 450
11.4.3　死锁处理 468

11.5　SQL语义定义锁 476
11.5.1　锁的粒度 476
11.5.2　重要的数据结构 478
11.5.3　InnoDB对接MySQL Server 480

11.6　其他类型的锁 493
11.6.1　Mini-Transaction加锁 493
11.6.2　事务锁之谓词锁 494

11.7　事务与锁 499

11.8　本章小结 500

第12章　InnoDB并发控制系统的实现—MVCC 502
12.1　数据结构 503
12.1.1　MVCC 503
12.1.2　Read View快照 504
12.1.3　事务与快照 505

12.2　可见性判断 506
12.2.1　可见性原则 506
12.2.2　二级索引的可见性 509

12.3　多版本的实现 509
12.3.1　多版本结构 509
12.3.2　多版本生成 510
12.3.3　多版本查找 510
12.3.4　多版本清理 511

12.4　一致性读和半一致性读 511
12.4.1　一致性读 512
12.4.2　半一致性读 512

12.5　本章小结 513

附录　TDSQL简介 514

```
