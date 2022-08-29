#!/usr/bin/ python3
# coding: utf-8

from __init__ import *

from Run.core.Analyze.analyze_tool import *
import pandas as pd
import joblib


# Check if the data is normal
# 检测数据是否正常
def check_storing_df(dataset):
    """
    Check dataframe is correct data, if not return False
    :param dataset: DataFrame
    :return: boolean
    """
    # filter data from reniging
    df = dataset[(dataset['<wissel> vergrendeld'] != 0) | (dataset['<wissel> ijzer'] != 0)]
    check_error_list = [
        len(set(df["<vecom> aanvraag onbekend"])) > 1,
        len(set(df["<wissel> ijzer"])) > 1,
        len(set(df["<vecom> storing"])) > 1,
        len(set(df["<vecom> geen output"])) > 1,
        len(set(df["<aanmelden> voertuig"])) > 2,  # !!!!
        len(set(df["<wissel> vergrendeld"])) < 2
    ]
    return any(check_error_list)


# Check again if the data is normal
# 再次检测数据是否正常
def recheck_storing(dataset):
    try:
        # cleaning dataset
        df = dataset[(dataset['<wissel> vergrendeld'] != 0) | (dataset['<wissel> ijzer'] != 0)]
        step_revert = 0
        step_list = df['step']
        step_list = [i for i in step_list if i is not None]
        # is_storing = False
        for i in range(len(step_list) - 1):
            if step_list[i + 1] < step_list[i]:
                step_revert += 1

        return any([step_revert > 3 + (max(df['<aktuell> niveau fifo']) + len(set(df['<aktuell> voertuig']))) * 2,
                    0 in df['<wissel> ijzer'].to_list(),
                    match_list([1, 0, 1], df['<hfp> spoorstroomkring bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfp> spoorstroomkring bezet'].to_list()),
                    match_list([1, 0, 0, 1], df['<hfk> aanwezigheidslus bezet'].to_list()),
                    match_list([1, 0, 1], df['<hfk> aanwezigheidslus bezet'].to_list())])
    except:
        return True

    
