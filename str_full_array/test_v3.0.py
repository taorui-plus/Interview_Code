#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description： 输入"看了又看"，
输出全排列['看了又看', '看了看又', '看又了看', '看又看了', '看看又了', '看看了又', '了看又看',
         '了看看又', '了又看看', '又了看看', '又看了看', '又看看了']
递归过程中去重
"""


def exchange(i, j, string):
    """交换字符串中指定位置的字符"""
    temp = string[j]
    trailer = string[j + 1:] if j + 1 < len(string) else ''
    string = string[0:j] + string[i] + trailer
    string = string[0:i] + temp + string[i + 1:]
    return string


def arrangement(string, beg, end):
    if beg == end - 1:
        str_list.append(string)
        return
    for i in range(beg, end):
        if string[i] in string[beg:i]:
            continue
        string = exchange(i, beg, string)
        arrangement(string, beg+1, end)
        string = exchange(i, beg, string)


if __name__ == '__main__':
    a = '看了又看'
    str_list = []
    arrangement(a, 0, len(a))
    print(len(str_list), str_list)