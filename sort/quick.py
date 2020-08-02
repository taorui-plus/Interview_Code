#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description：符合python风格的快排代码
"""


def quick_sort(arr):
    """快速排序"""
    if len(arr) < 2:
        return arr
    # 选取基准，随便选哪个都可以，选中间的便于理解
    mid = arr[len(arr) // 2]
    # 定义基准值左右两个数列
    left, right = [], []
    # 从原始数组中移除基准值
    arr.remove(mid)
    for item in arr:
        # 大于基准值放右边
        if item >= mid:
            right.append(item)
        else:
            # 小于基准值放左边
            left.append(item)
    # 使用迭代进行比较
    return quick_sort(left) + [mid] + quick_sort(right)


if __name__ == '__main__':
    arr = [1, 4, 3, 2]
    print(quick_sort(arr))

