## 描述
二叉搜索树的中序遍历

进阶： 使用迭代算法。

## 分析

```python
def traversal(node):
    # 前序遍历
    traversal(node.left)
    # 中序遍历
    traversal(node.left)
    # 后续遍历
```

使用迭代的话要使用栈来保存

## 代码

使用递归
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        self.traversal(root, result)
        return result

    def traversal(self, root: TreeNode, result: List) -> None:
        if root:
            if root.left:
                self.traversal(root.left, result)
            result.append(root.val)
            if root.right:
                self.traversal(root.right, result)
```

前序遍历：
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        self.traversal(root, result)
        return result


    def traversal(self, root: TreeNode, result: List) -> None:
        if root:
            result.append(root.val)
            if root.left:
                self.traversal(root.left, result)
            if root.right:
                self.traversal(root.right, result)
```

后续遍历
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def postorderTraversal(self, root: TreeNode) -> List[int]:
        result = []
        self.traversal(root, result)
        return result

    def traversal(self, root: TreeNode, result: List) -> None:
        if root:
            if root.left:
                self.traversal(root.left, result)
            if root.right:
                self.traversal(root.right, result)
            result.append(root.val)
```

使用迭代来做：

前序：
```python
```
中序：
```python
```
后序：
```python
```