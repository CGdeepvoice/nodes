## NavigableMap
NavigableMap接口继承了SortedMap,也是可排序，新增了一些功能。
可导航的map,提供了对已经排序的map的操作，可以找到一个元素，找到比他比他大或者小的元素。可以排序倒序之类的

```java
// 这里是复制的网上的资料
// 找到第一个比指定的key小的值
Map.Entry<K,V> lowerEntry(K key);

// 找到第一个比指定的key小的key
K lowerKey(K key);

// 找到第一个小于或等于指定key的值
Map.Entry<K,V> floorEntry(K key);

// 找到第一个小于或等于指定key的key
K floorKey(K key);

//  找到第一个大于或等于指定key的值
Map.Entry<K,V> ceilingEntry(K key);

K ceilingKey(K key);

// 找到第一个大于指定key的值
Map.Entry<K,V> higherEntry(K key);

K higherKey(K key);

// 获取最小值
Map.Entry<K,V> firstEntry();

// 获取最大值
Map.Entry<K,V> lastEntry();

// 删除最小的元素
Map.Entry<K,V> pollFirstEntry();

// 删除最大的元素
Map.Entry<K,V> pollLastEntry();

//返回一个倒序的Map
NavigableMap<K,V> descendingMap();

// 返回一个Navigable的key的集合，NavigableSet和NavigableMap类似
NavigableSet<K> navigableKeySet();

// 对上述集合倒序
NavigableSet<K> descendingKeySet();
```