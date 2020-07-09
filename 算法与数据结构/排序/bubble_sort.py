"""
冒泡排序， 每次交换相邻之间的元素，将最大的值放到最后一个，最大的就浮到了顶端，继续冒泡剩余的元素
时间复杂度： O(N^2)
"""

def bubble_sort(nums):
    length = len(nums)
    for i in range(length-1, -1, -1):
        for j in range(i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums

res = bubble_sort([3, 1, 4, 10])
print(res)