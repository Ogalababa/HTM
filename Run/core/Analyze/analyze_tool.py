# ！/usr/bin/python3
# coding:utf-8
# sys
from typing import Tuple, Any

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
                                    match_list([1, 0, 0, 1, 0], dataframe[col_name].to_list()),
                                    len(dataframe[dataframe[col_name] == 1]) / len(dataframe) > 0.7])


def check_fout_state(dataframe, col_name: str, storing: str, afdelling: str) -> Tuple[
        str, str, int, int, int, int, bool]:
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
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    if 1 in dataframe[col_name].to_list():
        lijn_nr = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> lijn']
        service = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> service']
        categorie = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> categorie']
        wagen_nr = dataframe[dataframe[col_name] == 1].iloc[0]['<aanmelden> wagen']
    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, 1 in dataframe[col_name].to_list()


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
    midden = wissel_gerade(wissel_nr)
    wissel_ijzer_index = dataframe[dataframe['<wissel> ijzer'] == 0].index.to_list()
    verkeerd_code = []
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    if len(wissel_ijzer_index) == 0:
        return storing, afdelling, lijn_nr, service, categorie, wagen_nr, False
    else:
        try:
            lijn_nr = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> lijn']
            service = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> service']
            categorie = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> categorie']
            wagen_nr = dataframe[dataframe['<wissel> ijzer'] == 0].iloc[0]['<aanmelden> wagen']
            for i in wissel_ijzer_index:
                sub_cycle = dataframe[dataframe['<aanmelden> wagen'] == dataframe.loc[i]['<aanmelden> wagen']]
                request_direction = None
                if 1 in sub_cycle['<input> naar midden'].tolist() and request_direction is None:
                    request_direction = midden
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
            return storing, afdelling, lijn_nr, service, categorie, wagen_nr, any(verkeerd_code)
        except KeyError:
            return storing, afdelling, lijn_nr, service, categorie, wagen_nr, False


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
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    for i in wagen_nr_set:
        sub_cycle_dataframe = dataframe[(dataframe['<aanmelden> wagen'] == i) &
                                        (dataframe["<hfp> spoorstroomkring bezet"] == 1) &
                                        (dataframe["<hfk> aanwezigheidslus bezet"] == 0)]
        if len(sub_cycle_dataframe) > 0:
            lijn_nr = sub_cycle_dataframe.iloc[0]['<aanmelden> lijn']
            service = sub_cycle_dataframe.iloc[0]['<aanmelden> service']
            categorie = sub_cycle_dataframe.iloc[0]['<aanmelden> categorie']
            wagen_nr = sub_cycle_dataframe.iloc[0]['<aanmelden> wagen']
            if any([1 not in sub_cycle_dataframe['<vecom> uit melding'].tolist(),
                    0 not in sub_cycle_dataframe['<vecom> uit melding'].tolist()]):
                return storing, afdelling, lijn_nr, service, categorie, wagen_nr, \
                    all([True, 0 in sub_cycle_dataframe['<wissel> ijzer'].to_list()])
        else:
            continue
    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, False


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
    return storing, afdelling, any(
        [all([max(dataframe['<wissel> links']) == 0, max(dataframe['<wissel> rechts']) == 0]),
        max(dataframe['<bis> wissel buiten dienst'] == 1)])


