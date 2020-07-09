"""
快排主要用了分治的思想
1. 选择一个数为基准，小于他的放到左边，大于他的放到右边，这个过程叫做分区
2. 对左右两边实行相同的操作--分区，直到只剩下一个元素
"""
def partition(nums, start, end):
    left = start
    for i in range(start, end):
        if nums[i] < nums[end]:
            nums[left], nums[i] = nums[i], nums[left]
            left += 1
    nums[left], nums[end] = nums[end], nums[left]
    return left


def quick_sort(nums, start, end):
    if end > start:
        pivot = partition(nums, start, end)
        quick_sort(nums, start, pivot-1)
        quick_sort(nums, pivot+1, end)


nums = [3, 1, 2, 4]
quick_sort(nums, 0, len(nums)-1)
print(nums)