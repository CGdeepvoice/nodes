## 描述
给定一个非负的数据a1, a2...an,每个数代表坐标中的一个点(i, ai).
坐标内画n条垂直线，垂直线i的两个端点分别为（i, ai）和(i, 0).找出其中的两条先，使得他们与x轴共同构成的容器可以容纳最多的水。

**说明**: 不能倾斜容器，切n的值最少是2

![avator](images/盛最多的水.jpg)
图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。

Example:
```text
input: [1,8,6,2,5,4,8,3,7]
output: 49
```

## 分析

计算面积，这里需要用到的公式是： `area = (end-start) * min(A[end], A[start])`

计算面积时候，控制面积的因素有两个，长度和高度，在查找过程中，从两端开始命中几率更大一点。
因为要查找，指针要移动，比如一个长的和一个短的，肯定要移动短的，这样才能算出更大的面积。
这里使用的是**双指针**法，就是两个指针从两端向中间靠拢。

## 代码

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        start, end = 0, len(height) - 1
        max_area = 0
        while start < end:
            area = (end - start) * min(height[start], height[end])
            max_area = max(max_area, area)
            if height[start] < height[end]:
                start += 1
            else:
                end -= 1
        return max_area
```
