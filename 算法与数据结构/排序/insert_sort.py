"""
插入排序： 像扑克牌，从开始到后面，每次选一张牌，从后往前遍历前已排序的子序列，遇到比自己大的，就让他往后走一步，直到遇到不大的，就放进去。
"""
def insert_sort(nums):
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j+1] = nums[j]
            j -= 1
        nums[j+1] = key

nums = [3, 1, 2, 4]
insert_sort(nums)
print(nums)