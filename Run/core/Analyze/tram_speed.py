# ！/usr/bin/python3
# coding:utf-8
# sys

import sqlalchemy
from Run.core.ConvertData.VerSelect import get_wissel_type_nr
import pandas as pd
from Run.core.ConvertData.ConnectDB import conn_engine


def wagen_lent(wagen_nr):
    """
    default wagen lent
    :param wagen_nr: int
    :return: int
    """
    if 3000 <= wagen_nr < 4000:
        lent = 30
    elif 4000 <= wagen_nr < 5000:
        lent = 37
    elif 5000 <= wagen_nr < 6000:
        lent = 35
    else:
        lent = 0
    return lent


def tram_speed_to_sql(log_db):
    # 从log db中提取tram通过wissel的速度
    """
    Calculate tram speed over the wissel from database
    :param log_db: str
    :return: none
    """

    insp = sqlalchemy.inspect(conn_engine(log_db))
    all_wissels = insp.get_table_names()
    all_wissels = [i for i in all_wissels if i in get_wissel_type_nr('denBDB3C')]
    data_dict = {}
    for wissel_nr in all_wissels:
        try:
            all_data = pd.read_sql_table(wissel_nr, conn_engine(log_db))
            all_data['date-time'] = pd.to_datetime(all_data['date-time'])
            afmeld = 0
            lijn_nr = ''
            hfk_in = 0
            hfk = False
            for i in range(len(all_data)):
                row = all_data.iloc[i]
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
                        tram_speed = row[['<aanmelden> lijn',
                                          '<afmelden> wagen',
                                          '<aanmelden> categorie',
                                          '<aanmelden> service',
                                          'wissel nr']]
                        tram_speed['hfk_in'] = hfk_in
                        tram_speed['hfk_uit'] = hfk_out
                        tram_speed['snelheid km/h'] = round(wagen_lent(row['<afmelden> wagen']) /
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

    for key in data_dict.keys():
        try:
            data_dict.get(key).to_sql(key,
                                      conn_engine(log_db,
                                                  path='snelheid'),
                                      index=False,
                                      if_exists='replace')
        except (ValueError, TypeError, KeyError):
            pass
        
