from .. import db
from ..model.movie import Movie

import jieba
import numpy as np
from collections import *
import difflib
import csv
import heapq


# 其中的str1，str2是分词后的标签列表
def cos_sim(str1, str2):
    # 基于词频的余弦相似度（TF-IDF）
    '''
假设a是str1的标签特征向量，b是str2的标签特征向量，那么两者的相似度可以用cosθ表示，且0<=cosθ<=1。
而关于str1，str2的标签特征向量的获取，我们这里用了TF-IDF中的思想，利用词频来表示。
例如str1=[“我”,”爱”,”漫威”]，str2=[“我”,”喜欢”,”漫威”,”电影”]
则所有词语的集合为[“我”,”爱”,”喜欢”,”漫威”,”电影”]
str1（计算相应词频）转变后的a=[1,1,0,1,0]
str2（计算相应词频）转变后的b=[1,0,1,1,1]
计算后的相似度为：0.577350
求余弦定理
    '''
    co_str1 = (Counter(str1))
    co_str2 = (Counter(str2))
    p_str1 = []
    p_str2 = []
    for temp in set(str1 + str2):
        p_str1.append(co_str1[temp])
        p_str2.append(co_str2[temp])
    p_str1 = np.array(p_str1)
    p_str2 = np.array(p_str2)
    return p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))


def diff(str1, str2):
    diff_result = difflib.SequenceMatcher(None, str1, str2).ratio()
    return diff_result


def minEditDist(str1, str2):
    '''
假设我们可以使用d[ i , j ]个步骤（可以使用一个二维数组保存这个值），表示将串s[ 1…i ] 转换为 串t [ 1…j ]所需要的最少步骤个数，那么，在最基本的情况下，即在i等于0时，也就是说串s为空，那么对应的d[0,j] 就是 增加j个字符，使得s转化为t，在j等于0时，也就是说串t为空，那么对应的d[i,0] 就是 减少 i个字符，使得s转化为t。

然后我们考虑一般情况，加一点动态规划的想法，我们要想得到将s[1..i]经过最少次数的增加，删除，或者替换操作就转变为t[1..j]，那么我们就必须在之前可以以最少次数的增加，删除，或者替换操作，使得现在串s和串t只需要再做一次操作或者不做就可以完成s[1..i]到t[1..j]的转换。所谓的“之前”分为下面三种情况：

我们可以在k个操作内将 s[1…i] 转换为 t[1…j-1]
我们可以在k个操作里面将s[1..i-1]转换为t[1..j]
我们可以在k个步骤里面将 s[1…i-1] 转换为 t [1…j-1]
针对第1种情况，我们只需要在最后将 t[j] 加上s[1..i]就完成了匹配，这样总共就需要k+1个操作。

针对第2种情况，我们只需要在最后将s[i]移除，然后再做这k个操作，所以总共需要k+1个操作。

针对第3种情况，我们只需要在最后将s[i]替换为 t[j]，使得满足s[1..i] == t[1..j]，这样总共也需要k+1个操作。而如果在第3种情况下，s[i]刚好等于t[j]，那我们就可以仅仅使用k个操作就完成这个过程。

最后，为了保证得到的操作次数总是最少的，我们可以从上面三种情况中选择消耗最少的一种最为将s[1..i]转换为t[1..j]所需要的最小操作次数。
    '''
    len_str1 = len(str1)
    len_str2 = len(str2)
    taglist = np.zeros((len_str1 + 1, len_str2 + 1))
    for a in range(len_str1):
        taglist[a][0] = a
    for a in range(len_str2):
        taglist[0][a] = a
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            if (str1[i - 1] == str2[j - 1]):
                temp = 0
            else:
                temp = 1
            taglist[i][j] = min(taglist[i - 1][j - 1] + temp, taglist[i][j - 1] + 1, taglist[i - 1][j] + 1)
    return 1 - taglist[len_str1][len_str2] / max(len_str1, len_str2)


# def super(num,list):
#     # 列表最大值返回该数值对应的index
#     for i in range(len(list)):
#         if num==list[i]:
#             return i

def prior(list):
    # 求出列表最大4个索引值
    # result = map(list.index, heapq.nlargest(3, list))
    temp = []
    Inf = 0
    for i in range(4):
        temp.append(list.index(max(list)))
        list[list.index(max(list))] = Inf
    # result.sort()
    temp.sort()
    return temp


def last(list1, list2):  # list1为索引值列表  #List2为需要匹配列表
    temp_ = []
    for i in list1:
        temp_.append(list2[i])
    return temp_


def main(str1, str2):
    end_result = []
    result = list(map(lambda var: jieba.lcut(var[0]), str1))  # 对str1做了结巴分词处理
    # result0=str(jieba.lcut(str2))

    result1 = list(map(lambda var: cos_sim(var[0], str2), result))
    # print(result1)
    result2 = list(map(lambda var: minEditDist(var[0], str2), result))
    # print(result2)
    result3 = list(map(lambda var: diff(var[0], str2), str1))  # 不需要结巴分词处理
    # print(result3)

    for i in range(len(result1)):
        end_result.append(result1[i] * 0.3 + result2[i] * 0.4 + result3[i] * 0.3)
    back_result = list(map(lambda x: x[0], str1))

    return last(prior(end_result), back_result)  # 最优解索引值


def get_prior_user(search_pattern: str):
    movie_list = Movie.query.all()
    a = list(map(lambda x: [x.name], movie_list))
    return main(a, search_pattern)
