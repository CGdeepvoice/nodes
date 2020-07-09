"""
希尔排序： 希尔排序是基于插入排序的。插入排序对于前面部分已经有序的复杂度很低，如果全是乱序的则性能差。

1. 以一定的间隔进行比较，交换
2. 缩小间隔继续比较，直到间隔为1.执行完结束
"""

def shell_sort(nums):
    length = len(nums)
    gap = length // 2
    while gap:
        for i in range(gap, length):
            j = i
            while j >= gap and nums[j-gap] > nums[j]:
                nums[j-gap], nums[j] = nums[j], nums[j-gap]
                j -= gap
        gap = gap//2

nums = [4, 2, 1, 5, 10, 20, 40, 2, 4, 5]
shell_sort(nums)
print(nums)