def wissel_eind_stand(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    check if the wissel do not have end state
    :param dataframe: pd.DataFrame
    :param afdelling: str
    :param storing: str
    :return: Tuple[bool, str, str
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


def wacht_op_sein(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    # Check if the driver is driving in sequence
    # 检测司机是否按序行驶
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    state_list = []
    for i in hfp_start_index(dataframe['<hfp> spoorstroomkring bezet'].tolist()):
        if i <= 3:
            hfp_error = all([all(dataframe.iloc[:i + 1]['<wls> seinbeld links geactiveerd'] == 0),
                            all(dataframe.iloc[:i + 1]['<wls> seinbeld rechts geactiveerd'] == 0)])
            state_list.append(hfp_error)
        else:
            hfp_error = all([all(dataframe.iloc[i - 3:i + 1]['<wls> seinbeld links geactiveerd'] == 0),
                            all(dataframe.iloc[i - 3:i + 1]['<wls> seinbeld rechts geactiveerd'] == 0)])
            state_list.append(hfp_error)
        if hfp_error:
            wagen_nr = dataframe.iloc[i]['<aanmelden> wagen']
            service = dataframe.iloc[i]['<aanmelden> service']
            categorie = dataframe.iloc[i]['<aanmelden> categorie']
            lijn_nr = dataframe.iloc[i]['<aanmelden> lijn']
    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, any(state_list),


def no_wagen_nr(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    # Check if the vehicle has vecom installed
    # 检测车辆是是否安装vecom
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    if 0 in dataframe['<aanmelden> wagen'].tolist():
        lijn_nr = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> lijn']
        service = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> service']
        categorie = dataframe[dataframe['<aanmelden> wagen'] == 0].iloc[0]['<aanmelden> categorie']

    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, 0 in dataframe['<aanmelden> wagen'].tolist()


def small_dataset(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    null_state = dataframe['step'].tolist().count('0')
    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, \
        any([len(dataframe) < 4, all([4 <= len(dataframe) < 10, null_state / len(dataframe) > 0.7])])


def double_wissels(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    wissel_nr = dataframe['wissel nr'].to_list()[0]
    if wissel_nr == 'W091':
        if all([32 in dataframe['<aanmelden> uitgang'].to_list(),
                1 in dataframe['<vecom> geen output'].to_list()]):
            return storing, afdelling, True
        else:
            return storing, afdelling, False
    elif wissel_nr == 'W533':
        if all([8 in dataframe['<aanmelden> uitgang'].to_list(),
                1 in dataframe['<vecom> geen output'].to_list()]):
            return storing, afdelling, True
        else:
            return storing, afdelling, False

    else:
        return storing, afdelling, False


def double_input(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    """
    check there are double direction request from tram to wissel
    :param dataframe: pd.dataframe
    :param storing: str
    :param afdelling: str
    :return: Tuple[str, str, int, int, int, int, bool]
    """
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    try:
        double_input_dataset = dataframe[
            ((dataframe['<input> naar links'] == 1) & (dataframe['<input> naar midden'] == 1)) |
            ((dataframe['<input> naar links'] == 1) & (dataframe['<input> naar rechts'] == 1)) |
            ((dataframe['<input> naar rechts'] == 1) & (dataframe['<input> naar midden'] == 1))
        ]
        if len(double_input_dataset) >= 1:
            lijn_nr = double_input_dataset['<aanmelden> lijn'].to_list()[0]
            service = double_input_dataset['<aanmelden> service'].to_list()[0]
            categorie = double_input_dataset['<aanmelden> categorie'].to_list()[0]
            wagen_nr = double_input_dataset['<aanmelden> wagen'].to_list()[0]
            
            return storing, afdelling, lijn_nr, service, categorie, wagen_nr, \
                all([True, 0 in dataframe['<wissel> ijzer'].to_list()])
        else:
            return storing, afdelling, lijn_nr, service, categorie, wagen_nr, False
    except:
        return storing, afdelling, lijn_nr, service, categorie, wagen_nr, False


def no_aktuell(dataframe, storing: str, afdelling: str) -> Tuple[str, str, int, int, int, int, bool]:
    """
    check if aanmelden wagen niet verhandeld
    :param dataframe: pd.dataframe
    :param storing: str
    :param afdelling: str
    :return: Tuple[str, str, int, int, int, int, bool]
    """
    lijn_nr = -1
    service = -1
    categorie = -1
    wagen_nr = -1
    error_status = False
    aanmelden_set = set(dataframe[(dataframe['<aanmelden> wagen']) != \
                                  (dataframe['<afmelden> wagen'])]['<aanmelden> wagen'].to_list())
    for i in aanmelden_set:
        sub_df = dataframe[dataframe['<aanmelden> wagen'] == i]
        if i not in sub_df['<aktuell> wagen'].to_list() and 1 in sub_df['<aktuell> niveau fifo'].to_list():
            lijn_nr = sub_df['<aanmelden> lijn'].to_list()[0]
            service = sub_df['<aanmelden> service'].to_list()[0]
            categorie = sub_df['<aanmelden> categorie'].to_list()[0]
            wagen_nr = sub_df['<aanmelden> wagen'].to_list()[0]
            error_status = True
            return storing, afdelling, lijn_nr, service, categorie, wagen_nr, error_status
        else:
            pass
    return storing, afdelling, lijn_nr, service, categorie, wagen_nr, error_status


def hfk_defect(dataframe, storing: str, afdelling: str) -> Tuple[str, str, bool]:
    """
    Bepaal of hfk beschadigd is
    判断hfk是否损坏
    :param dataframe: pd.DataFrame
    :param storing: str
    :param afdelling: str
    :return: Tuple(str, str, int, int, int, int, bool)
    """
    return storing, afdelling, len(dataframe[dataframe['<hfk> aanwezigheidslus bezet']== 1]) / len(dataframe) > 0.6


def wissel_loop_niet_om(dataframe, storing:str, afdelling: str) -> Tuple[str, str, bool]:
    """
        check if the wissel do not have end state
        :param dataframe: pd.DataFrame
        :param afdelling: str
        :param storing: str
        :return: Tuple[bool, str, str
        """
    naar_links = list(dataframe['<wissel> naar links'] + dataframe['<wissel> rechts'])
    naar_rechts = list(dataframe['<wissel> naar rechts'] + dataframe['<wissel> links'])
    error_data = [2,2,2]
    error_status = []
    for i in range(len(naar_rechts)):
        error_status.append(naar_rechts[i:i+3] == error_data)
    for i in range(len(naar_links)):
        error_status.append(naar_links[i:i + 3] == error_data)
    return storing, afdelling, any(error_status)