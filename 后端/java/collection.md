# 新坑 容器源码分析
Collection容器系列代码在java.base/java/util 下面

# 

# 部分源码算法分析

## ArrayList.batchRemove
先贴出源码
```java
// removeAll会调用这个方法进行删除，this是源列表，c是要删除的， complement=False
// 目的是删除this中包含在c中的元素。
boolean batchRemove(Collection<?> c, boolean complement, int from, int end) {
        Objects.requireNonNull(c);
        Object[] es = this.elementData;

        for(int r = from; r != end; ++r) {
            if (c.contains(es[r]) != complement) {
                int w = r++; // 遇到在c中的代码时，保存位置为当前位置，这里是int w = r； r++的合并

                try {
                    for(; r < end; ++r) {
                        // 这个循环很有意思， 一直循环，当遇到一个没在c中的元素时，把他放到w中，然后w自增。
                        // 如果一直在c中，就一直向后找，等于把没在c中的前移。
                        Object e;
                        if (c.contains(e = es[r]) == complement) {
                            es[w++] = e;
                        }
                    }
                } catch (Throwable var12) {
                    System.arraycopy(es, r, es, w, end - r);
                    w += end - r;
                    throw var12;
                } finally {
                    // 保存修改数量
                    this.modCount += end - w;
                    // 这里会把w 到 end位置的元素置为Null,方便gc
                    this.shiftTailOverGap(es, w, end);
                }
                // 这里就已经完成了，会遍历全部的
                return true;
            }
        }
        // 没有删除，表示没有要删除的。
        return false;
    }
```
有趣的是，retainAll方法调用和removeAll差不多，只有complement=True,这个结果就刚好相反，保留的都是在两个集合中的交集。而且保存在源列表中。
## Arrays.sort()
这里根据参数会从两种排序算法中二选一
1. merage归并算法

```java
private static void mergeSort(Object[] src, Object[] dest, int low, int high, int off, Comparator c) {
    int length = high - low;
    int destLow;
    int destHigh;
    if (length < 7) {
        // 长度小的话，直接用插入算法
        for(destLow = low; destLow < high; ++destLow) {
            for(destHigh = destLow; destHigh > low && c.compare(dest[destHigh - 1], dest[destHigh]) > 0; --destHigh) {
                swap(dest, destHigh, destHigh - 1);
            }
        }

    } else {
        destLow = low;
        destHigh = high;
        low += off;
        high += off;
        int mid = low + high >>> 1;
        mergeSort(dest, src, low, mid, -off, c);
        mergeSort(dest, src, mid, high, -off, c);
        if (c.compare(src[mid - 1], src[mid]) <= 0) {
            System.arraycopy(src, low, dest, destLow, length);
        } else {
            int i = destLow;
            int p = low;

            for(int q = mid; i < destHigh; ++i) {
                if (q < high && (p >= mid || c.compare(src[p], src[q]) > 0)) {
                    dest[i] = src[q++];
                } else {
                    dest[i] = src[p++];
                }
            }

        }
    }
}
```
2. TimSort
TimSort是归并排序做了大量优化的版本。 java.base/java/util/TimSort.class
