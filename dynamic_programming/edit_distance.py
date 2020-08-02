#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description：求两个字符串的编辑距离
"""


def edit_distance(str1, str2):
    cell = [[i+j for j in range(len(str2)+1)] for i in range(len(str1)+1)]
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j-1]:
                d = 0
            else:
                d = 1
            cell[i][j] = min(cell[i-1][j]+1, cell[i][j-1]+1, cell[i-1][j-1]+d)
    return cell[len(str1)][len(str2)]


# 测试
str1 = "float"
str2 = "flot"
print(edit_distance(str1, str2))