# ！/usr/bin/python3
# coding:utf-8
# sys

import sqlalchemy
import pandas as pd
from Run.core.ConvertData.ConnectDB import conn_engine
from Run.core.Analyze.DataInitialization import get_alldata_from_db
from Run.core.Analyze.DataInitialization import save_to_sql
from Run.core.Analyze.VaribleTool import wagen_length


class Calculator:
    """
    Get data from log database
    Calculate log data to useful data
    """

    def __init__(self, db_name):
        """
        Initialization data from sqlite3 db to dict with key = table name
        :param db_name: dict
        """
        self.db_name = db_name
        self.db_dict = get_alldata_from_db(db_name, path='db')

    def C_tram_speed(self):
        """
        Calculate tram speed while tram passing the wissel
        :return: dict
        """
        data_dict = {}
        for key, value in self.db_dict.items():
            try:
                value['date-time'] = pd.to_datetime(value['date-time'])
                afmeld = 0
                lijn_nr = ''
                hfk_in = 0
                richting = 'ontbekend'
                hfk = False
                for i in range(len(value)):
                    row = value.iloc[i]
                    if row['<input> naar gerade'] == 1:
                        richting = 'Recht door'
                    elif row['<input> naar rechts'] == 1:
                        richting = 'Rechts af'
                    elif row['<input> naar links'] == 1:
                        richting = 'links af'

                    if row['<hfk> schakelcriterium bezet'] == 1 and \
                            row['<hfp> schakelcriterium bezet'] == 1 and \
                            row['<afmelden> wagen'] != 0 and \
                            hfk is False:

                        hfk_in = row['date-time']
                        afmeld = row['<afmelden> wagen']
                        lijn_nr = str(row['<aanmelden> lijn'])
                        hfk = True

                    elif row['<hfk> schakelcriterium bezet'] == 0 and \
                            row['<hfp> schakelcriterium bezet'] == 0 and \
                            row['<afmelden> wagen'] != 0 and \
                            hfk is True:

                        hfk_out = row['date-time']
                        hfk = False

                        if afmeld == row['<afmelden> wagen'] and row['<aanmelden> lijn'] != 0:
                            tram_speed = row[[
                                '<aanmelden> lijn',
                                '<afmelden> wagen',
                                '<aanmelden> categorie',
                                '<aanmelden> service',
                                'wissel nr'
                            ]]
                            tram_speed['Richting'] = richting
                            tram_speed['hfk_in'] = hfk_in
                            tram_speed['hfk_uit'] = hfk_out
                            tram_speed['snelheid km/h'] = round(wagen_length(row['<afmelden> wagen']) /
                                                                (hfk_out - hfk_in).total_seconds() * 3.6)
                            tram_speed_df = pd.DataFrame(tram_speed.to_dict(), index=[i])

                            if lijn_nr in data_dict.keys():
                                data_dict[lijn_nr] = pd.concat([data_dict.get(lijn_nr), tram_speed_df])

                            else:
                                data_dict[lijn_nr] = tram_speed_df
                        else:
                            pass
                    else:
                        pass
            except (ValueError, TypeError, KeyError) as err:
                print(err)
                pass
        save_to_sql(self.db_name, data_dict, 'snelheid')

