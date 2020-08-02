#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description： 输入"看了又看"，
输出全排列['看了又看', '看了看又', '看又了看', '看又看了', '看看又了', '看看了又', '了看又看',
         '了看看又', '了又看看', '又了看看', '又看了看', '又看看了']
递归过程中不去重，最后去重
"""


def list_deduplication(orig_l):
    new_l = []
    for i in orig_l:
        if i not in new_l:
            new_l.append(i)
    return new_l


def str_sort(s=''):
    if len(s) <= 1:
        return [s]
    arr_list = []
    for i in range(len(s)):
        for j in str_sort(s[0:i] + s[i + 1:]):
            arr_list.append(s[i] + j)
    return list_deduplication(arr_list)


if __name__ == '__main__':
    str_list = str_sort('孙行者')
    print(len(str_list), str_list)


