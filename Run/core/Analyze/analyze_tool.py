# ！/usr/bin/python3
# coding:utf-8
# sys

def match_list(small_list: list, big_list: list) -> bool:
    """
    Match two list, return bool if small list in big list
    :param small_list: list
    :param big_list: list
    :return: bool
    """
    compare_result = []
    for i in range(len(big_list)):
        compare_result.append(small_list == big_list[i:i + len(small_list)])
    return any(compare_result)


def check_bad_contact(dataframe, col_name: str) -> bool:
    """
    check hfp data is correct
    :param dataframe: pd.DataFrame
    :param col_name: str
    :return: bool
    """
    return any([match_list([1, 0, 1], dataframe[col_name].to_list()),
                match_list([1, 0, 0, 1], dataframe[col_name].to_list())])


def check_fout_state(dataframe, col_name: str) -> bool:
    """
    check if error state in dataset
    :param dataframe: pd.DataFrame
    :param col_name: str
    :return: bool
    """
    return 1 in dataframe[col_name].to_list()


def check_werk_wagen(dataframe) -> bool:
    """
    check if storing from werk wagen
    :param dataframe: pd.DataFrame
    :return: bool
    """
    aanmelden_list = list(set(dataframe['<aanmelden> wagen'].tolist()))
    afmelden_list = list(set(dataframe['<afmelden> wagen'].tolist()))
    aktuell_list = list(set(dataframe['<aktuell> wagen'].tolist()))
    werk_wagen = None
    werk_wagen = [i for i in aanmelden_list if i < 3000]
    if len(werk_wagen) > 0 and werk_wagen[0] in aanmelden_list:
        return werk_wagen[0] not in afmelden_list
    else:
        return False
