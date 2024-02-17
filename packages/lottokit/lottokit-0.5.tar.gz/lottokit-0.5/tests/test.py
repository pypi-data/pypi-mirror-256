#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : zhengdongqi
@Email   : nickdecodes@163.com
@Usage   :
@FileName: test.py
@DateTime: 2024/1/28 20:13
@SoftWare: 
"""

from lottokit.daletou import Daletou
from collections import Counter
from itertools import combinations
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Iterable, List, Tuple, Any, Optional, Union, Set, Dict
import re


class Test(Daletou):
    def __int__(self, **kwargs):
        super().__init__(**kwargs)

    def get_history_num_count(self):
        history_data = self.read_csv_data_from_file(self.history_record_path, app_log=self.app_log)
        all_count = len(list(history_data[:-1]))
        print(all_count)
        num_front_count = Counter()
        num_back_count = Counter()

        for comb in history_data[-11:-1]:
            num_front_count.update(self.calculate_front(comb))
            num_back_count.update(self.calculate_back(comb))

        return num_front_count, num_back_count

    def get_all_number_frequency(self, start=1, end=35, size=5):
        # 生成1到35之间取5个数的所有组合
        all_combinations = list(combinations(range(start, end + 1), size))

        # 将所有组合展开为一个列表
        all_numbers = [number for combination in all_combinations for number in combination]

        # 统计每个数字的频率
        number_frequency = Counter(all_numbers)

        # 计算每个数字的百分比
        total_count = len(all_numbers)
        number_percentage = {number: (count / total_count) * 100 for number, count in number_frequency.items()}

        print(number_percentage)
        return number_frequency


    def run(self):
        num_front_count, num_back_count = self.get_history_num_count()
        print(num_front_count.most_common())
        print(num_back_count.most_common())
        self.get_all_number_frequency(start=1, end=35, size=5)
        self.get_all_number_frequency(start=1, end=12, size=2)


if __name__ == '__main__':
    # t = Test()
    # t.run()
    t = Daletou()
    t.download_data(force=True)

