from multiprocessing import Pool
from datetime import datetime
import sys
import pandas as pd
from __init__ import *
from Run.core.Integration.DataCalculator import Calculator
from Run.core.Integration.DataInitialization import get_alldata_from_db



def test_wissel_schakel(db_name):
    values = Calculator(db_name)
    # print('tram sepeed')
    values.C_tram_speed()
    # print('schakel')
    values.C_wissel_schakel()
    # print('storing')
    values.C_storingen()
    return values.error_list

def test_tram_speed(db_name):
    values = Calculator(db_name)
    values.C_tram_speed()
    
if __name__ == '__main__':
    
    
        start = datetime.now()
        print(sys.argv[1])
        test_wissel_schakel(sys.argv[1])
        end = datetime.now()
        print((end - start).total_seconds())