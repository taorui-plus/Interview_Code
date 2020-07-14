#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description:
    1.读取大文件表，生成hash key&value 存入1024个小文件（采用桶排序/计数排序，注意value不是字符串内容而是记录所在大文件中的行数）
        1.1 key为hash值（采用md5<散列化>）
        1.2 value为所在大文件中的行数
    2.根据顺序依次从大到小读出topN
    3.获取topN在文件中的行数并读取大文件表获取内容
    4.循环输出topN

优化点：
    1.md5码，16个字节,128位,2**128=10**40，100亿条数据，32位就够用，最小完美哈希
    2.加缓存，避免重复读入数据
"""
import hashlib
import os
import time
RM_DUP_DICT = dict()  # 哈希去重
FS = []  # 文件句柄
BUCKET_NUM = 1024


def check_dir(slice_files_dir):
    is_exists = os.path.exists(slice_files_dir)
    if not is_exists:
        os.mkdir(slice_files_dir)


def open_files_for_write(input_dir):
    global FS
    for i in range(1, BUCKET_NUM+1):
        FS.append(open(input_dir + "/" + str(i) + ".txt", mode="w+", encoding="utf-8"))


def open_files_for_read(input_dir):
    global FS
    FS = []
    for i in range(1, BUCKET_NUM+1):
        FS.append(open(input_dir + "/" + str(i) +
                       ".txt", mode="rb"))


def close_files():
    global FS
    for f in FS:
        f.close()
    FS = []


def get_file_md5(my_string) -> str:
    m = hashlib.md5()
    m.update(my_string)
    return m.hexdigest()


def file_split_buckets(file_path):
    # 创建1024个桶
    open_files_for_write("bucket_files")
    global RM_DUP_DICT, FS
    num = 0
    max_v = 0
    with open(file_path, 'rb') as f:
        for line in f:
            num += 1
            length = len(line)  # 文本长度
            if length == 0:
                continue
            max_v = max(max_v, length)
            md5_value = get_file_md5(line)  # 文本哈希
            # 哈希去重
            if md5_value not in RM_DUP_DICT:
                RM_DUP_DICT[md5_value] = num
                FS[length-1].write(str(num) + os.linesep)  # 记录行数
    close_files()


def get_top_n(file_path, num) -> list:
    num_ret = []  # 满足条件的行号列表
    open_files_for_read("bucket_files")
    global FS
    print("fs length:", len(FS))
    for i in range(1024, 0, -1):
        if num <= 0:
            break
        line = FS[i-1].readline()
        while line:
            num_ret.append(int(line))
            line = FS[i-1].readline()
            num -= 1
            if num <= 0:
                break
    close_files()
    num_ret.sort()
    line_num = 1
    ret_str = []
    # 通过行号去原始文件取文本
    with open(file_path, 'rb') as f:
        for line in f:
            if len(num_ret) > 0:
                if line_num == num_ret[0]:
                    ret_str.append(line)
                    del num_ret[0]
            else:
                break
            line_num += 1
    return ret_str


def main(input_file, top_n, bucket_files_dir):
    """主流程
    Args:
        input_file: 输入文件
        top_n: 将要输出的文本个数
        bucket_files_dir: 分桶文件地址
    """
    # 创建桶目录
    check_dir(bucket_files_dir)
    # 对文件内容去重，并根据文本长度插入不同的桶
    file_split_buckets(input_file)
    # 获取最长的top n的文本
    result = get_top_n(input_file, top_n)
    # print("top_n_text:", result)


if __name__ == "__main__":
    input_file = "test_data.txt"  # 输入文件
    bucket_files_dir = "bucket_files"  # 分桶地址
    top_n = 1000
    start = time.time()
    main(input_file, top_n, bucket_files_dir)
    end = time.time()
    print("耗时(s)：", end-start)
