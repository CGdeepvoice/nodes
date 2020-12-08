"""
input: 3+2*{1+2*[-4/(8-6)+7]}
output: 25

思路：中缀表达式转为后缀表达式
方法：利用两个栈，一个保存操作数，一个保存符号。
遍历字符串，遇到数字，保存到操作数栈，遇到符号进行比较。
如果是 + - * /， 先对特殊情况处理，如果是-,需要判断是否是第一个元素，或者-前面不是数字和),这样就是负数，在前面加一个0
其他情况，比较当前符号与操作符栈顶的优先级比较，如果压不住，就弹出操作符到数据栈。如果压得住就方进入。
遇到（，直接压入操作符栈，遇到),需要开始弹出，找到（为止。

最后计算后缀表达式，就是找操作符，找到之后弹出之前的两个操作数，进行运算并放入第一个位置。知道数组只有一个值。
"""
def pri(x):
    if x == "(":
        return 1
    if x in ["+", "-"]:
        return 2
    if x in ["*", "/"]:
        return 3

def cal(t1, t2, t3):
    if t3 == "+":
        return int(t1) + int(t2)
    elif t3 == "-":
        return int(t1) - int(t2)
    elif t3 == "*":
        return int(t1) * int(t2)
    elif t3 == "/":
        return int(t1) // int(t2)

while True:
    try:
        s = input()
        s = s.replace("{", "(").replace("}", ")")
        s = s.replace("[", "(").replace("]", ")")
        data = []
        opr = []
        i = 0
        while i < len(s):
            if s[i].isdigit():
                j = i
                while i < len(s) and s[i].isdigit():
                    i += 1
                data.append(s[j:i])
            elif s[i] in ["+", "-", "*", "/"]:
                if s[i] == "-":
                    if i == 0 or (not s[i-1].isdigit() and s[i-1] != ")"):
                        data.append("0")
                if not opr:
                    opr.append(s[i])
                else:
                    if pri(s[i]) > pri(opr[-1]):
                        opr.append(s[i])
                    else:
                        while opr and pri(opr[-1]) >= pri(s[i]):
                            data.append(opr.pop())
                        opr.append(s[i])
                i += 1
            else:
                if s[i] == "(":
                    opr.append(s[i])
                else:
                    while opr[-1] != "(":
                        data.append(opr.pop())
                    opr.pop()
                i += 1
        while opr:
            data.append(opr.pop())
        
        print(data)
        # 计算后缀表达式
        j = 0
        while len(data) != 1:
            try:
                fl = int(data[j])
                j += 1
            except:
                t1 = data.pop(j)
                t2 = data.pop(j-1)
                data[j-2] = str(cal(data[j-2],t2,t1))
                j = j - 1
        print(data[0])

    except:
        break

