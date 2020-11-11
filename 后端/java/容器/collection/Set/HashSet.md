## HashSet
先来看一个最简单也比较常见的set,利用hash来实现的set

继承自AbstractSet,实现了set方法
他的内部是利用了一个HashMap来存储的。有点奇怪了，Map内部也用到了Set接口，我还是先去看Map接口。