# Parse error data
# 分析错误数据
def define_storing(dataset):
    """
    define storing type.
    :param dataset: pd.DataFrame
    :return: str, pd.DataFrame
    """

    error_info = None
    voertuig_nr = max(dataset['<aanmelden> voertuig'].tolist(), key=dataset['<aanmelden> voertuig'].tolist().count)
    storing_type = {
        'begin tijd': [dataset.iloc[1]['date-time']],
        'eind tijd': [dataset.iloc[-1]['date-time']],
        'Wissel Nr': [dataset.iloc[1]['wissel nr']],
        'lijn nr': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> lijn']],
        'service': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> service']],
        'categorie': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> categorie']],
        'voertuig nr': [voertuig_nr],
        'wissel stop': [(min(dataset['<wissel> ijzer']) - 1) * -1]
    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']
    func_list = [
        # Sorting method: Arrange from top to bottom according to the detection index
        # 排序方式：根据检测index从上到下排列
        # 0
        small_dataset(dataset, 'invalid data', 'system'),
        # 1
        hfk_defect(dataset, 'aanwezigheidslus defect', 'infra'),
        # 2
        wissel_buiten_dinst(dataset, 'wissel buiten dienst', 'infra'),
        #19
        wissel_loop_niet_om(dataset, 'wissel loop niet om', 'infra'),
        # 3
        double_wissels(dataset, 'not_error', 'double wissels'),
        
        # 5
        wissel_eind_stand(dataset, 'wissel heeft geen eind stand', 'infra'),
        fifo_fout(dataset, 'afmelden fout', 'infra'),
        # 6
        check_fout_state(dataset, '<vecom> aanvraag onbekend', 'categorie/handbedien code fout', 'bestuurder'),
        # 7
        check_bad_contact(dataset, '<hfp> spoorstroomkring bezet', 'spoorstroomkring detector fout', 'infra'),
        # 8
        check_bad_contact(dataset, '<hfk> aanwezigheidslus bezet', 'aanwezigheidslus detector fout', 'infra'),
        # 9
        # hfk_defect(dataset, 'HFK defect', 'infra'),
        # 10
        check_voertuig_vecom(dataset, 'vecom in voertuig fout', 'voertuig'),
        # 11
        miss_out_meld(dataset, 'afmelden fout', 'infra'),
        
        # 12
        wacht_op_sein(dataset, 'bestuurder wacht niet op sein', 'bestuurder'),
        # 13
        check_fout_state(dataset, '<vecom> storing', 'VECOM hardware fout', 'infra'),
        # 14
        check_fout_state(dataset, '<vecom> geen output', 'wissel niet beschikken voor code', 'bestuurder'),
        check_fout_state(dataset, '<vecom> aanvraag onbekend', 'wissel niet beschikken voor code', 'bestuurder'),
        # 15
        check_werk_voertuig(dataset, 'wissel kan de werk voertuig niet afmeden', 'infra'),
        # 16
        check_verkeerd_code(dataset, 'richting en code niet overeen', 'bestuurder'),
        # 17
        double_input(dataset, 'richting veranderen na de aanvragen', 'bestuurder'),
        # 18
        no_aktuell(dataset, 'bestuurder rit te vroeg naar de spoorstroomkring', 'bestuurder'),
        # 4
        no_voertuig_nr(dataset, 'voertuig zonder vecom', 'voertuig'),
        # 19
        
        
    ]
    try:
        storing_type['voertuig nr'] = [i for i in dataset['<aktuell> voertuig'].tolist() if i != 0][0]
    except:
        storing_type['voertuig nr'] = [0]
    for error_info in func_list:
        if error_info[-1]:
            #  error_info = i
            storing = [error_info[0]]
            afdelling = [error_info[1]]
            if len(error_info) == 7:
                storing_type['lijn nr'] = [error_info[2]]
                storing_type['service'] = [error_info[3]]
                storing_type['categorie'] = [error_info[4]]
                storing_type['voertuig nr'] = [error_info[5]]
            break
        elif recheck_storing(dataset) is not True:
            storing = ['not_error']
    storing_type['storing'] = storing
    storing_type['afdelling'] = afdelling
    storing_type['count'] = [1]

    return storing[0], pd.DataFrame(storing_type)


def define_storing_int(dataset):
    """
    define storing type.
    :param dataset: pd.DataFrame
    :return: str, pd.DataFrame
    """
    stay_list = ['<aanmelden> handbediening', '<aanmelden> voertuig', '<afmelden> voertuig', '<aktuell> voertuig',
                 '<aktuell> niveau fifo', '<wissel> naar links', '<wissel> naar rechts', '<wissel> links',
                 '<wissel> rechts',
                 '<vlsa> links', '<vlsa> rechts', '<wls> seinbeld links geactiveerd',
                 '<wls> seinbeld rechts geactiveerd',
                 '<hfp> spoorstroomkring bezet', '<hfk> aanwezigheidslus bezet', '<vecom> naar links',
                 '<vecom> naar midden',
                 '<vecom> naar rechts', '<vecom> lock', '<vecom> aanvraag onbekend', '<vecom> uit melding',
                 '<wissel> vergrendeld',
                 '<wissel> ijzer', '<bis> wissel buiten dienst', '<vecom> storing', '<vecom> geen output',
                 '<input> naar links',
                 '<input> naar rechts', '<input> naar midden', 'step']
    
    dtc_model = joblib.load(os.path.join(rootPath, 'Run', 'conf', 'pipfiles', 'DTC_model.pkl'))
    storing_int_dict = {
        'not_error': 0, 'wissel buiten dienst': 1, 'invalid data': 2, 'aanwezigheidslus defect':3, 
        'wissel loop niet om':4, 'wissel heeft geen eind stand':5, '<vecom> aanvraag onbekend':6, 
        '<vecom> aanvraag onbekend':7, '<hfk> aanwezigheidslus bezet':8, 'vecom in voertuig fout':9,
        'afmelden fout':10, 'afmelden fout':11, 'bestuurder wacht niet op sein':12, '<vecom> storing':13, 
        '<vecom> geen output':14, '<vecom> aanvraag onbekend':15, 'richting en code niet overeen':16, 
        'richting veranderen na de aanvragen':17, 'bestuurder rit te vroeg naar de spoorstroomkring':18, 
        'voertuig zonder vecom':19,'ontbekend':20,
    }
    int_storing_dict = {v:k for k,v in storing_int_dict.items()}
    storing_afdelint_dict = {
        'invalid data': 'system','aanwezigheidslus defect': 'infra','wissel buiten dienst': 'infra',
        'wissel loop niet om': 'infra','not_error':'double wissels','wissel heeft geen eind stand': 'infra',
        'afmelden fout': 'infra','categorie/handbedien code fout': 'bestuurder',
        'spoorstroomkring detector fout': 'infra','aanwezigheidslus detector fout': 'infra',
        'vecom in voertuig fout': 'voertuig','bestuurder wacht niet op sein':'bestuurder',
        'VECOM hardware fout':'infra','wissel niet beschikken voor code': 'bestuurder',
        'wissel kan de werk voertuig niet afmeden':'infra', 'richting en code niet overeen':'bestuurder',
        'richting veranderen na de aanvragen':'bestuurder',
        'bestuurder rit te vroeg naar de spoorstroomkring': 'bestuurder','voertuig zonder vecom':'voertuig'
    }
    error_info = -1
    voertuig_nr = max(dataset['<aanmelden> voertuig'].tolist(), key=dataset['<aanmelden> voertuig'].tolist().count)
    storing_type = {
        'begin tijd': [dataset.iloc[1]['date-time']],
        'eind tijd': [dataset.iloc[-1]['date-time']],
        'Wissel Nr': [dataset.iloc[1]['wissel nr']],
        'lijn nr': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> lijn']],
        'service': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> service']],
        'categorie': [dataset[dataset['<aanmelden> voertuig'] == voertuig_nr].iloc[0]['<aanmelden> categorie']],
        'voertuig nr': [voertuig_nr],
        'wissel stop': [(min(dataset['<wissel> ijzer']) - 1) * -1]
    }
    storing = ['ontbekend']
    afdelling = ['ontbekend']
    
    dataset = dataset[stay_list]
    voertuig_nr = {0: 0}
    flow_nr = 0
    voertuig = dataset[['<aanmelden> voertuig', '<afmelden> voertuig', '<aktuell> voertuig']]
    np_voertuig = voertuig.to_numpy()
    np_voertuig = np_voertuig.reshape((np_voertuig.shape[0] * np_voertuig.shape[1],))
    for j in np_voertuig:
        if j != 0 and j not in  voertuig_nr.keys():
            flow_nr += 1
            voertuig_nr[j] = flow_nr
    dataset = dataset.replace(voertuig_nr)
    np_1 = dataset.to_numpy()
    np_1 = np_1.reshape((np_1.shape[0] * np_1.shape[1]))
    np_2 = np_1.copy()
    np_2.resize((30, 31))
    np_2 = np_2.reshape((1, np_2.shape[0] * np_2.shape[1]))
    dtc_predict = dtc_model.predict(np_2)
    # print(dtc_predict)
    storing = int_storing_dict.get(dtc_predict[0])
    afdelling = storing_afdelint_dict.get(storing)
    # print(afdelling)
    # print(storing)
    storing_type['storing'] = storing
    storing_type['afdelling'] = [afdelling]
    storing_type['count'] = [1]
    return storing, pd.DataFrame(storing_type)
    
    