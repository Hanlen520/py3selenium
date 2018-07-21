#!/usr/bin/env python
"""
@author:     ivan.wang
@contact:    357492882@qq.com
@others:     DTStudio, All rights reserved-- Created on 2017/11/10
@desc:
"""
import xlrd
from unittest import TestCase
from selenium import webdriver
from config import settings
from public.Log import Log

class BaseSeleniumTestCase(TestCase):

    def get_web_driver(self):
        driver = webdriver.Chrome()
        driver.maximize_window()
        return driver

    def setUp(self):
        self.selenium = self.get_web_driver()
        self.log = Log("[%s][%s]" % (self.get_current_case_file_name(), self.get_current_case_class_name()))
        self.logger = self.log.get_logger()
        self.dataDict = self.get_excel_data_by_casename(settings.TEST_DATA_EXCEL_FILE)  # 获取当前在执行的case的测试数据[dict]
        self.log.build_start_line(self.dataDict['caseName'], self.dataDict['description'])  # 打印case开始线到日志

    def tearDown(self):
        self.log.build_end_line(self.dataDict['caseName'])  # 打印case结束线到日志
        self.selenium.quit()

    def get_excel_data_by_casename(self, excelFile, colIndex=0, sheetName=u'test_csv'):  # 修改自己路径
        test_name = self.get_current_case_name()  # 获取调用函数的函数名称(test_name)
        data = xlrd.open_workbook(excelFile)
        table = data.sheet_by_name(sheetName)  # 获得表格
        nrows = table.nrows  # 拿到总共行数
        colnames = table.row_values(colIndex)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
        rownums = 0
        findrow = 0
        for i in range(nrows):
            cell_value = table.cell_value(i, colIndex)
            if test_name == str(cell_value):
                findrow += 1
                rownums = i
        assert findrow == 1, 'None or more than one test name in excel sheet, please check!'
        row = table.row_values(rownums)
        excelDict = {}
        for j in range(0, len(colnames)):
            # if row[j] == '':
            #     continue
            excelDict[colnames[j]] = row[j]  # 表头与数据对应
        return excelDict

    def get_current_case_name(self):
        '获取当前运行的case的name'
        return super().id().split(".")[-1]

    def get_current_case_class_name(self):
        '获取当前运行的case所在的类名'
        return super().id().split(".")[-2]

    def get_current_case_file_name(self):
        '获取当前运行的case所在的文件名'
        return "%s.py" % super().id().split(".")[-3]