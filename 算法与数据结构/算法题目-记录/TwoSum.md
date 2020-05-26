## 描述
TwoSum: 给一个整数数组和一个目标值，找到两个元素的和为目标值，不能重复使用一个数。每个题目只有一个答案。

Example:
```text
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].

```

## 分析
1. 找到两个数的和为目标值，最简单的是直接遍历，内外循环，这样可以找到所有的值，但是效率太低了。
2. 进一步分析，两个值的和，直到目标值和一个数，可以用减法算出另外一个数，而且数组的每个元素都可以计算出一个差值。如果第一遍循环保存了差值，第二遍循环检查当前的值有没有在差值里面，就可以把O(n**2)变成 2O（n),数量级就下来了。
3. 不能利用重复的一个数，那就没必要在进行第二遍循环了，在第一遍遍历的时候检查前面的值的差值即可，找到就不用继续算差值和保存了，既省时间又省空间。
4. 这里需要一个容器来保存差值和索引值（因为要返回索引值），检查时候要检查差值在不在容器里，这里就可以用到哈希表，因为哈希表的检查包含复杂度是O(1)。这里不同的语言哈希表的容器不同，Python使用了字典dict,java使用了HashMap<>

## 代码

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        if len(nums) < 2:
            return
        difference = dict()
        for index, value in enumerate(nums):
            if value in difference:
                return difference[value], index
            difference[target-value] = index
```

```java
public static int[] twoSum(int[] nums, int target) {
        HashMap<Integer, Integer> hashMap = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (hashMap.containsKey(nums[i])){
                return new int[]{hashMap.get(nums[i]), i};
            }
            hashMap.put(target-nums[i], i);
        }
        return new int[]{};
    }
```