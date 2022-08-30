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
        # 19
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

    # error_info = None
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
    storing_int_dict = {'invalid data': 0, 'aanwezigheidslus defect': 1, 'wissel buiten dienst': 2,
                        'wissel loop niet om': 3, 'not_error': 4, 'wissel heeft geen eind stand': 5,
                        'afmelden fout': 6, 'categorie/handbedien code fout': 7, 'spoorstroomkring detector fout': 8,
                        'aanwezigheidslus detector fout': 9, 'wissel niet beschikken voor code': 10,
                        'vecom in voertuig fout': 11, 'bestuurder wacht niet op sein': 12, 'VECOM hardware fout': 13,
                        'wissel kan de werk voertuig niet afmeden': 14, 'richting en code niet overeen': 15,
                        'richting veranderen na de aanvragen': 16,
                        'bestuurder rit te vroeg naar de spoorstroomkring': 17, 'voertuig zonder vecom': 18,
                        }
    func_list = [
        # Sorting method: Arrange from top to bottom according to the detection index
        # 排序方式：根据检测index从上到下排列
        # 0
        small_dataset(dataset, 'invalid data', 'system'),
        # 1
        hfk_defect(dataset, 'aanwezigheidslus defect', 'infra'),
        # 2
        wissel_buiten_dinst(dataset, 'wissel buiten dienst', 'infra'),
        # 19
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
    storing_type['storing'] = storing[0]
    storing_type['afdelling'] = afdelling
    storing_type['count'] = [1]

    return storing[0], pd.DataFrame(storing_type)


def define_storing_ai(dataset):
    # ML learning model
    dtc_model = joblib.load(os.path.join(rootPath, 'Run', 'conf', 'pipfiles','DTC_model.pkl'))

    # Constants
    stay_list = ['wissel nr', '<aanmelden> handbediening', '<aanmelden> voertuig', '<afmelden> voertuig',
                 '<aktuell> voertuig',
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
    wissel_int_dict = {
        'W425': 425, 'W050': 50, 'W520': 520, 'W624': 624, 'W623': 623, 'W233': 233, 'W001': 1, 'W003': 3,
        'W014': 14, 'W038': 38, 'W059': 59, 'W067': 67, 'W081': 81, 'W094': 94, 'W113': 113, 'W116': 116,
        'W117': 117, 'W119': 119, 'W121': 121, 'W133': 133, 'W135': 135, 'W139': 139, 'W140': 140,
        'W153': 153, 'W157': 157, 'W159': 159, 'W161': 161, 'W164': 164, 'W198': 198, 'W202': 202,
        'W223': 223, 'W228': 228, 'W230': 230, 'W232': 232, 'W235': 235, 'W263': 263, 'W268': 268,
        'W269': 269, 'W271': 271, 'W273': 273, 'W275': 275, 'W279': 279, 'W305': 305, 'W307': 307,
        'W338': 338, 'W340': 340, 'W383': 383, 'W391': 391, 'W480': 480, 'W525': 525, 'W530': 530,
        'W542': 542, 'W578': 578, 'W580': 580, 'W583': 583, 'W601': 601, 'W603': 603, 'W605': 605,
        'W613': 613, 'W630': 630, 'W632': 632, 'W640': 640, 'W643': 643, 'W005': 5, 'W013': 23, 'W027': 27,
        'W028': 28, 'W031': 31, 'W035': 35, 'W037': 37, 'W046': 46, 'W056': 56, 'W057': 57, 'W066': 66,
        'W091': 91, 'W118': 118, 'W146': 146, 'W156': 156, 'W166': 166, 'W180': 180, 'W182': 182,
        'W184': 184, 'W194': 194, 'W199': 199, 'W201': 201, 'W204': 204, 'W242': 242, 'W244': 244,
        'W257': 257, 'W260': 260, 'W262': 262, 'W297': 297, 'W378': 378, 'W385': 385, 'W392': 392,
        'W399': 399, 'W523': 523, 'W532': 532, 'W533': 533, 'W537': 537, 'W550': 550, 'W564': 564,
        'W571': 571, 'W573': 573, 'W576': 576, 'W584': 584, 'W586': 586, 'W588': 588, 'W607': 607,
        'W615': 615, 'W617': 617, 'W619': 619, 'W621': 621, 'W628': 628, 'W634': 634, 'W636': 636,
        'W638': 638, 'W644': 644, 'W649': 649, 'W657': 657, 'W658': 658, 'W033': 33, 'W052': 52, 'W079': 79,
        'W104': 104, 'W120': 120, 'W151': 151, 'W169': 169, 'W171': 171, 'W178': 178, 'W189': 189,
        'W200': 200, 'W246': 246, 'W072': 72, 'W084': 84, 'W487': 487, 'W560': 560, 'W595': 595,
        'W500': 500, 'W662': 662, 'W665': 665, 'W668': 668, 'W018': 18, 'W022': 22, 'W127': 127, 'W129': 129,
        'W689': 689, 'W692': 692, 'W145': 145, 'W291': 291, 'W646': 646, 'W651': 651, 'W666': 666,
        'W656': 656, 'W540': 540, 'W660': 660, 'W661': 661,
    }
    storing_int_dict = {'invalid data': 0, 'aanwezigheidslus defect': 1, 'wissel buiten dienst': 2,
                        'wissel loop niet om': 3, 'not_error': 4, 'wissel heeft geen eind stand': 5,
                        'afmelden fout': 6, 'categorie/handbedien code fout': 7, 'spoorstroomkring detector fout': 8,
                        'aanwezigheidslus detector fout': 9, 'wissel niet beschikken voor code': 10,
                        'vecom in voertuig fout': 11, 'bestuurder wacht niet op sein': 12, 'VECOM hardware fout': 13,
                        'wissel kan de werk voertuig niet afmeden': 14, 'richting en code niet overeen': 15,
                        'richting veranderen na de aanvragen': 16,
                        'bestuurder rit te vroeg naar de spoorstroomkring': 17, 'voertuig zonder vecom': 18,
                        'ontbekend': 19,
                        }
    int_storing_dict = {value: key for key, value in storing_int_dict.items()}
    storing_afdelling_dict = {'invalid data': 'system', 'aanwezigheidslus defect': 'infra',
                              'wissel buiten dienst': 'infra', 'wissel loop niet om': 'infra',
                              'not_error': 'double wissels', 'wissel heeft geen eind stand': 'infra',
                              'afmelden fout': 'infra', 'categorie/handbedien code fout': 'bestuurder',
                              'spoorstroomkring detector fout': 'infra', 'aanwezigheidslus detector fout': 'infra',
                              'vecom in voertuig fout': 'voertuig', 'bestuurder wacht niet op sein': 'bestuurder',
                              'VECOM hardware fout': 'infra', 'wissel niet beschikken voor code': 'bestuurder',
                              'wissel kan de werk voertuig niet afmeden': 'infra',
                              'richting en code niet overeen': 'bestuurder',
                              'richting veranderen na de aanvragen': 'bestuurder',
                              'bestuurder rit te vroeg naar de spoorstroomkring': 'bestuurder',
                              'voertuig zonder vecom': 'voertuig',
                              }

    # cycle info
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

    # cleaning data
    voertuig_nr = {0: 0}
    flow_nr = 0
    voertuig = dataset[['<aanmelden> voertuig', '<afmelden> voertuig', '<aktuell> voertuig']]
    np_voertuig = voertuig.to_numpy()
    np_voertuig = np_voertuig.reshape((np_voertuig.shape[0] * np_voertuig.shape[1],))
    for j in np_voertuig:
        if j != 0 and j not in voertuig_nr.keys():
            flow_nr += 1
            voertuig_nr[j] = flow_nr
    dataset = dataset.replace(voertuig_nr)
    dataset = dataset.replace(wissel_int_dict)
    dataset = dataset[stay_list]
    np_1 = dataset.to_numpy()
    np_1 = np_1.reshape((np_1.shape[0] * np_1.shape[1]))
    np_2 = np_1.copy()
    np_2.resize((30, len(stay_list)))
    np_2 = np_2.reshape((1, np_2.shape[0] * np_2.shape[1]))
    predict = dtc_model.predict(np_2)
    storing = int_storing_dict.get(predict[0])
    afdelling = storing_afdelling_dict.get(storing)
    storing_type['storing'] = [storing]
    storing_type['afdelling'] = [afdelling]
    storing_type['count'] = [1]

    return storing, pd.DataFrame(storing_type)

