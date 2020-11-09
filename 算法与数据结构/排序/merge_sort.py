"""
归并排序 主要使用了分治的算法，先进行拆分，然后两两合并
1. 利用递归进行拆分，对结果进行合并并返回
"""
def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if left:
        result += left
    if right:
        result += right
    return result

def merge_sort(nums):
    if len(nums) <= 1:
        return  nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)

nums = [3, 1, 2, 4]
res = merge_sort(nums)
print(res)