## 描述
给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。

你的算法时间复杂度必须是 O(log n) 级别。

如果数组中不存在目标值，返回 [-1, -1]。

示例 1:

输入: nums = [5,7,7,8,8,10], target = 8
输出: [3,4]
示例 2:

输入: nums = [5,7,7,8,8,10], target = 6
输出: [-1,-1]

## 分析
模式识别: logn, 排序数组
二分法

第一次寻找左边界，遇到中点时候向左移动。因为退出时 left = right + 1
左边界可能超了，检查是否找到了
如果第一次没找到，直接退出了
如果第一次找到了，就找右边界。遇到中点就右移动。
退出时就算最后一个是右边界，返回的left也是right+1, 所以结果要-1

## 代码

```python
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        left = self.left_bound(nums, target)
        if left == -1:
            return [-1, -1]
        return [left, self.right_bound(nums, target)-1]

    def left_bound(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + (right-left)//2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            elif nums[mid] == target:
                right = mid - 1
        if left >= len(nums) or nums[left] != target:
            return -1
        return left
 
    def right_bound(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = left + (right-left)//2
            if nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
            elif nums[mid] == target:
                left = mid + 1
        if right < 0 or nums[right] != target:
            return -1
        return left
```