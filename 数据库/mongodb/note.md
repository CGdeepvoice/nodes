# mongodb

1. Mongodb保存文档为BSON格式，json的二进制格式。文档保存在集合中。
2. mongodb的文档的字段和格式是动态的，可以随便存储。也可以进行校验json格式。

主要结构： db -> collection -> document -> bson
## 视图 
视图是一个聚合查询的结果集。不会持久化到磁盘，每次查询都会更新。视图不支持写操作。
1. 创建 `db.createView()`
2. 删除 `db.collection.drop()`

视图使用基础数据的索引，无法创建删除和修改。
可以使用 $merge into来保存
```js
updateMonthlySales = function(startDate) {
   db.bakesales.aggregate( [
      { $match: { date: { $gte: startDate } } },
      { $group: { _id: { $dateToString: { format: "%Y-%m", date: "$date" } }, sales_quantity: { $sum: "$quantity"}, sales_amount: { $sum: "$amount" } } },
      { $merge: { into: "monthlybakesales", whenMatched: "replace" } }
   ] );
};
```
每次更新调用函数就可以
3. 固定大小的集合。 当达到设置容量时，删除掉旧的数据来保存新的数据。

## 文档
1. 点操作
   1. array `array.index`
   2. 迭代对象 `embedded.field`
2. bson最大为16M，所以单一文档最大16M，如果超过了可以使用GridFS(分布式文件系统)
3. _id字段是保留的主键字段，如果捕食者，会自动使用ObjectId，不可以保存数据。

    ObjectId是唯一的快速生成的12位字节，其中包括：
    - 4个字节时间戳
    - 5个字节随机值
    - 3个字节递增计数器，初始化为随机值

    这里1个字节是8位，8个bit，可以用2个16进制数来表示。



## BJSON
1. 数据类型：String、Object、Array、Undefined、ObjectId、Boolean、Date、Null、Timestamp
2. ObjectId
3. String UTF-8
4. Date() 是一个64位的数字来表示字1970年到现在的毫秒数

## mongo shell
mongo shell 是交互式的js接口。
typeof 
instanceof
## CURD
### 插入
1. `db.mycol.insertOne({})`
2. `db.mycol.insertMany([{}, {}])`

### 查询
1. `db.mycol.find({})`
2. 对于迭代对象：`db.mycol.find({"dict.key": "value"})`
3. 小于 `db.mycol.find({"size.h": {$lt: 15}})`
4. 与 `db.mycol.find({ status: "A", qty : {$lt: 30}})`
5. 或 `db.mycol.find({$or: [{status: 'A'}, {qty: {$lt: 30}}]})`
6. 复合查询，同时使用与和或
   ```js
   db.inventory.find({
       status: 'A',
       $or: [{qty: {$lt: 30}}, {item: /^p/}]
   })
   ```
7. 查询数据大小
   `db.mycol.find({"tags": {$size: 3}})`
8. 查询对象列表时候，需要使用迭代查询，且字段顺序不能改变。
    `db.inventory.find( { "instock": { warehouse: "A", qty: 5 } } )` 这里如果warehouse和qty顺序换了则查询失败。
9. 显示查询结果 `find({}, {_id: 0, name: 1, instock.qty: 1})`
10. 查询空 null

**文本查询**
1. 对文本进行查询时候可以先创建文本索引，每个文档只能创建一个文本索引，但是文本索引可以包含多种格式。 
2. 创建文本索引 `db.mycol.createIndex({name: "text", description: "text"})`
3. 之后可以使用 $text进行查询，后面的查询条件是或的关系 ： 
   ```db.mycol.find({$text: {$search: "java coffee shop"}})```

4. 使用$text精准匹配 
   ```db.mycol.find({$text: {$search: "\"coffee shop\""}})```

5. 排除 coffee
   ```db.mycol.find({$text: {$search: "java shop -coffee"}})```

6. 根据关联程度进行排序

   ```js
   db.mycol.find(
      {$text: {$search: "java coffee shop"}},
      {score: {$meta: "textScore"}}
   ).sort({score: {$meta: "textScore"}})
   ```


### 更新
1. 更新一个 updateOne
   ```js
   db.mycol.updateOne(
       {"item": "parper"}, // 查询 这里就算结果有多个也只会更新一个
       {
           $set: {"size.uom": "cm", "status": "p"}, // 修改数据
           $currentDate: {"lastMondiffied": true} // 当前时间
       }
   )
   ```
2. 更新多个 updateMany 用法同上面一样，查询语句结果应该为多个文档。
3. replaceOne替换一个
### 删除
1. deleteOne
2. deleteMany


### 批量操作
bulkWrite()
对于插入操作分为有序插入和无序插入，无序插入在分片集合中速度更快，默认是有序插入。使用 orsered: false进行无序插入。

1. 在分片集合中的批量插入的策略
   1. 预拆分集合
   2. 进行无序插入
   3. 避免单调递增的插入 递增的插入，会导致永远只在一个chunk上操作，导致性能和单个chunk差不多，最好保证随机，均衡的放入多个分片上。

## 聚合操作
### pipeline
db.mycol.aggregate({})
1. $match 过滤
2. $group 分组  groupby
3. $sum  计算合计

## 副本集
副本集是具有自动故障恢复的主从集群。由一个活跃节点（primary)和一个或者多个备份节点（secondary)构成。当活跃节点发生故障，备份节点会自动变为活跃节点。以前的活跃节点恢复之后会变成备份节点。

不同的节点角色：
   - standard 常规节点，存储一份完整的数据副本，参与选举投票，可能会称为活跃节点
   - passive 被动节点，存储了完整的数据副本，参与投票，不能成为活跃节点
   - arbiter 仲裁者只参与投票，不接受复制的数据，也不能成为活跃节点

设置用途：
   - 读扩展  对于读密集型应用，可以从从节点进行读取数据，减轻主节点压力
   - 利用从节点进行聚合操作，减轻压力

**工作原理**
主节点负责处理客户端的请求，记录所有操作。从节点负责映射主节点的数据，定期轮询主节点获得这些操作，对自己执行。从而可以与主节点保持数据同步。

1. oplog 主节点的操作记录称为oplog(opreatrion log)，它只记录改变数据库状态的操作（查询不算）。所有操作会转变为幂等的，操作多次结果一样。
2. 同步 启动从节点后，会对主节点的数据进行完整的复制。

## 分片
将数据拆分，放入不用的机器上。也叫分区。

分片之前，会启用一个路由进程，负责数据和分片之间的路由。
1. 片键， 分片时需要选择一个字段作为数据拆分的依据，叫做片键。比如按照名字作为片键，将A-F放到一个片。。。
