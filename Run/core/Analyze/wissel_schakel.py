# ！/usr/bin/python3
# coding:utf-8
# sys

import pandas as pd


def wissel_schakel(df):
    """
    Calculate wissel switch from single wissel cycle
    :param df: sigle wissel cycle dataframe
    :return: wissel switch status dataframe
    """
    beweging = {}
    try:
        tijd = df.iloc[1]['date-time']
        wissel_nr = df.iloc[1]['wissel nr']
        position_before = None
        position_after = None
        position_request = None
        position_action = None
        wagen_nr = 0
        wissel_omloop = 0

        for i in range(len(df) - 1):
            row = df.iloc[i]
            row_dict = row.to_dict()
            aktu_wagen = row_dict.get("<aktuell> wagen")

            if aktu_wagen != 0 and wagen_nr == 0:
                wagen_nr = aktu_wagen

            if position_before == None:
                if row_dict.get("<wissel> links") == 1:
                    position_before = "links"
                elif row_dict.get("<wissel> rechts") == 1:
                    position_before = "Rechts"
            elif position_request == None:
                if row_dict.get("<input> naar links") == 1:
                    position_request = "Links"
                elif row_dict.get("<input> naar rechts") == 1:
                    position_request = "Rechts"
                elif row_dict.get("<input> naar gerade") == 1:
                    position_request = "Gerade"
            elif position_action == None:
                if row_dict.get("<wissel> naar links") == 1:
                    position_action = "Links"
                elif row_dict.get("<wissel> naar rechts") == 1:
                    position_action = "Rechts"
            elif position_after == None:
                if row_dict.get("<wissel> links") == 1:
                    position_after = "Links"
                elif row_dict.get("<wissel> rechts") == 1:
                    position_after = "Rechts"
            else:
                wissel_omloop = "Error"

            if position_before == position_request and position_request == position_after:
                wissel_omloop = "Geen"
            elif position_action != None:
                wissel_omloop = 1
        beweging['tijd'] = [tijd]
        beweging['wissel nr'] = [wissel_nr]
        beweging['wagen nr'] = [wagen_nr]
        beweging['voor'] = [position_before]
        beweging['aanvragen'] = [position_request]
        beweging['na'] = [position_after]
        beweging['omloop'] = [wissel_omloop]
        beweging['steps'] = [len(df)]

    except (ValueError, TypeError, KeyError) as err:
        print(err)
        pass

    return pd.DataFrame(beweging)
