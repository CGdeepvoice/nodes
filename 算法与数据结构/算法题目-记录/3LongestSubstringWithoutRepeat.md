## 描述
给定一个字符串，返回字符串中最长的不重复的子串。

Example 1
```text
Input: "abcabcbb"
Output: 3 
Explanation: The answer is "abc", with the length of 3. 
```

Example 2
```text
Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

Example 3
```text
Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. 
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
```
## 分析
1. 这里查找不重复的子串，用到了滑动窗口。查找重复的，首先想到的是哈希表，可以把索引保存在value里面，Key里面保留字符。
2. 当没有出现重复的时候，只需要计算当前长度和最大长度并更新。
3. 出现重复的时候，需要更新当前的起始值，就是重复元素在哈希表中的索引值得下一个。这里有一个地方，如果出现一个值但是他出现在哈希中的索引比起始值小，说明已经跨越他了，不用管。。

![avator](images/滑动窗口.png)

## 代码

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        container = dict() # 存放每个值得索引位置
        start, max_len = 0, 0   # 起点，当出现重复元素时候，前一个重复元素的下一个元素就是起始位置
        for index, value in enumerate(s):
            if value not in container or container[value] < start: #  如果当前元素不是重复元素，并且就算以前出现过当时是在上一个重复之前的就不用管，直接计算值。 
                                                                   #  例如 bacab  计算第二个B的时候，就算在container里面出现过，但是start已经变了，就不管了。只计算start的差值就够了。
                max_len = max(max_len, index - start + 1)
            else:
                start = container[value] + 1
            container[value] = index # 无论怎样都要更新索引值。
        return max_len
```

```java
package basic.leetcode;

import java.util.HashMap;

public class LongestSubstringWithoutRepeat {
    public int lengthOfLongestSubstring(String s) {
        HashMap<Character, Integer> container = new HashMap<>();
        int maxLen = 0;
        int start = 0;
        for (int i = 0; i < s.length(); i++) {
            if (!container.containsKey(s.charAt(i)) || container.get(s.charAt(i)) < start){
                maxLen  = Math.max(maxLen, i - start + 1);
            } else{
                start = container.get(s.charAt(i)) + 1;
            }
            container.put(s.charAt(i), i);
        }
        return maxLen;
    }
}
```