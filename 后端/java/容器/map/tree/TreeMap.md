## TreeMap
分析前面两个接口SortedMap， NavigableMap都是为了导入TreeMap
由树实现的Map方法，红黑树，是一种平衡树，通过标记红色和黑色的节点，每次新增和删除都进行旋转，使得每条路径的高度不会相差很多。所以增删改查的复杂度都是O(lgN).

**Entry**
首先看下键值对，这里的键值对继承了Map.Entry。并且实现了树的节点。红黑树的特点
先复习一下红黑树 

[红黑树笔记](https://github.com/CGdeepvoice/notes/blob/master/算法与数据结构/算法导论/第三部分数据结构.md#红黑树)