# -*- coding:utf-8 -*-
# __author:ivan.wang
# date: 2017/12/28
import os, codecs
import configparser
from config.settings import CONFIG_DIR

class ReadConfig:
    """
    创建ConfigParser对象，读取指定目录conf_path配置文件config_name
    """
    def __init__(self, config_name):
        self.conf = configparser.ConfigParser()
        # 中文乱码问题需要添加encoding="utf-8-sig"
        self.conf.read(os.path.join(CONFIG_DIR, config_name), encoding="utf-8-sig")

    def get_bs(self, name):
        value = self.conf.get("BS", name)
        return value

    def get_db(self, name):
        value = self.conf.get("DB", name)
        return value

    def get_redis(self, name):
        value = self.conf.get("REDIS", name)
        return value

    def get_open_close(self, name):
        value = self.conf.get("OPEN_CLOSE", name)
        return value

    def get_runtime_data(self, name):
        value = self.conf.get("RUNTIME_DATA", name)
        return value

class WithConfig:
    """
    主要作用是获取脚本运行时出错的文件名和行号，然后传递给logger负责打印name信息
    """
    def __init__(self, config_name, section, key, value=None):
        self.section = section
        self.key = key
        self.value = value
        self.config_name = config_name
        self.con = configparser.ConfigParser()
        self.con.read(os.path.join(CONFIG_DIR, config_name), encoding="utf-8-sig")

    def __enter__(self):
        if self.value:
            self.write_config()
            return True
        else:
            return self.read_config()

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_tb is None:
            pass
        else:
            return False   # 可以省略，缺省的None也是被看做是False

    def write_config(self):
        self.con.set(self.section, self.key, self.value)
        self.con.write(codecs.open(os.path.join(CONFIG_DIR, self.config_name),  "w", "utf-8-sig"))

    def read_config(self):
        traceInfo = self.con.get(self.section, self.key)
        return traceInfo

def write_case_info_to_config(case_name):
    with WithConfig("config.ini", "RUNTIME_DATA", "current_testcase_name", case_name):
        pass

def read_case_name_from_config():
    with WithConfig("config.ini", "RUNTIME_DATA", "current_testcase_name") as caseName:
        return caseName

if __name__ == '__main__':
    co = ReadConfig("808_config.ini")
    print(co.get_bs("IP"))
    # print(proDir1)


    # with WithConfig("TRACEBACK", "trace_info") as conInfo:
    #     print(conInfo)



