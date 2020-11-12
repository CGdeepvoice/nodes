## TreeMap
分析前面两个接口SortedMap， NavigableMap都是为了导入TreeMap
由树实现的Map方法，红黑树，是一种平衡树，通过标记红色和黑色的节点，每次新增和删除都进行旋转，使得每条路径的高度不会相差很多。所以增删改查的复杂度都是O(lgN).


**红黑树**

[红黑树笔记](https://github.com/CGdeepvoice/notes/blob/master/算法与数据结构/算法导论/第三部分数据结构.md#红黑树)


红黑树是一种平衡二叉搜索树。 二叉搜索树是一种对搜索有好的数，类似于二分法，每个节点左子树小于该节点，右子树大于该节点。要检索一个值可以很快的找到，只要比较树的高度个节点，一共有n个节点，复杂度是Lgn.
但是二叉树有缺点，如果一直新增元素在一个方向上，就成了链表，查询的复杂度就是N，为了保持平衡，在新增和删除节点的时候会对树做一些调整，通过旋转来使二叉树不存在一边倒的形式。常见的有两种一种是AVL树，在每个节点保存当前的高度，当同一级的节点的高度差大于等于2的时候，就进行旋转。根据子树的形态会进行左旋右旋，先左旋后右旋或者相反。但是这样的策略会让旋转操作太频繁了，插入和删除的复杂度就高了。就有了红黑树。
红黑树有5个性质，每次新增和删除都要保持这5个性质：
1. 节点是红色或者黑色
2. 根是黑色
3. 叶子节点是黑色
4. 每个红色节点必须有两个黑色的子节点，不能连续的红色节点
5. 从任一节点到他的每个叶子节点的简单路径都有相同数目的黑色节点。

红黑树不用每次都旋转，他可以进行染色操作，每次保持这5个特性就行了。他是近似平衡不是完全平衡的，所以不需要频繁的调整。
这里使用红黑树来实现TreeMap,应该就是这样了，每个Entry都是一个节点，TreeMap只要持有其根节点就行了，每次的增删查都是对红黑树进行操作的。
这里的情况太多了，要考虑父节点的颜色，父亲的兄弟节点的颜色等等，看看这里具体怎么写的
这里的进度太慢了，快一周了这几个容器还没看完，争取今天看完，看完了TreeMap,HashMap和HashSet，可以继续学习springBoot,周五把springboot视频看完，笔记记录，周末试着写个SSM项目。下周进行整体复习加框架学习，复习一周加写简历。



**Entry**
首先看下键值对，这里的键值对继承了Map.Entry。并且实现了树的节点。红黑树的特点
每个Entry有几个属性
```java
K key; // 保存key
V value; // 保存value
Entry<K,V> left; // 左孩子
Entry<K,V> right; // 右孩子
Entry<K,V> parent; 
boolean color = BLACK;
```

方法简介:
这里的方法就是获取和修改值，和进行比较，具体的操作在主类中定义的。


**TreeMap**树的相关操作

```java
final Entry<K,V> getFirstEntry() {
    // 获取第一个键值对，就是最左边的一个，这里使用的是中序遍历，第一个值就是最左边的元素了
    Entry<K,V> p = root;
    if (p != null)
        while (p.left != null)
            p = p.left;
    return p;
}
final Entry<K,V> getLastEntry() {
    // 右子树，中序遍历的最后一个
    Entry<K,V> p = root;
    if (p != null)
        while (p.right != null)
            p = p.right;
    return p;
}
static <K,V> TreeMap.Entry<K,V> successor(Entry<K,V> t) {
    // 获取一个节点的后继节点，后继节点就是树的中序遍历中，这个节点后面的一个，也就是比这个节点的key大的最小值
    // 这时候需要考虑两种情况：
    // 1. 这个节点有没有右子树，如果有右子树，后继节点就是右子树中最小的值，也就是右子树中的左子节点
    // 2. 如果没有右子树，就需要向上找，知道找到某个点x，这个x不是他的父节点的右子树就行了，那么这个父节点就是后继节点了，因为只要是右子树的，那么这个点的父节点就会小于它，所以我们要找到在左边子树的父节点，而且从这个点x到t,所有的点都在这个父节点的左边，都比他小，所以这个父节点就是后继节点了
    if (t == null)
        return null;
    else if (t.right != null) {
        Entry<K,V> p = t.right;
        while (p.left != null)
            p = p.left;
        return p;
    } else {
        Entry<K,V> p = t.parent;
        Entry<K,V> ch = t;
        while (p != null && ch == p.right) {
            ch = p;
            p = p.parent;
        }
        return p;
    }
}
/**
* Returns the predecessor of the specified Entry, or null if no such.
*/
static <K,V> Entry<K,V> predecessor(Entry<K,V> t) {
    // 要找前驱节点也是一样的。就是找中序遍历中他的前一个点，比他小的最大的一个值
    // 如果有左子树，就是左子树的最大值
    // 如果没有左子树，就向上找，找到节点x，x是他的父节点的左子树，这个父节点就是前驱节点了。
    if (t == null)
        return null;
    else if (t.left != null) {
        Entry<K,V> p = t.left;
        while (p.right != null)
            p = p.right;
        return p;
    } else {
        Entry<K,V> p = t.parent;
        Entry<K,V> ch = t;
        while (p != null && ch == p.left) {
            ch = p;
            p = p.parent;
        }
        return p;
    }
}
```
其实这里没必要分析跨节点从左到右来找，因为是中序遍历，最差情况也就是根节点了，不会经过他来找的。
这里封装了前驱和后继是为了后面旋转时候使用

左旋右旋，fixAfterDeletion，这些操作等后面有时间再来补吧，看算法导论时候看过了，也懂了但是现在又忘了，太麻烦了这些操作


继续看Map的构成
1. 检查键
```java
public boolean containsKey(Object key) {
    return getEntry(key) != null;
}
public V get(Object key) {
    // 获取键值对，常见的map.get方法了
    Entry<K,V> p = getEntry(key);
    return (p==null ? null : p.value);
}
final Entry<K,V> getEntry(Object key) {
    // 这个comparator是用来作比较的，因为保存的key不一定是数组，可能是字符串或者其他类型，红黑树是搜索树，有顺序的，所以需要Key能进行比较
    // Offload comparator-based version for sake of performance
    if (comparator != null)
        return getEntryUsingComparator(key);
    if (key == null)
        throw new NullPointerException();
    @SuppressWarnings("unchecked")
        Comparable<? super K> k = (Comparable<? super K>) key;
    Entry<K,V> p = root;
    // 这里就是树的查找，lgN
    while (p != null) {
        int cmp = k.compareTo(p.key);
        if (cmp < 0)
            p = p.left;
        else if (cmp > 0)
            p = p.right;
        else
            return p;
    }
    return null;
}
```
2. 检查value
```java
public boolean containsValue(Object value) {
    // 这里就是要遍历所有的节点来查找，三种方式前序遍历中序遍历和后续遍历。这里使用了中序遍历，左中右
    // 先找到最左边的节点，每次循环找到他的后继节点。其实这里的复杂度要高于n了，比数组的检查还要慢
    for (Entry<K,V> e = getFirstEntry(); e != null; e = successor(e))
        // 这里就是简单的比较，如果相等就找到了
        if (valEquals(value, e.value))
            return true;
    return false;
}
final Entry<K,V> getFirstEntry() {
    Entry<K,V> p = root;
    if (p != null)
        while (p.left != null)
            p = p.left;
    return p;
}
```
3. put方法，新增和删除应该是最难的一部分了，所有树的操作就在这里了,这里简单分析一下
   
```java
public V put(K key, V value) {
    // 获取根，
    Entry<K,V> t = root;
    if (t == null) {
        compare(key, key); // type (and possibly null) check

        root = new Entry<>(key, value, null);
        size = 1;
        modCount++;
        return null;
    }
    int cmp;
    Entry<K,V> parent;
    // split comparator and comparable paths
    Comparator<? super K> cpr = comparator;
    // 这两个分支，一个是用定义在类中的比较器，一个是用key自带的compareTo方法来比较，只要能进行比较就行了，看默认的吧
    if (cpr != null) {
        do {
            parent = t;
            cmp = cpr.compare(key, t.key);
            if (cmp < 0)
                t = t.left;
            else if (cmp > 0)
                t = t.right;
            else
                return t.setValue(value);
        } while (t != null);
    }
    else {
        if (key == null)
            throw new NullPointerException();
        // 把key强转为可以比较的类型
        @SuppressWarnings("unchecked")
            Comparable<? super K> k = (Comparable<? super K>) key;
        do {
            // 一直找，找到能放下的位置，这个put还是可以修改value的
            parent = t;
            cmp = k.compareTo(t.key);
            if (cmp < 0)
                t = t.left;
            else if (cmp > 0)
                t = t.right;
            else
                // 如果找到t已经存在了就修改值
                return t.setValue(value);
        // 退出条件是找到了叶子节点，也就是不存在，不过这时候已经获取到了他的parent,这要吧这个节点插入进去，就可以进行下一步了
        } while (t != null);
    }
    // 把键值对封装成节点
    Entry<K,V> e = new Entry<>(key, value, parent);
    //这里就是插入进去了
    if (cmp < 0)
        parent.left = e;
    else
        parent.right = e;
    // 插入之后修复红黑树的5个性质，显示要判断，然后在变色旋转。标记一下后面再看 TODO:红黑树
    fixAfterInsertion(e);
    size++;
    modCount++;
    return null;
}
```
4. remove操作和put一样，都是找到之后删除，然后验证性质，如果不满足就进行相应的操作。
5. 这里还包含一些其他的使用操作，replace,修改value，
6. pollFirstEntry,pollLastEntry，简化操作吧，还是调用的deleteEntry，不过这里删除的并不是第一个插入或者最后一个插入的，删除的最大值和最小值
7. values, keys，获取全部的key和value。
先看一下values
```java
class TreeMap<K,V>{
    public Collection<V> values() {
        // 这里要获取所有的values
        Collection<V> vs = values;
        if (vs == null) {
            // 默认是没有的，创建一个Values对象
            vs = new Values();
            values = vs;
        }
        return vs;
    }
    class Values extends AbstractCollection<V>{
        public Iterator<V> iterator(){
            // 从下面可以知道，遍历就是从第一个条目，key的最小值，一直找后继到结束
            return new ValueIterator(getFirstEntry());
        }
    }
    final class ValueIterator extends PrivateEntryIterator<V> {
        ValueIterator(Entry<K,V> first) {
            super(first);
        }
        public V next() {
            return nextEntry().value;
        }
    }
    abstract class PrivateEntryIterator<T> implements Iterator<T> {
        Entry<K,V> next;
        Entry<K,V> lastReturned;
        int expectedModCount;

        // 这里就是获取下一个entry了
        final Entry<K,V> nextEntry() {
            Entry<K,V> e = next;
            if (e == null)
                throw new NoSuchElementException();
            if (modCount != expectedModCount)
                throw new ConcurrentModificationException();
            // 其实就是找后继节点
            next = successor(e);
            lastReturned = e;
            return e;
        }
    }
}

```
获取keySet其实是一样的，不过keyset是set不可以重复的。不在重复了。

其实从名字也能看出来，树实现的map,就是用key做了一个树，利用二叉搜索树来实现可比较，利用红黑树来防止树不平衡。其他的增删改查也就是围绕着树的操作。看这个类感觉和看数据结构书差不多的，这些操作其实都是一样。接下来看hashMap