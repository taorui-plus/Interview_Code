#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description： 生成测试文件
"""
import secrets
import string
import random


def gen_q2_data(file_name, line_num):
    """生成N条文本长度在1-1024之间随机长度的文件
    Args:
        file_name: 输出文件路径
        line_num: 行数
    """
    text_max_len = 100  # 1024
    with open(file_name, 'w') as file_object:
        for i in range(0, line_num):
            text = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(random.randint(1, text_max_len)))
            file_object.write(text)
            file_object.write('\n')
            print("第"+str(i)+"行写入...")
        print("Finish!")


if __name__ == '__main__':
    file_name = 'Q2/test_data.txt'
    line_num = 1000000  # 文本行数
    gen_q2_data(file_name, line_num)








