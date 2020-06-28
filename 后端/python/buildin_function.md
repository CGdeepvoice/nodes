# 数学相关
1. 最大公约数：辗转相除法
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```
2. 最大公约数： 两数值积除以最大公约数
```python
a*b/gcd(a, b)
```

3. 等差数列只和：
```python
a1 + a2 ...+ an: 
an = a1 + (n-1)*d
sum = (a1 + an) * n / 2 = (a1 + a1+  (n-1)*d) *n /2
    = 2(a1+(n-1)*d) * n / 2
    = (2*a1*n + (n-1)*n*d )/2
    = a1*n + (n-1)* n *d/2
```

# python
1. str.endwith
2. list.sort 无返回值，直接在源列表进行排序
3. round(num, n) 保留几位小数
4. str = str.replace() 修改在一个新的字符串并返回
5. iteration.product(l1, repeat=3) 笛卡尔积
6. iteration.permutations(l1)  全排列
7. bin(int) 10进制转2进制 
8. oct(int) 10进制转8进制
9. hex(int) 10进制转16进制
10. 正无穷 `float('inf')` 负无穷 `-float('inf')`
11. ord() 返回字符的asicII码
12. chr() ASICII码转字符