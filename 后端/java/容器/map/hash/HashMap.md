## HashMap

哈希map，肯定就是哈希函数实现的map了，哈希函数简单来说就是把一个字符串通过计算，得到一个数组，而且不同的字符串得到的数组不同。相同的字符串多次计算结果相同。
HashMap类继承自AbstractMap，实现了Map,Cloneable,Serializable接口

**Node**
这里定义了内部类node继承自Map.Entry，用来保存键值对
```java
static class Node<K,V> implements Map.Entry<K,V> {
    // 这里多保存了一个int型的hash值
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
    // 其他操作就是正常的获取值和修改值，toString,hashCode和equals了
}
```

**工具方法**
```java
static final int hash(Object key) {
    // 根据key计算出他的哈希值
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```
**属性字段**
1. `transient Node<K,V>[] table;`，这里就是根节点了
2. `transient Set<Map.Entry<K,V>> entrySet; ` 

这个类与其他有点区别，他内部不止简单的使用了一种数据结构，使用了数组加链表、红黑树的格式，当容量和链表长度到达一定长度的时候，链表转为红黑树。
所以这里优先看他的put方法

**put**
```java
public V put(K key, V value) {
    // 可以看到，这里会调用到hash(key),利用key的哈希值来存储
    return putVal(hash(key), key, value, false, true);
}
/**
* Implements Map.put and related methods.
* 
* @param hash hash for key  
* @param key the key
* @param value the value to put
* @param onlyIfAbsent if true, don't change existing value  如果为True，不改变现在的值，就是没有更新的作用了
* @param evict if false, the table is in creation mode. 创建模式，主要用来区别通过put添加还是创建时初始化数据的
* @return previous value, or null if none
* 这个函数看起来挺乱的，但是他要做的最终就是把这个键值对插进去而已
*/
final V putVal(int hash, K key, V value, boolean onlyIfAbsent, boolean evict) {
    Node<K,V>[] tab; 
    Node<K,V> p; 
    int n, i;
    // 如果表示空的，需要进行初始化，也就是扩容
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    // 如果找到的这个位置上是空的，就创建一个链表节点，直接放进去
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        // 如果已经有值了，就需要进行校验和转换了。
        Node<K,V> e; K k;
        // 这里就是进行比较的，如果找到的节点p和要加入的节点的哈希值相等，并且键也相同的话，就取出这个节点、
        // 为什么这样算呢，因为位置是进行截取的，整体的哈希值并不一定相同
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        // 如果找到的节点是红黑树，通过调用这个节点的putTreeVal，把节点加进去
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            // 这里就是哈希值不同，键值不同，并且还是链表的
            for (int binCount = 0; ; ++binCount) {
                // 遍历这个链表

                if ((e = p.next) == null) {
                    // 找到结尾了，还是没有相同key的,创建一个链表节点加进去
                    p.next = newNode(hash, key, value, null);
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        // 如果链表的长度超过了8个，那么就需要转变为数
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash &&((k = e.key) == key || (key != null && key.equals(k))))
                    // 遍历过程中找到了相同key的。// 这里的e就是p
                    break;
                p = e;
            }
        }
        // 其实上面的操作就是get_or_create
        if (e != null) { // existing mapping for key
            // 存在这个值的话，其实如果不存在已经加进去了，这里就是为了统一处理起来方便些
            V oldValue = e.value;
            // 根据参数进行判断是否要新增
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            // 这里定义的空的，在linkedHashMap中定义了，可以切入点
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}

final Node<K,V>[] resize() {
    // 这个方法的目的是调整大小，这里调整了大小之后需要移动原有的值
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap, newThr = 0;
    // 这里有两对变量，新旧容量，新旧阈值， 阈值的意思是要调整大小的下一个大笑之，容量*负载系数。
    // 如果不是第一次扩容
    if (oldCap > 0) {
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        // 新的容量是旧容量加倍。如果新的容量小于最大容量并且旧的容量不是以第一扩容。那么阈值也就加倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                    oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1; // double threshold
    }
    // 如果容量是0，但是阈值大于0，那么新的容量就是阈值
    else if (oldThr > 0) // initial capacity was placed in threshold
        newCap = oldThr;
    //这里是第一次初始化，容量就是 DEFAULT_INITIAL_CAPACITY = 1 << 4 aka 16
    else {               // zero initial threshold signifies using defaults
        newCap = DEFAULT_INITIAL_CAPACITY;
        // 新的阈值是 16*0.75
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                    (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    // 上面就是扩容和调整阈值的操作。到这里已经获取到了新的容量和阈值
    @SuppressWarnings({"rawtypes","unchecked"})
    //这里直接创建了新的数组
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    // 如果就的数组不为空
    if (oldTab != null) {
        // 遍历旧数组中的每个键值对
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                // 非空键值对，拿到之后，把原来的位置置为null
                oldTab[j] = null;
                if (e.next == null)
                    // 这里的意思就是，如果这个哈希值得位置只有一个数，它这里没有连接着列表或者树的话
                    // 就把它放到新的位置上，这里用的是 e.hash & newCap-1,其实就是根据容量对哈希值的二进制进行截取，让他能更加分散的分布在整个数组中。这个操作是必要的，不然在新的容量中，相同的key计算出相同的哈希值，但是位置变了，再也找不到这个了。或者说不准确了
                    newTab[e.hash & (newCap - 1)] = e;
                else if (e instanceof TreeNode)
                    // 如果是树的节点，也就是这里连着红黑树，需要进行分解并重新放入
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else { // preserve order
                    // 这里应该就是列表了，遍历列表做准备
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            // 前面的都是 e.hash & cap-1 
                            // 比如两个哈希值5       0x0000 0101， 
                            //             21      0x0001 0101
                            // 旧容量是16 16-1=15   0x0000 1111
                            // 结果就是      5      0x0000 0101  ==> 5
                            //              21     0x0000 0101  ===>5
                            // 所以以前这两个绑在一起，后来扩容到32， 31  0x0001 1111，那么这两个哈希值与的结果就变了，需要进行重新分布
                            // 但是所有的都要重新分布吗，并不是， 原来的容量是 16， 0x0001 0000
                            //                             n & cap    n=5   0x0000 0000 == 0
                            //                                        n=21  0x0001 0000 != 0
                            // 这就说明了 哈希值为5的不需要移动了，但是哈希值为21的需要移动。
                            // 为了保证以前加入进来的顺序，以前都是加载尾巴上，这里就用了两套head+tail， loHead,loTail加载了不需要移动的头和尾，另一个则是需要重新移动的头和尾，这两移动之后原来的顺序就不用改变了。
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    if (loTail != null) {
                        loTail.next = null;
                        // 这里也是运用了这个道理，保证了顺序，并且这些值再次计算哈希值还是相同的，与计算的结果也是相同的。所以直接放在原来的位置就行了
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        // 对于需要移动的，其实也就是移动这个hiHead到hiTail之间全部的，直接放进去就行了。
                        // 这个与运算和双列表运用的真的挺巧妙的。
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}

/**
* Replaces all linked nodes in bin at index for given hash unless
* table is too small, in which case resizes instead.
* 就是因为table数组太小了，容易哈希冲突了，需要把链表中的节点转换为树的节点。这时候其实应该扩容的。
*/
final void treeifyBin(Node<K,V>[] tab, int hash) {
    int n, index; Node<K,V> e;
    // 如果表是空的或者数组态度太短了，就直接扩容好了
    if (tab == null || (n = tab.length) < MIN_TREEIFY_CAPACITY)
        resize();
    // 如果这里hash值得位置上有值，就进行转换。防止转换空值
    else if ((e = tab[index = (n - 1) & hash]) != null) {
        TreeNode<K,V> hd = null, tl = null;
        // 把链表中的每个节点转化为树节点
        do {
            TreeNode<K,V> p = replacementTreeNode(e, null);
            //  TreeNode<K,V> replacementTreeNode(Node<K,V> p, Node<K,V> next) {
            //      return new TreeNode<>(p.hash, p.key, p.value, next);
            //  }
            // hd就是头了，把所有的节点连在他后面，用next和prev
            if (tl == null)
                hd = p;
            else {
                p.prev = tl;
                tl.next = p;
            }
            tl = p;
        } while ((e = e.next) != null);
        // 把原来位置上的链表节点p替换为新的树节点hd.这里的树只是一个双向链表
        if ((tab[index] = hd) != null)
            // 进行树化, treeify定义在内部类TreeNode中，这个方法就不分析了，大概意思就是调整红黑树
            hd.treeify(tab);
    }
}
```
他这里的增加一个元素还是挺麻烦的，首先它内部是保存了一个数组。首先检查容量够不够，不够就扩容。然后利用 hash & cap-1 计算出index,然后找到`table[index]`,如果为空就放进去，不为空就看下里面是什么结构。如果是树形结构就加到树中。最麻烦的就是链表类型，遍历整个链表，看看有没有相同的key就是要不要替换，没有的话就加到链表尾部。如果链表长度超过8，那么就转为树来存储，优化查询。这样做的好处呢，就是查询是能得到O(1)的复杂度。查询最快的数据格式之一了。另外的就是hashset了。

