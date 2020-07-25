#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Author: TaoRui
Date: 2020/07/10 14:36:33
Description: 计算给定语料的tf-idf
    1.分词
    2.分别统计生成各个文档的词频字典
    3.根据公式计算tf-idf值
"""
from collections import Counter
import jieba
import numpy as np
jieba.load_userdict('userdict.txt')  # 补充词库


# 创建停用词list
def stopwords_list(file_path):
    stopwords = [line.strip() for line in open(file_path, 'r').readlines()]
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    sentence_seg = jieba.cut(sentence.strip())
    stopwords = stopwords_list('stop_word.txt')  # 加载停用词库
    out_str = ''
    for word in sentence_seg:
        if word not in stopwords:
            if word != '\t':
                out_str += word
                out_str += " "
    return out_str


def tf(word, count):
    return count[word] / sum(count.values())


def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


def idf(word, count_list):
    return np.log(len(count_list) / (1 + n_containing(word, count_list)))


def tf_idf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


if __name__ == '__main__':
    inputs = open('input.txt', 'r')  # 加载要处理的文件的路径
    count_list = []  # 分别统计每个文档的词频字典
    for line in inputs:
        # 1.WordCut
        word_cut = []
        line_seg = seg_sentence(line)
        # 2.WordCount
        count = dict(Counter(line_seg.split(" ")))
        count_list.append(count)
    inputs.close()
    # 计算TF-IDF
    for i, count in enumerate(count_list):
        print("Top words in document {}".format(i + 1))
        scores = {word: tf_idf(word, count, count_list) for word in count}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))