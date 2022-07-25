from multiprocessing import Pool

import pandas as pd
from __init__ import *
from Run.core.Integration.DataCalculator import Calculator
from Run.core.Integration.DataInitialization import get_alldata_from_db



def test_wissel_schakel(db_name):
    values = Calculator(db_name)
    values.C_tram_speed()
    values.C_wissel_schakel()
    values.C_storingen()
    return values.error_list

def test_tram_speed(db_name):
    values = Calculator(db_name)
    values.C_tram_speed()
    
if __name__ == '__main__':
    
    db_list = os.listdir(os.path.join(rootPath, "DataBase", "db"))
    db_list = [i for i in db_list if 'db' in i]
    db_list = [i[:-3] for i in db_list]
    db_list.sort()
    
    for i in db_list:
        test_wissel_schakel(i)