## Deque
double ended queue双向队列，允许两侧插入和删除元素。
deque接口继承了Queue接口

**主要方法**
1. void addFirst(E e); 默认的add是加到队尾的，这里可以插入到队首
2. void addLast(E e);
3. boolean offerFirst(E e);
4. boolean offerLast(E e);

上面4个都是新增，可以在双向新增。删除也是一样的
1. E removeFirst(); 删除第一个元素
2. E removeLast();
3. boolean pollFirst();
4. boolean pollLast()
5. boolean removeFirstOccurrence(Object o); 删除第一个与o相同的元素
6. boolean removeLastOccurrence(Object o);

获取元素：
1. E getFist();
2. E getLast();
3. E peekFirst();
4. E peekLast();

因为是继承了Queue,所以对应的add,offer,remove,poll,element,peek都有。

**实现stack**
1. void push(E e); 等价于addFirst()
2. E pop(); 等价于removeFirst()
利用push和pop可以实现stack栈的操作
