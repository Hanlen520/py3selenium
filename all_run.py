#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     ivan.wang
@contact:    357492882@qq.com
@others:     DTStudio, All rights reserved-- Created on 2017/10/25
@desc:       
"""
import unittest
import os
import time
import sys
import xlrd
from public.function import send_mail
from public import HTMLTestRunner
from public.Log import MyLog
from public.ReadConfig import ReadConfig
from config.settings import TEST_DATA_EXCEL_FILE
from config.settings import TEST_CASE_TOP_DIR

test_dir = "./test_case/web_test_case/"
rc = ReadConfig("config.ini")

class RunTest:
    def __init__(self):
        """
        初始化需要的参数
        :return:
        """
        global log, logger, resultPath
        # log初始化
        log = MyLog.get_log("[%s]" % os.path.basename(__file__))
        self.logger = log.get_logger()
        # 定义结果保存路径
        self.resultPath = log.get_report_path()
        # 取得test_case文件路径
        self.caseFile = os.path.join(TEST_CASE_TOP_DIR, "web_test_case")
        # 获取配置文件中的EXCEL路径
        self.xls_path = TEST_DATA_EXCEL_FILE
        self.sheet_name = "INDEX"
        # 定义一个空列表，用于保存类名
        self.caseList = []

    def send_report_by_email(self, report_folder):
        result_dir = report_folder
        lists = os.listdir(result_dir)
        lists.sort(key=lambda fn: os.path.getmtime(result_dir + "\\" + fn))
        # print (u'最新测试生成的报告： '+lists[-1])
        # 找到最新生成的文件
        file_new = os.path.join(result_dir, lists[-1])
        print (file_new)
        # 调用发邮件模块
        send_mail(file_new)

    def find_pyfile_and_import(self, rootDir):
        '遍历rootDir下所有目录是否有“__init__.py”这个文件了，如果没有则创建，import所有test_*.py'
        if os.path.exists(rootDir):
            arr = rootDir.split("/")
            pathDir = ""
            for path in arr:
                pathDir = pathDir + path + "/"
                if not os.path.exists(pathDir + "/__init__.py"):
                    f = open(pathDir + "/__init__.py", 'w')
                    f.close()
        # 遍历文件夹找出test_开头的py文件，导入，注意globals，否则作用域只是在这个函数下
        list_dirs = os.walk(rootDir)
        for dirName, subdirList, fileList in list_dirs:
            for f in fileList:
                file_name = f
                if file_name[0:5] == "test_" and file_name[-3:] == ".py":
                    if dirName[-1:] != "/":
                        impPath = dirName.replace("/", ".")[2:].replace("\\", ".")
                    else:
                        impPath = dirName.replace("/", ".")[2:-1]
                    if impPath != "":
                        exe_str = "from " + impPath + " import " + file_name[0:-3]
                    else:
                        exe_str = "import " + file_name[0:-3]
                    exec(exe_str, globals())

    def get_xls_case_by_index(self):
        '根据数据表中维护的结果顺序添加case，结果保存在一个list中返回'
        file = xlrd.open_workbook(self.xls_path)
        sheet = file.sheet_by_name(self.sheet_name)
        ncols = sheet.ncols
        for j in range(ncols):
            cell_value = sheet.cell_value(0, j)
            if cell_value == "fileName":
                col1 = j
            elif cell_value == "ClassName":
                col2 = j
            elif cell_value == "caseName":
                col3 = j
            else:
                pass
        nrows = sheet.nrows
        caseList = []
        for i in range(1, nrows):
            if sheet.row_values(i)[0].lower().strip() == 'ready':
                try:
                    fileName = sheet.cell_value(i, col1)
                    ClassName = sheet.cell_value(i, col2)
                    caseName = sheet.cell_value(i, col3)
                    # 组装测试用例名称为格式：文件名.类名（‘方法名’）
                    case = '%s.%s("%s")' % (fileName.strip(), ClassName.strip(), caseName.strip())
                    caseList.append(case)
                except TypeError as ex:
                    print("请检查Excel中sheet:%s是否有维护表头信息[fileName][ClassName][caseName]" % self.sheet_name)
                    raise ex
        return caseList

    def gen_test_suite(self, testDir):
        '参数testDir为所有脚本的顶层目录'
        testunit = unittest.TestSuite()
        self.find_pyfile_and_import(testDir)     # 导入所有test_*.py文件
        testCaseList = self.get_xls_case_by_index()    # 获取需要执行的所有case的列表
        for test_case in testCaseList:            # 从testCaseList中读取case并顺序添加
            testunit.addTest(eval(test_case))
        return testunit

    def run(self):
        '将项目的目录加载到系统变量中'
        cur_dir = os.getcwd()
        sys.path.append(cur_dir)
        now = time.strftime("%Y-%m-%d %H_%M_%S")
        os.environ['WEBSERVICE_ITERATION_RUN_TIME'] = now
        report_folder = cur_dir + os.sep + 'report' + os.sep
        filename = report_folder + now + '_result.html'  # 测试报告的路径名
        try:
            all_test_units = self.gen_test_suite(test_dir)
            if all_test_units is not None:
                self.logger.info("******************************ALL RUN START******************************")
                fp = open(filename, 'wb')  # 打开测试报告文件
                runner = HTMLTestRunner.HTMLTestRunner(
                    stream=fp,
                    title='Test Report',
                    description='Test Description',
                    verbosity=2)
                runner.run(all_test_units)
                # 根据setting中发送邮件的开关确定是否发送邮件报告
                if rc.get_open_close("is_send_email") == "True":
                    self.send_report_by_email(report_folder)  # 发送报告
            else:
                self.logger.info("Have no case to test.")
        except Exception as e:
            logger.error(str(e))
        finally:
            self.logger.info("*******************************ALL RUN END*******************************")
            fp.close()

if __name__ == '__main__':
    testRun = RunTest()
    testRun.run()


