# -*- coding: utf-8 -*-
"""中文别名冒烟测试: 打印 ~ print, 如果 ~ if"""
打印("你好，中文Python!")

如果 True:
    打印("如果 True 分支 OK")
else:
    打印("不应该到这里")

x = 5
如果 x == 1:
    打印("一")
elif x == 5:
    打印("五-OK")
else:
    打印("其他")

# 打印参数透传
打印("a", "b", sep="-", end="!\n")

# 三元表达式也可用 如果 (与 if 同 token)
y = 10 如果 True else 20
assert y == 10, y
打印("全部通过!")
