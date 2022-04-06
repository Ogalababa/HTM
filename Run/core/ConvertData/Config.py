# ！/usr/bin/python3
# coding:utf-8
# sys
from __init__ import *
import configparser
import os.path
import re


# noinspection PyTypeChecker
class WisselData:
    """
    Convert wissel data from log file
    """

    def __init__(self, hex_data, bit_config, byte_config):
        """
        :type hex_data: str
        :type bit_config: dict
        :type byte_config: dict
        """

        self.config = configparser.ConfigParser()
        self.hex_data = hex_data
        self.bit_config = bit_config
        self.byte_config = byte_config
        self.wissel_info = {}
        self.wissel_ini = {}
        self.multi_bits = {}
        self.single_bit = {}
        self.hex_str_list = []
        self.hex_str = ''
        self.bin_data = ''
        # data loc
        self.DATA_HEADER = 16
        self.LOC_DATE_START = 0
        self.LOC_DATE_END = 16
        self.LOC_TIME_START = 16
        self.LOC_TIME_END = 40

        # path
        self.curentpath = os.path.dirname(os.path.realpath(__file__))
        curentdir = os.path.basename(self.curentpath)
        self.mainpath = f'{self.curentpath.replace(curentdir, "")}'

        try:
            if self.hex_data.index('PZDA') > 0:
                full_data_start = self.hex_data.index('PZDA') + 4
                self.state_data = self.hex_data[full_data_start:]

                # self.hex_data_list = self.line_to_hex()
                server_date_time = self.hex_data[:19]
                if re.search(r'W\d\d\d', self.hex_data) is not None:
                    self.wissel_info['wissel nr'] = [re.search(r'W\d\d\d', self.hex_data).group()]
                else:
                    pass
                # wissel_nr_start = self.hex_data.index('HTM_') + 4
                # wissel_nr = self.hex_data[wissel_nr_start:wissel_nr_start + 4]

                self.wissel_info['server time'] = [server_date_time]
        except ValueError:
            pass

    def line_to_hex(self):
        """detect hex data from log file"""
        single_hex = ''
        hex_start = False
        hex_end = False

        for check_char in self.state_data:
            try:
                # 判断是否 hex
                if check_char == '<':
                    hex_start = True
                elif check_char == '>':
                    hex_end = True

                elif hex_start is False and hex_end is False:
                    char_to_hex = check_char.encode('utf-8').hex()
                    # print(i)
                    self.hex_str_list.append(char_to_hex)
                else:  # 单个char
                    single_hex += check_char
                if hex_end is True:  # 添加到list，重置判断条件
                    self.hex_str_list.append(single_hex)
                    single_hex = ''
                    hex_start = False
                    hex_end = False

            except ValueError:
                pass

        return self.hex_str_list

    def list_to_str(self):
        """Convert hex data to string"""
        self.hex_str_list.reverse()
        for single_hex in self.hex_str_list:
            self.hex_str += single_hex
        return self.hex_str

    def hex_to_bin(self):
        """Convert hex string to binary string"""
        try:
            interger = int(self.hex_str, 16)
            bits = len(self.hex_str * 4)
            self.bin_data = format(interger, f'0>{bits}b')
        except ValueError:
            pass
        return self.bin_data

    def covert_data(self):
        """Convert binary data to wissel status data"""
        # Record date - time
        record_date = self.bin_data[self.LOC_DATE_START:self.LOC_DATE_END]
        record_time = self.bin_data[self.LOC_TIME_START: self.LOC_TIME_END]

        # data count
        data_count = self.bin_data[-self.DATA_HEADER:]
        self.wissel_info['Count'] = [int(data_count, 2)]
        try:
            self.wissel_info['date-time'] = [
                f'20{int(record_date[9:], 2)}-'
                f'{int(record_date[5:9], 2)}-'
                f'{int(record_date[:5], 2)} '
                f'{str(int(record_time[:5], 2)).zfill(2)}:'
                f'{str(int(record_time[5:11], 2)).zfill(2)}:'
                f'{str(int(record_time[11:17], 2)).zfill(2)}.'
                f'{str(int(record_time[17:], 2)).zfill(2)}'
            ]
            for key, value in self.multi_bits.items():
                bit_data = self.bin_data[-(self.DATA_HEADER + int(value[1])): -(self.DATA_HEADER + int(value[0]) - 1)]

                if key == 'PAR uit':
                    self.wissel_info['<REGISTRATIE> uitgangen'] = [hex(int(bit_data, 2))]

                elif bit_data == '11111111111111111111111111111111':
                    self.wissel_info[key] = [0]

                else:
                    self.wissel_info[key] = [int(bit_data, 2)]

            # Single bit data
            for key, value in self.single_bit.items():
                bit_data = self.bin_data[-(self.DATA_HEADER + int(value))]

                self.wissel_info[key] = [int(bit_data)]

        except ValueError:
            pass
        except IndexError:
            pass
        except TypeError:
            pass
        except KeyError:
            pass

        return self.wissel_info

    def wissel_version(self, version):
        """Get wissel version from wissel nr"""
        if version is None:
            pass
        else:

            # [single_bit]

            self.single_bit = self.bit_config.get(version)

            # [multi_bits]

            self.multi_bits = self.byte_config.get(version)
