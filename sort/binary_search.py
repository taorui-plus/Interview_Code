#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/08/01 14:36:33
Description：返回有序数组中指定元素的索引，二分查找
"""


def binary_search(arr, left, right, x):
    # 基本判断
    if right >= left:
        mid = int(left + (right - left) / 2)
        # 元素整好的中间位置
        if arr[mid] == x:
            return mid
        # 元素小于中间位置的元素，只需要再比较左边的元素
        elif arr[mid] > x:
            return binary_search(arr, left, mid - 1, x)
        # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            return binary_search(arr, mid + 1, right, x)
    else:
        # 不存在
        return -1


if __name__ == '__main__':
    arr = [2, 3, 4, 10, 40]  # 测试数组
    x = 10
    result = binary_search(arr, 0, len(arr) - 1, x)