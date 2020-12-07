# Elasticsearch全文搜索引擎

## 为什么用Elasticsearch
他可以快速的存储，搜索和分析海量数据。
在一些应用场景，如商城的数据越来越多，如果使用模糊查询，模糊查询会放弃索引，直接扫表，效率非常低。Elasticsearch使用一种倒序索引的方式，可以实现全文索引。非常有效的解决这个问题。

什么是倒序索引?
正序索引：100个页面，每个页面都有一个tag，将所以的文章都检索提取出所有的tag，这就是正序索引
倒序索引：给定一个tag，找到包含他的全部页面。

例如百度搜索时，需要给定一个关键词，返回所有包含他的页面，这就是倒序索引。
过程
```
id      content
1       秋水浮萍
2       秋水任缥缈
3       一叶浮萍任缥缈

首先进行分词
id      content
1       秋水,浮萍
2       秋水，任缥缈
3       一叶，浮萍，任缥缈

然后建立词到文档的映射
id      content
秋水    1，2
浮萍    1，3
任缥缈  2，3
一叶    3
```
这样，在搜索的场景下可以很快速的查到结果
## 核心概念
1. Cluster 集群 & Node 节点

Elastic 本质上是一个分布式数据库，允许多台服务器协同工作，每台服务器也可以运行多个Elastic实例。每个elatic实例就是一个节点，一组节点构成一个集群。

2. Index & Type & Document

Index，是单个数据库的同义词，即等于Databases
Type, 类似于table,区别是他是虚拟的逻辑分组，用来过滤document
Document, 类似于row,表示单条记录

## 操作
操作使用的是rest接口
### Index
1. 新增
```bash
curl -X PUT "localhost:9200/weather"
# 创建一个weather的index
{
    "acknowledged": true, # 表示成功
    "shards_acknowledged": true 
}
```
2. 删除

```bash
curl -X DELETE "localhost:9200/weather"
```



