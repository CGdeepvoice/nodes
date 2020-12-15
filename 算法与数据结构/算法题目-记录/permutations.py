# 全排列
# 把每个字符都放在队首进行，递归
class Solution:
    def permutation(self, nums, max):
        result = []
        def pm(result, tmp_list, nums, index, max):
            if index == max:
                result.append(tmp_list)
            for i in range(0, len(nums)):
                pm(result, tmp_list+[nums[i]], nums[:i]+nums[i+1:], index+1, max)
        pm(result, [], nums, 0, max)
        return result

s = Solution()
x = s.permutation(['a', 'b', 'c', 'd'], 3)
print(x)
