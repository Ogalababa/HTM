# ！/usr/bin/python3
# coding:utf-8
# sys


def wagen_length(wagen_nr):
    """
    default wagen lent
    :param wagen_nr: int
    :return: int
    """
    if 3000 <= wagen_nr < 4000:
        length = 30
    elif 4000 <= wagen_nr < 5000:
        length = 37
    elif 5000 <= wagen_nr < 6000:
        length = 35
    else:
        length = 0
    return length


def match_list(small_list, big_list):
    compare_result = []
    for i in range(len(big_list)):
        compare_result.append(small_list == big_list[i:i+len(small_list)])
    return any(compare_result)