**remove**
既然有了新增，肯定就有删除，有树化就有逆转树化的操作，继续分析下。

```java
public V remove(Object key) {
    Node<K,V> e;
    return (e = removeNode(hash(key), key, null, false, true)) == null ? null : e.value;
}
/**
* Implements Map.remove and related methods.
*
* @param hash hash for key
* @param key the key
* @param value the value to match if matchValue, else ignored
* @param matchValue if true only remove if value is equal 是否要值也匹配才删除
* @param movable if false do not move other nodes while removing 是否要移动其他节点，如果为false,删除的时候就不移动其他节点了
* @return the node, or null if none
*/
final Node<K,V> removeNode(int hash, Object key, Object value, boolean matchValue, boolean movable) {
    Node<K,V>[] tab; Node<K,V> p; int n, index;
    // 检查兼赋值，检查表是否为空，长度是否为0，这个索引上是否有索引。 这里赋了4个值，tb, n, p, index
    // 这样写确实简介一些，后面可以尝试
    if ((tab = table) != null && (n = tab.length) > 0 && (p = tab[index = (n - 1) & hash]) != null) {
        Node<K,V> node = null, e; K k; V v;
        // 如果找到的这个位置上的节点就是要删除的，用node来获取
        if (p.hash == hash &&((k = p.key) == key || (key != null && key.equals(k))))
            node = p;
        else if ((e = p.next) != null) {
            // 否则的话就遍历后面的
            if (p instanceof TreeNode)
                // 树形节点就调用他的查找方式来找
                node = ((TreeNode<K,V>)p).getTreeNode(hash, key);
            else {
                do {
                    // 链表就是循环
                    if (e.hash == hash &&
                        ((k = e.key) == key ||
                            (key != null && key.equals(k)))) {
                        node = e;
                        break;
                    }
                    p = e;
                } while ((e = e.next) != null);
            }
        }
        // 到这里是找到节点了
        // 判断下参数，要不要进行值匹配
        if (node != null && (!matchValue || (v = node.value) == value ||
                                (value != null && value.equals(v)))) {
            if (node instanceof TreeNode)
                // 树形的就就调用树的处理方式，movable这里的作用就是，删除之后要不要调整，不调整也不影响查找，可以在新增的时候再调整，这里是传给他的参数是要调整
                ((TreeNode<K,V>)node).removeTreeNode(this, tab, movable);
            else if (node == p)
                // 如果是第一个的话，就直接更新为第二个
                tab[index] = node.next;
            else
                // 如果是中间的话，就删除这个节点 node = p.next， 删除node
                p.next = node.next;
            ++modCount;
            --size;
            // 这里也是别的类添加回调函数的。
            afterNodeRemoval(node);
            return node;
        }
    }
    return null;
}
```

**获取一个元素**

```java
public V get(Object key) {
    Node<K,V> e;
    // 这里通过三元表达式的判断语句进行了赋值，确实非常方便
    return (e = getNode(hash(key), key)) == null ? null : e.value;
}

/**
* Implements Map.get and related methods.
*
* @param hash hash for key
* @param key the key
* @return the node, or null if none
*/
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    // 经典的判断赋值
    if ((tab = table) != null && (n = tab.length) > 0 && (first = tab[(n - 1) & hash]) != null) {
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            // 检查第一个元素，如果相等就返回了，它的注释也行了，总是检查第一个
            return first;
        if ((e = first.next) != null) {
            // 第一个不是，就检查后面的
            if (first instanceof TreeNode)
                // 如果是树形的，就从树种获取节点，这个速度比链表要快，但是节点数量比链表多
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            do {
                // 他们还挺爱用do while的，检查每个元素，找到就返回了
                if (e.hash == hash && ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

**内部类TreeNode**
这个类是继承自linkedHashMap.Entry，LinkedHashMap.Entry又是继承自HashMap的Node内部类，也就是说树的节点其实继承自链表的节点。但是添加了指针和颜色。
