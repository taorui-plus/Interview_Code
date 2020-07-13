#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description: 外部排序实现计算日记点赞表的P90值
    1.读取大文件表，维护一个数据总量nTotal
    2.分为n个小文件（第一次内部排序<采用优化后的快排>；注意：内存量 大于等于 小文件的数据量大小）
    3.采用外部排序排序每个小文件
    4.合并所有小文件并输出到一个新的文件（依次读取每个文件从第一行到末尾，比较获取极（大/小）值，存入新文件）
    5.最终获得一个排序好的大文件
    6.通过排序后的大文件获取p90的位置 通过文件指针偏移读取具体的p90数据
    注：小文件倒序排列，点击数多的排在前面
"""
import pandas as pd
from tqdm import tqdm
import os
import math


def slice_data(input_file, sliced_files_dir, chunk_size, sliced_num):
    """Large file split
    Args:
        input_file: 输入文件
        sliced_files_dir: 切片后数据目录
        chunk_size: 切割后每个小文件的大小, int
        sliced_num: 切片数量, int
    """
    reader = pd.read_csv(input_file, iterator=True)
    i = 0
    with tqdm(range(sliced_num+1), 'Reading ...') as t:
        for _ in t:
            try:
                chunk = reader.get_chunk(chunk_size)
                i += 1
                chunk.to_csv(sliced_files_dir+'/slice_' + str(i) +
                             '.csv', index=False, header=None)
            except StopIteration:
                break


def slice_sort(slices, slice_files_dir):
    """Sort split file
    Args:
        slices: 切片大小, int
        slice_files_dir: 原始切片
    """
    for i in range(1, slices):
        try:
            lc = pd.read_csv(slice_files_dir + '/slice_' +
                             str(i) + '.csv', sep=',', header=None)
            print('slice_' + str(i))
        except Exception:
            raise Exception('file is not found!')
        # 按1列的倒序排序，去重，写入
        lc = lc.sort_values(by=[1], ascending=[False])
        lc = lc.drop_duplicates()
        lc.to_csv(slice_files_dir+'/slice_' + str(i) +
                  '.csv', index=False, header=None, sep=',')


def merge_files(input_files, outputs_file):
    """File merge
    Args:
        input_files: 输入文件
        outputs_file: 合并后文件
    """
    files = os.listdir(input_files)
    fs = []  # 文件句柄
    for f in files:
        fs.append(open(input_files + "/" + f))
    lines = []
    keys = []

    for f in fs:
        line = f.readline()  # 第一行
        lines.append(line)
        keys.append(get_key(line))  # 每一行的第二列
    # print("key:", keys[0:10])
    buff = []
    buff_size = 20
    append = buff.append
    output = open(outputs_file, 'w')
    try:
        key = max(keys)
        index = keys.index(key)  # 列表的索引
        while 1:
            while key == max(keys):
                append(lines[index])  # 最大值放到缓冲区
                if len(buff) > buff_size:
                    output.write(''.join(buff))
                    del buff[:]

                line = fs[index].readline()
                if not line:       # 读完全部行，跳出
                    fs[index].close()
                    del fs[index]
                    del keys[index]
                    del lines[index]
                    break
                key = get_key(line)
                keys[index] = key
                lines[index] = line

            if len(fs) == 0:  # 读完全部文件，跳出
                break
            key = max(keys)
            index = keys.index(key)

        if len(buff) > 0:    # 写入缓冲区最后一个元素
            output.write(''.join(buff))
    finally:
        output.close()


def get_p_n(the_file_path, point, total):
    """计算P_N值
    Args:
        the_file_path: 输入文件
        point: 排序后文件
        total: 切片大小, int
    Return：
        p_n，float
    """
    down_value = math.floor(total*(100-point)/100)
    up_value = math.ceil(total*(100-point)/100)
    down = 0
    up = 0
    for cur_line_number, line in enumerate(open(the_file_path, 'rU')):
        if cur_line_number == down_value:
            down = int(line.split(",")[1])
            if down_value == up_value:
                up = int(line.split(",")[1])
                break
        elif cur_line_number == up_value:
            up = int(line.split(",")[1])
            break
    return (down+up)/2


def get_line_nums(the_file_path):
    count = 0
    for index, line in enumerate(open(the_file_path, 'r')):
        count += 1
    return count


def get_key(line):
    line = line.split(",")
    return int(line[1])


def check_dir(slice_files_dir):
    is_exists = os.path.exists(slice_files_dir)
    if not is_exists:
        os.mkdir(slice_files_dir)


def main(input_file, output_file, chunk_size, sliced_num):
    """主流程
    Args:
        input_file: 输入文件
        output_file: 排序后文件
        chunk_size: 切片大小
        sliced_num: 切片数, int
    """
    # 切片
    slice_files_dir = "sliced_files"
    check_dir(slice_files_dir)
    slice_data(input_file, slice_files_dir, chunk_size, sliced_num=20)
    # 切片排序
    slice_sort(sliced_num, slice_files_dir)
    # 文件合并
    merge_files(slice_files_dir, output_file)
    # 计算P90
    p90 = get_p_n(sorted_file, 90, get_line_nums(sorted_file))
    print("\n")
    print("P90:", p90)


if __name__ == '__main__':
    input_file = "diary_likes_test_data.csv"  # 输入文件
    # 注：sliced_num*chunk_size>=文件总行数
    sliced_num = 20   # 切片个数
    chunk_size = 500  # 切片大小
    sorted_file = 'diary_likes_sorted.csv'  # 排序后文件
    main(input_file, sorted_file, chunk_size, sliced_num)
