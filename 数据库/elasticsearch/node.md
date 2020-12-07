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

2. Index & Type & Document & Mapping

Index，是单个数据库的同义词，即等于Databases
Type, 类似于table,区别是他是虚拟的逻辑分组，用来过滤document
Mapping, 类似于schema,定义表的语句
Document, 类似于row,表示单条记录

无需手动创建mapping和type.ES会根据插入的数据自动地创建。

3. 分析器

普通的数据库，如果某个字段没有建立索引，也可以进行查询，只是速度慢一点。但是ES如果不建立索引，只能作为数据的载体。需要定义分析器，或者第三方的分析器，对索引字段进行分词


## 操作
操作使用的是rest接口
### Index
1. 新增
```bash
curl -X PUT "localhost:9200/weather" -d '
{
    "settings": {
        "index": {
            "number_of_replicas": "1", # 设置复制数
            "number_of_shards": "5" # 设置主分片数
        }
    },
    "mappings": { # 创建mapping
    "test_type": { # 在index中创建一个新的type(相当于table)
      "properties": {
        "name": { # 创建一个字段（string类型数据，使用普通索引）
          "type": "string",
          "index": "not_analyzed"
        },
        "age": {
          "type": "integer"
        }
      }
    }
  }
}
'
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

### Mapping
1. 创建mapping

```bash
curl -xPUT 'localhost:9200/index_test/_mapping/test_type' -d '
{
    "test_type": {
        "properties": {
            "name":{
                "type": "string",
                "index": "not_analyzed" # 不分析，直接作为索引
            }
        }
    }
}
'
```
2. 删除mapping

```bash
curl -xDELETE 'localhost:9200/index_test/_mapping/test_type'
```

3. 查看索引的mappings

```bash
curl -xGET 'localhost:9200/index_test/_mapping/test_type'
```
### 文档
1. 新增一个文档

```bash
curl -xPUT 'localhost:9200/index_test/test_type/1?pertty' -d '
{
    "name": "zhangsan",
    "age": "12"
}
'
```
2. 更新一个文档

```bash
curl -XPOST 'localhost:9200/index_test/test_type/1?pretty' -d ' # 这里的1必须是索引中已经存在id，否则就会变成新增文档操作
{
    "name": "lisi",
    "age" : "12"
}'
```
3. 删除一个文档

```bash
curl -XDELETE 'localhost:9200/index_test/test_type/1?pretty' # 这里的1必须是索引中已经存在id
```
4. 查看一个文档

```bash
curl -XGET 'localhost:9200/index_test/test_type/1?pretty'
```

5. 全文搜索

```bash
curl -XGET 'localhost:9200/index_test/test_type/_search' -d'
{
    "query": {
        "match": {
            "name": "zhangsan"
        }
    }
}
'
```
会查询到name中包含zhangsan的所有记录
