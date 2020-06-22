# 描述
LRU 是一种缓存淘汰策略

因为缓存容量有限，所以缓存满了的时候需要删除一些数据，这个策略就规定了怎么删除以及删除那些数据。

简单讲就是用一个链表来存储缓存。每次`cache.get(key)`，将`key`对应的缓存提升到队首。每次`cache.set(key)`的时候检查缓存的容量，如果满了就删掉链表最后一个，将新的放到队首。

这里用到了双向链表来存储，因为会有队首队尾，用双向链表可以很轻松的实现删除和新增到队首的功能。每次的复杂度都是O(1),如果用普通的链表，每次删除都要从队首找到`node.pre`，单向的没有，只能遍历复杂度太高了。

还有一个就是如何快速的检查一个Key在不在缓存中呢，肯定是用哈希来检查，哈希表的value可以用来存放节点的指针，这样每次get的时候，可以直接拿到指针。

# python实现

```python

class Node:
    # 单节点
    def __init__(self, key, x):
        self.value = x
        self.key = key
        self.next = None
        self.pre = None
        

class DoubleList:
    # 双向链表 可以直接用list替换，这里练习链表操作
    def __init__(self):
        self.head = Node('head', -1)
        self.tail = Node('tail', -1)
        self.head.next = self.tail
        self.tail.pre = self.head
        self.size = 0
    
    def addFirst(self, node: Node):
        # 实现将一个元素加到队首
        self.head.next.pre = node
        node.next = self.head.next
        self.head.next = node
        node.pre = self.head
        self.size += 1

    def remove(self, node: Node):
        # 删除一个节点
        node.next.pre = node.pre
        node.pre.next = node.next
        self.size -= 1
        return node

    def removeLast(self):
        # 删除最后一个元素
        return self.remove(self.tail.pre)


class LRUCache:
    # 实现两个功能， get,set
    # 包含两个容器，一个哈希表，一个双向链表


    def __init__(self, size):
        self.size = size
        self.hashmap = dict()
        self.doubleList = DoubleList()
    def get(self, key):
        # 如果在哈希表里，就取出对应指针，在列表里取出值，并在链表里将他的位置提到最前面
        # 如果不在哈希表里，直接返回空
        if key in self.hashmap.keys():
            node = self.hashmap.get(key)
            result = node.value
            node = self.doubleList.remove(node)
            self.doubleList.addFirst(node)
            return result
        else:
            return None
    
    def set(self, key, value):
        # 判断是否满了，如果容量满了，删除链表最后一个，并把哈希表对应的key删掉，加入新的。
        # 如果没满，直接加到队首
        if key in self.hashmap.keys():
            node = self.hashmap.get(key)
            node = self.doubleList.remove(node)
            self.hashmap.pop(node.key)
        elif self.doubleList.size == self.size:
            node = self.doubleList.removeLast()
            self.hashmap.pop(node.key)
        node = Node(key, value)
        self.doubleList.addFirst(node)
        self.hashmap[key] = node

def test():
    lru = LRUCache(3)
    lru.set('a', 1)
    lru.set('b', 2)
    lru.set('c', 3)
    res = lru.get('a')
    print(res)
    res = lru.get('a')
    print(res)
    res = lru.get('a')
    print(res)
    lru.set('d', 4)
    res = lru.get('b')
    print(res)

```