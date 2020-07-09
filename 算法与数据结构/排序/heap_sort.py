"""
堆排序： 使用最大堆，每次取出首部元素，放到后面，直到堆得大小为0

构建堆： 堆是一个完全二叉树，parent_index=i, left_child = 2*i + 1, right_child = left_child+1
平衡堆： 从当前节点向下，比较自己和左右节点，选出最大的并且交换，如果发生了交换（最大的不是自己）继续对该分支进行平衡

"""

class Heap:
    def __init__(self, nums):
        self.array = nums
        self.size = len(self.array)
        self.build_heap()
    
    def get_children(self, parent):
        left = parent * 2 + 1
        right = left + 1
        return left, right
    
    def build_heap(self):
        for j in range(self.size//2-1, -1, -1):
            self.fix(j)
    
    def fix(self, parent):
        left, right = self.get_children(parent)
        lagest = parent
        if left < self.size and self.array[left] > self.array[lagest]:
            lagest = left
        if right < self.size and self.array[right] > self.array[lagest]:
            lagest = right
        
        if lagest != parent:
            self.array[lagest], self.array[parent] = self.array[parent], self.array[lagest]
            self.fix(lagest)
    
    def heap_sort(self):
        while self.size > 0:
            self.array[0], self.array[self.size-1] = self.array[self.size-1], self.array[0]
            self.size -= 1
            self.fix(0)
        return self.array

nums = [3, 1, 2, 4]
r = Heap(nums).heap_sort()
print(r)