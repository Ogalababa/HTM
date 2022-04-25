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


def wissel_garde(wissel_nr: str) -> str:
    """
    define direction of input garde
    :param wissel_nr: str
    :return: Links/Recht
    """
    rechts_wissel = [
        'W001', 'W003', 'W013', 'W014', 'W018', 'W022', 'W027', 'W028', 'W031', 'W038', 'W046', 'W056', 'W057',
        'W067', 'W081', 'W084', 'W094', 'W104', 'W113', 'W118', 'W121', 'W127', 'W133', 'W135', 'W151', 'W153',
        'W156', 'W161', 'W164', 'W166', 'W169', 'W171', 'W180', 'W184', 'W189', 'W194', 'W200', 'W202', 'W223',
        'W228', 'W232', 'W235', 'W257', 'W268', 'W271', 'W275', 'W291', 'W287', 'W307', 'W383', 'W385', 'W391',
        'W399', 'W425', 'W500', 'W520', 'W523', 'W542', 'W550', 'W560', 'W564', 'W573', 'W583', 'W584', 'W601',
        'W607', 'W619', 'W628', 'W632', 'W636', 'W640', 'W644', 'W646', 'W649', 'W656', 'W657', 'W658', 'W660',
        'W662', 'W665', 'W668', 'W689'
    ]
    if wissel_nr in rechts_wissel:
        return 'rechts'
    else:
        return 'links'
