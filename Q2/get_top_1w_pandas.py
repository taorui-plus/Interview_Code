#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description: pandas可以处理<=5TB的文件，直接使用pandas来处理超大文件
    1.读入文件为DataFrame：reader
    2.去重
    3.新增文本长度列和索引列
    4.按文本长度列分组（1024个分组）并返回每个分组的元素个数，产生新的DataFrame：group
    5.通过group表返回top_n文本的最小长度
    6.在reader大表中按条件查找行，产生DataFrame:result
    7.通过result表返回符合条件的top_n文本
"""
import pandas as pd
import time

def get_top_n_len(group, top_n):
    """获取top_n文本的最小长度
    Args:
        group: 分组后的DataFrame
        top_n: 返回的文本个数，int
    Return：
        top_n_len：top_n文本的最小长度
    """
    group_len = len(group)
    top_n_len = group_len
    total_size = 0
    for i in reversed(range(0, group_len)):
        size = group.loc[i]["size"]
        total_size = total_size + size
        if total_size >= top_n:
            break
        top_n_len = top_n_len-1
    return top_n_len


def main(input_file, top_n):
    """主流程
    Args:
        input_file: 输入文件路径
        top_n: 返回的文本个数，int
    """
    # 1.读入文件为DataFrame，产生reader表
    reader = pd.read_csv(input_file)
    reader.columns = ["text"]

    # 2.文本去重
    reader.drop_duplicates(subset=['text'], keep='first', inplace=True)
    row_num = len(reader)

    # 3.1新增文本长度列
    reader["len"] = reader.apply(lambda row: len(str(row[0])), axis=1)
    # 3.2新增文本索引列
    reader["index"] = [i for i in range(0, row_num)]

    # 4.按"len"列分组统计数据个数，产生group表
    group = reader.groupby(['len']).size().reset_index(name='size')

    # 5.找出top-n文本的最小长度
    top_n_len = get_top_n_len(group, top_n)
    print("top_"+str(top_n)+"的最小文本长度：", top_n_len)

    # 6.在reader大表中按条件查找行，产生result表
    result = reader.loc[(reader['len'] >= top_n_len)]

    # 7.返回符合条件的文本
    top_n_text = list(result['text'])
    print("top_"+str(top_n)+"_text:", top_n_text)


if __name__ == '__main__':
    input_file = "test_data.txt"  # 输入文件
    top_n = 1000
    start = time.time()
    main(input_file, top_n)
    end = time.time()
    print("耗时(s)：", end-start)