#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description：lambda 格式的快排，一行代码实现
"""


quick_sort = lambda array: array if len(array) <= 1 \
    else quick_sort([item for item in array[1:] if item <= array[0]]) \
         + [array[0]] \
         + quick_sort([item for item in array[1:] if item > array[0]])


if __name__ == '__main__':
    arr = [1, 4, 3, 2]
    print(quick_sort(arr))

