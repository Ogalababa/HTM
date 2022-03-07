# convert data with H & k Config
import configparser
from __init__ import *


def main_dir():
    curentpath = os.path.dirname(os.path.realpath(__file__))
    curentdir = os.path.basename(curentpath)
    maindir = f'{curentpath.replace(curentdir, "")}'
    return maindir


def bit_config():
    ini_list = os.listdir(os.path.join(main_dir(), 'HkConfig', 'cfg'))
    remove_list = ['.ipynb_checkpoints']
    ini_list = [i for i in ini_list if i not in remove_list]
    bit_configs = {}
    for ini_name in ini_list:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.join(main_dir(), 'HkConfig', 'cfg'), ini_name), 'unicode-escape')
        single_bit = {}
        option_list = config.options('bit')
        for name in option_list:
            single_bit[name] = config.getint('bit', name)
        bit_configs[ini_name[:-4]] = single_bit

    return bit_configs


def byte_config():
    start = 'byte start'
    end = 'byte end'
    ini_list = os.listdir(os.path.join(main_dir(), 'HkConfig', 'cfg'))
    remove_list = ['.ipynb_checkpoints']
    ini_list = [i for i in ini_list if i not in remove_list]
    byte_configs = {}
    for ini_name in ini_list:
        config = configparser.ConfigParser()
        multi_bits = {}
        config.read(os.path.join(os.path.join(main_dir(), 'HkConfig', 'cfg'), ini_name), 'unicode-escape')
        bytes_start = config.options(start)
        for name in bytes_start:
            multi_bits[name] = [config.getint(start, name), config.getint(end, name)]
        byte_configs[ini_name[:-4]] = multi_bits
    return byte_configs


def drop_config():
    ini_list = os.listdir(os.path.join(main_dir(), 'HkConfig', 'cfg'))
    remove_list = ['.ipynb_checkpoints']
    ini_list = [i for i in ini_list if i not in remove_list]
    drop = {}
    for ini_name in ini_list:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.join(main_dir(), 'HkConfig', 'cfg'), ini_name), 'unicode-escape')
        drop_list = config.options('drop')
        drop[ini_name[:-4]] = drop_list
    return drop


