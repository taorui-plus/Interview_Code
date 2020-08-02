#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description：求两个字符串的最长公共子串
"""


def max_sub_str(str1, str2):
    cell = [[0 for j in range(len(str2)+1)] for i in range(len(str1)+1)]
    max_len = 0  # 最大匹配长度
    last_1p = 0  # 当前最大匹配字串在str1中的最后一位
    for i in range(len(str1)):
        for j in range(len(str2)):
            if str1[i] == str2[j]:
                cell[i+1][j+1] = cell[i][j]+1
                if cell[i+1][j+1] > max_len:
                    max_len = cell[i+1][j+1]
                    last_1p = i + 1
    return str1[last_1p - max_len:last_1p]


# 测试
str1 = "float"
str2 = "flot"
print(max_sub_str(str1, str2))