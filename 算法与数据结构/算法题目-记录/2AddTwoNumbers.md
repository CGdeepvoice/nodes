## 描述
给定两个非空的链表，代表两个非空的整数，数字顺序是逆序的，并且么个节点只包含一位数字。
返回一个新的链表来表示他们的和。
可以假设除了数字0之外，这两个数字都不会以0开头。

Example:
```text
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Reason: 342 + 465 = 807
```
## 分析
1. 这个题目重要的是审题，因为看错题目耽误了时间。这里说的是逆序，也就是低位在前，高位在后，计算起来和手工计算没区别，小于10就直接加起来放到新的链表里，大于10直接进位就行了。
2. 这里要保存一个进位，进位的值是0或者1.每次计算都要进行更新进位。
3. 创建新的返回值链表时候，默认第一个是0或者空，返回时记得返回第二个。
4. 循环时候，不要用与操作符，因为只有要一个链表没空就得继续加下去。计算和的时候单独算，哪个没空加哪个，都空的时候就退出了。

## 代码
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1.val == None:
            return l2
        if l2.val == None:
            return l1
        
        result = ListNode(None)
        l3 = result
        carry = 0
        while l1 or l2 or carry:
            tmp_sum = carry
            if l1:
                tmp_sum += l1.val
                l1 = l1.next
            if l2:
                tmp_sum += l2.val
                l2 = l2.next
            if tmp_sum > 9:
                tmp_sum = tmp_sum - 10
                l3.next = ListNode(tmp_sum)
                carry = 1
            else:
                l3.next = ListNode(tmp_sum)
                carry = 0
            l3 = l3.next
        return result.next
```

```java
class ListNode {
    int val;
    ListNode next;
    ListNode(int x) { val = x; }
}
public class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        if (l1 == null){
            return l2;
        }
        if (l2 == null){
            return l1;
        }
        int carry = 0;
        ListNode result = new ListNode(0);
        ListNode l3 = result;
        while (l1 != null || l2!= null || carry!=0){
            int tmp_sum = carry;
            if (l1 != null){
                tmp_sum += l1.val;
                l1 = l1.next;
            }
            if (l2 != null){
                tmp_sum += l2.val;
                l2 = l2.next;
            }
            if (tmp_sum < 10){
                l3.next = new ListNode(tmp_sum);
                carry = 0;
            } else{
                l3.next = new ListNode(tmp_sum-10);
                carry = 1;
            }
            l3 = l3.next;
        }
        return result.next;
    }
}
```