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


def wissel_gerade_state(wissel_nr: str) -> str:
    """
    get wissel state for <input> naar gerade
    :param wissel_nr: str
    :return: str
    """
    LINKS = 'links'
    RECHTS = 'rechts'
    gerade_state = {
        'W001': RECHTS, 'W002': LINKS, 'W003': RECHTS, 'W004': RECHTS, 'W005': LINKS, 'W006': LINKS, 'W012': LINKS,
        'W013': RECHTS, 'W014': RECHTS, 'W015': RECHTS, 'W016': LINKS, 'W017': RECHTS, 'W018': RECHTS, 'W019': RECHTS,
        'W020': LINKS, 'W021': RECHTS, 'W022': RECHTS,  'W023': LINKS, 'W024': LINKS, 'W025': RECHTS, 'W026': RECHTS,
        'W027': RECHTS, 'W028': RECHTS, 'W029': RECHTS, 'W030': LINKS, 'W031': RECHTS, 'W032': LINKS, 'W033': LINKS,
        'W034': LINKS, 'W035': LINKS,
    }
    return gerade_state.get(wissel_nr)