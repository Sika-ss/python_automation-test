# -*- coding:utf-8 -*-
from tools import constant
from configparser import ConfigParser


class DoConf:

    def __init__(self, files):
        self.cf = ConfigParser()
        self.cf.read(files, encoding='utf-8')
        switch = self.cf.get('switch', 'on')
        if switch == "dev":
            self.file = constant.conf_test_dir
            self.cf.read(constant.conf_test_dir, encoding='utf-8')
        elif switch == "uat":
            self.file = constant.conf_test_dir
            self.cf.read(constant.conf_uat_dir, encoding='utf-8')
        elif switch == "prod":
            self.file = constant.conf_test_dir
            self.cf.read(constant.conf_prod_dir, encoding='utf-8')
        else:
            print("没有匹配到对应的文件")

    def get_value(self, sections, options):
        value = self.cf.get(sections, options)
        return value

    def set_value(self, sections, options, value):
        """
               写入配置文件
               :param sections:
               :param options:
               :param value:
               :param files:
               :return:
               """
        self.cf.set(sections, options, value)
        with open(self.file, 'w') as configfile:
            self.cf.write(configfile)


if __name__ == '__main__':
    dc = DoConf(constant.globe_conf_dir)
