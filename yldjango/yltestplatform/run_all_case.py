# -*- coding:utf-8 -*-
#!/usr/local/bin/python3
# @Time    : 2017-11-24
# WT


import unittest
import os

#测试用例路径
#case_path = os.path.join(os.getcwd(),'case')
case_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'TestCase')
#报告路径
report_path = os.path.join(os.getcwd(),'report')

def all_case():
    discover = unittest.defaultTestLoader.discover(case_path,pattern='test*.py',top_level_dir=None)
    print(discover)
    return discover


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(all_case())
