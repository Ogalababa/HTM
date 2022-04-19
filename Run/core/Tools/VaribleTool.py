# ！/usr/bin/python3
# coding:utf-8
# sys


def wagen_length(wagen_nr: int) -> int:
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



