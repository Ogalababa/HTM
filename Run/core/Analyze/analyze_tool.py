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

def check_input_end_state(dataframe) -> bool:
    """
    check if end state is same as request
    :param dataframe: pd.DataFrame
    :return: bool
    """

    total_wagen = set(dataframe['<aanmelden> wagen'].to_list())
