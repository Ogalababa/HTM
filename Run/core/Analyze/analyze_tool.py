# ！/usr/bin/python3
# coding:utf-8
# sys
from typing import Tuple

from Run.core.Tools.VaribleTool import wissel_gerade


def match_list(small_list: list, big_list: list) -> bool:
    """
    Match two list, return bool if small list in big list
    :param small_list: list
    :param big_list: list
    :return: bool
    """
    # Check if the byte is wrong
    # 检测字节是否错误
    compare_result = []
    for i in range(len(big_list)):
        compare_result.append(small_list == big_list[i:i + len(small_list)])
    return any(compare_result)


def check_bad_contact(dataframe, col_name: str, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check hfp data is correct
    :param dataframe: pd.DataFrame
    :param col_name: str
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Check hfk, hfp data correctness
    # 检测hfk， hfp数据正确性
    aanmelden_list = dataframe['<aanmelden> wagen'].tolist()
    return storing, afdelling, any([match_list([1, 0, 1], dataframe[col_name].to_list()),
                                    match_list([1, 0, 0, 1], dataframe[col_name].to_list()),
                                    len(dataframe[dataframe[col_name] == 1]) / len(dataframe) > 0.7])


def check_fout_state(dataframe, col_name: str, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    """
    check if error state in dataset
    :param dataframe: pd.DataFrame
    :param col_name: str
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Check state correctness
    # 检测状态正确性
    lijn_nr = None
    service = None
    categroie = None
    wagen_nr = None
    if 1 in dataframe[col_name].to_list():
        lijn_nr = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> lijn']
        service = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> service']
        categroie = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> categorie']
        wagen_nr = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> wagen']
    return storing, afdelling, lijn_nr, service, categroie, wagen_nr, 1 in dataframe[col_name].to_list()


def check_werk_wagen(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check if storing from werk wagen
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Detect work cart logout error
    # 检测工作车登出错误
    aanmelden_list = list(set(dataframe['<aanmelden> wagen'].tolist()))
    afmelden_list = list(set(dataframe['<afmelden> wagen'].tolist()))
    aktuell_list = list(set(dataframe['<aktuell> wagen'].tolist()))
    werk_wagen = None
    werk_wagen = [i for i in aanmelden_list if i < 3000]
    if len(werk_wagen) > 0 and werk_wagen[0] in aanmelden_list:
        return storing, afdelling, werk_wagen[0] not in afmelden_list
    else:
        return storing, afdelling, False


def check_verkeerd_code(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    """
    check if the trame with wrong code
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Check the consistency between the planned direction and the travel direction
    # 检测计划方向与行进方向一致性
    wissel_nr = dataframe['wissel nr'].tolist()[0]
    gerade = wissel_gerade(wissel_nr)
    wissel_ijzer_index = dataframe[dataframe['<wissel> ijzer'] == 0].index.to_list()
    verkeerd_code = []
    lijn_nr = -1
    service = -1
    categroie = -1
    wagen_nr = -1
    if len(wissel_ijzer_index) == 0:
        return storing, afdelling, lijn_nr, service, categroie, wagen_nr, False
    else:
        try:
            lijn_nr = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> lijn']
            service = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> service']
            categroie = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> categorie']
            wagen_nr = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> wagen']
            for i in wissel_ijzer_index:
                sub_cycle = dataframe[dataframe['<aanmelden> wagen'] == dataframe.loc[i]['<aanmelden> wagen']]
                request_direction = None
                if 1 in sub_cycle['<input> naar gerade'].tolist() and request_direction is None:
                    request_direction = gerade
                elif 1 in sub_cycle['<input> naar links'].tolist() and request_direction is None:
                    request_direction = '<wissel> links'
                elif 1 in sub_cycle['<input> naar rechts'].tolist() and request_direction is None:
                    request_direction = '<wissel> rechts'
                sub_wissel_ijzer_index = sub_cycle[sub_cycle['<wissel> ijzer'] == 0].index.to_list()[0]
                wissel_state = sub_cycle.loc[sub_wissel_ijzer_index - 1][request_direction]
                if wissel_state == 1 and wissel_state != sub_cycle.iloc[-1][request_direction]:
                    verkeerd_code.append(True)
                else:
                    verkeerd_code.append(False)
            return storing, afdelling, lijn_nr, service, categroie, wagen_nr, any(verkeerd_code)
        except KeyError:
            return storing, afdelling, lijn_nr, service, categroie, wagen_nr, False


def miss_out_meld(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    """
    check if vecom afmelden error
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[str, str, int, int, int, int, bool]
    """
    # Check for logout errors
    # 检测登出错误
    state_list = []
    wagen_nr_set = set(dataframe['<aanmelden> wagen'].tolist())
    lijn_nr = None
    service = None
    categroie = None
    wagen_nr = None
    for i in wagen_nr_set:
        sub_cycle_dataframe = dataframe[(dataframe['<aanmelden> wagen'] == i) &
                                        (dataframe["<hfp> schakelcriterium bezet"] == 1) &
                                        (dataframe["<hfk> schakelcriterium bezet"] == 0)]
        if len(sub_cycle_dataframe) > 0:
            lijn_nr = sub_cycle_dataframe.iloc[0]['<aanmelden> lijn']
            service = sub_cycle_dataframe.iloc[0]['<aanmelden> service']
            categroie = sub_cycle_dataframe.iloc[0]['<aanmelden> categorie']
            wagen_nr = sub_cycle_dataframe.iloc[0]['<aanmelden> wagen']
            if any([1 not in sub_cycle_dataframe['<vecom> aftellen'].tolist(),
                    0 not in sub_cycle_dataframe['<vecom> aftellen'].tolist()]):
                return storing, afdelling, lijn_nr, service, categroie, wagen_nr, True
        else:
            continue
    return storing, afdelling, lijn_nr, service, categroie, wagen_nr, False


def check_wagen_vecom(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check the condition of the vecom in tram
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Detect vehicle VECOM errors
    # 检测车载VECOM错误
    aanmelden_list = dataframe['<aanmelden> wagen'].tolist()
    fifo_wagen = None
    handel_list = []
    for i in aanmelden_list:
        if i != fifo_wagen:
            handel_list.append(i)
            fifo_wagen = i
    return storing, afdelling, len(handel_list) != len(set(handel_list))


def wissel_buiten_dinst(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check if the wissel out of order
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
    """
    # Check if wissel is out of order
    # 检测wissel是否关闭
    return storing, afdelling, all([max(dataframe['<wissel> links']) == 0, max(dataframe['<wissel> rechts']) == 0])


def wissel_eind_stand(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check if the wissel do not have end state
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[str, str, bool]
    """
    # Check if wissel is fully closed
    # 检测wissel是否完全闭合
    eind_stand = dataframe[(dataframe['<wissel> links'] == 0) & (dataframe['<wissel> rechts'] == 0)]

    return storing, afdelling, 0.3 < len(eind_stand) / len(dataframe) < 1


def hfp_start_index(hfp_list: list) -> list:
    # Detect hfp data start sequence
    # 检测hfp数据开始序列
    hfp_start_list = []
    for i in range(len(hfp_list)):
        if [0, 1, 1] == hfp_list[i: i + 3]:
            hfp_start_list.append(i)
    return hfp_start_list


def wacht_op_sein(dataframe, storing:str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    # Check if the driver is driving in sequence
    # 检测司机是否按序行驶
    lijn_nr = None
    service = None
    categroie = None
    wagen_nr = None
    state_list = []
    for i in hfp_start_index(dataframe['<hfp> schakelcriterium bezet'].tolist()):
        if i <= 3:
            hfp_error = all([all(dataframe.iloc[:i+1]['<wls> seinbeld links geactiveerd'] == 0),
                             all(dataframe.iloc[:i+1]['<wls> seinbeld rechts geactiveerd'] == 0)])
            state_list.append(hfp_error)
        else:
            hfp_error = all([all(dataframe.iloc[i-3:i + 1]['<wls> seinbeld links geactiveerd'] == 0),
                             all(dataframe.iloc[i-3:i + 1]['<wls> seinbeld rechts geactiveerd'] == 0)])
            state_list.append(hfp_error)
        if hfp_error:
            wagen_nr = dataframe.iloc[i]['<aanmelden> wagen']
            service = dataframe.iloc[i]['<aanmelden> service']
            categroie = dataframe.iloc[i]['<aanmelden> categorie']
            lijn_nr = dataframe.iloc[i]['<aanmelden> lijn']
    return storing, afdelling, lijn_nr, service, categroie, wagen_nr, any(state_list),


def no_wagen_nr(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    # Check if the vehicle has vecom installed
    # 检测车辆是是否安装vecom
    lijn_nr = None
    service = None
    categroie = None
    wagen_nr = 0
    if 0 in dataframe['<aanmelden> wagen'].tolist():
        lijn_nr = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> lijn']
        service = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> service']
        categroie = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> categorie']
        
    return storing, afdelling, lijn_nr, service, categroie, wagen_nr, 0 in dataframe['<aanmelden> wagen'].tolist()


def miss_data(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    # 放到检测列表末端
    """
    check if the dataset complete
    :param dataframe: pd.DAtaFrame
    :param storing: str
    :param afdelling: str
    :return: Tuple[str, str, bool]
    """
    status = False
    count_list = dataframe['Count'].tolist()
    fifo = count_list[0]
    for i in count_list:
        if i - fifo > 20:
            status = True
        else:
            fifo = i
    return storing, afdelling, status