# ！/usr/bin/python3
# coding:utf-8
# sys

import pandas as pd


# Detect wissel steering
# 检测wissel转向
def wissel_schakel(df):
    """
    Calculate wissel switch from single wissel cycle
    :param df: sigle wissel cycle dataframe
    :return: wissel switch status dataframe
    """
    beweging = {}
    tijd = df.iloc[1]['date-time']
    wissel_nr = df.iloc[1]['wissel nr']
    position_before = None
    position_after = None
    position_request = None
    # position_action = None
    wagen_nr = 0
    wissel_omloop = -2  # default Error
    try:

        for i in range(len(df) - 1):
            row = df.iloc[i]
            row_dict = row.to_dict()
            aktu_wagen = row_dict.get("<aktuell> wagen")

            if aktu_wagen != 0 and wagen_nr == 0:
                wagen_nr = aktu_wagen

            if position_before is None:
                if row_dict.get("<wissel> links") == 1:
                    position_before = "Links"
                elif row_dict.get("<wissel> rechts") == 1:
                    position_before = "Rechts"
            elif position_request is None:
                if row_dict.get("<input> naar links") == 1 or row_dict.get("<wls> seinbeld links geactiveerd"):
                    position_request = "Links"
                elif row_dict.get("<input> naar rechts") == 1 or row_dict.get("<wls> seinbeld rechts geactiveerd"):
                    position_request = "Rechts"
                elif row_dict.get("<input> naar gerade") == 1:
                    position_request = "Gerade"
            # elif position_action == None:
            #     if row_dict.get("<wissel> naar links") == 1:
            #         position_action = "Links"
            #     elif row_dict.get("<wissel> naar rechts") == 1:
            #         position_action = "Rechts"
            elif position_request is not None:
                if row_dict.get("<wissel> links") == 1:
                    position_after = "Links"
                elif row_dict.get("<wissel> rechts") == 1:
                    position_after = "Rechts"
            else:
                wissel_omloop = -2

            if position_before != position_after:
                wissel_omloop = 1
            elif position_before == position_after:
                wissel_omloop = 0
            if not all([position_before, position_request, position_after]):
                wissel_omloop = -1
            if wagen_nr == 0:
                wissel_omloop = -1
        beweging['Tijd'] = [tijd]
        beweging['Wissel Nr'] = [wissel_nr]
        beweging['Wagen Nr'] = [wagen_nr]
        beweging['Voor'] = [position_before]
        beweging['aanvragen'] = [position_request]
        beweging['Na'] = [position_after]
        beweging['Schakelen'] = [wissel_omloop]
        beweging['Steps'] = [len(df)]

    except (ValueError, TypeError, KeyError) as err:
        print(f'{wissel_nr}:{err}')
        pass

    if wissel_omloop < 0:
        return [pd.DataFrame(beweging), df]
    else:
        return [pd.DataFrame(beweging)]
