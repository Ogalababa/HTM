# ！/usr/bin/python3
# coding:utf-8
# sys
from Run.core.Tools.VaribleTool import wissel_gerade


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
                match_list([1, 0, 0, 1], dataframe[col_name].to_list()),
                len(dataframe[dataframe[col_name] == 1]) / len(dataframe) > 0.5])


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


def check_verkeerd_code(dataframe) -> bool:
    """
    check if the trame with wrong code
    :param dataframe: pd.DataFrame
    :return: bool
    """
    wissel_nr = dataframe['wissel nr'].tolist()[0]
    gerade = wissel_gerade(wissel_nr)
    wissel_ijzer_index = dataframe[dataframe['<wissel> ijzer'] == 0].index.to_list()
    verkeerd_code = []
    if len(wissel_ijzer_index) == 0:
        return False
    else:
        try:
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
            return any(verkeerd_code)
        except KeyError:
            return False


def miss_out_meld(dataframe) -> bool:
    """
    check if vecom afmelden error
    :param dataframe: pd.DataFrame
    :return: Bool
    """
    wagen_nr_list = list(set(dataframe['<aanmelden> wagen'].tolist()))
    out_lus_list = []
    for i in wagen_nr_list:
        try:
            sub_cycle = dataframe[dataframe['<aanmelden> wagen'] == i]
            hfk_dataset = sub_cycle[sub_cycle['<hfk> schakelcriterium bezet'] == 1]
            if 1 in hfk_dataset['<vecom> aftellen'].tolist():
                out_lus_list.append(True)
            else:
                out_lus_list.append(False)
        except KeyError:
            return False
    return any(out_lus_list)


def check_wagen_vecom(dataframe) -> bool:
    """
    check the condition of the vecom in tram
    :param dataframe: pd.DataFrame
    :return: Bool
    """
    aanmelden_list = dataframe['<aanmelden> wagen'].tolist()
    fifo_wagen = None
    handel_list = []
    for i in aanmelden_list:
        if i != fifo_wagen:
            handel_list.append(i)
            fifo_wagen = i
    return len(handel_list) != len(set(handel_list))


def wissel_buiten_dinst(dataframe) -> bool:
    """
    check if the wissel out of order
    :param dataframe: pd.DataFrame
    :return: Bool
    """
    return all([max(dataframe['<wissel> links']) == 0, max(dataframe['<wissel> rechts']) == 0])


def wissel_eind_stand(dataframe) -> bool:
    """
    check if the wissel do not have end state
    :param dataframe: pd.DataFrame
    :return: Bool
    """
    eind_stand = dataframe[(dataframe['<wissel> links'] == 0) & (dataframe['<wissel> rechts'] == 0)]
    
    return len(eind_stand) / len(dataframe) >= 0.3 and len(eind_stand) / len(dataframe) != 1


