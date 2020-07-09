"""
选择排序，每次选出最小的一个，放到首部，与冒泡的不同是，它每个循环只会交换一次，但是复杂度相同
"""

def select_sort(nums):
    for i in range(len(nums)):
        min_index, min_value = i, nums[i]
        for j in range(i, len(nums)):
            if nums[j] < min_value:
                min_index, min_value = j, nums[j]
        nums[i], nums[min_index] = nums[min_index], nums[i]


nums = [3, 1, 2, 4, 5, 10, 7, 8]
select_sort(nums)
print(nums)