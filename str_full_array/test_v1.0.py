#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description： 输入"看了又看"，
输出全排列['看了又看', '看了看又', '看又了看', '看又看了', '看看了又', '看看又了', '了看又看', '了看看又',
         '了又看看', '了又看看', '了看看又', '了看又看', '又看了看', '又看看了', '又了看看', '又了看看',
         '又看看了', '又看了看', '看看了又', '看看又了', '看了看又', '看了又看', '看又看了', '看又了看']
不考虑去重
"""


def dfs(u):
    # 所有位置都填充值以后，进行输出
    if length == u:
        string_t = ''
        for i in range(0, length):
            string_t = string_t + changes[i]
        outputs.append(string_t)
    # i表示填入的值，u表示第几个位置
    for i in range(0, length):
        if status[i] == 0:
            status[i] = 1
            changes[u] = inputs[i]
            dfs(u+1)
            # 恢复现场
            status[i] = 0


inputs = '看了又看'
length = len(inputs)
changes = []
status = []
outputs = []
for i in range(0, length):
    status.append(0)
    changes.append(0)
dfs(0)
print(len(outputs), outputs)