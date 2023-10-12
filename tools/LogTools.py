# -*- coding:utf-8 -*-
import logging
import os
from tools import constant
from tools.ConfTools import DoConf


class DoLogs:

    def __init__(self, login_name):
        conf = DoConf(constant.globe_conf_dir)
        # 定义一个日志收集器
        self.mylog = logging.getLogger(login_name)
        if not self.mylog.handlers:
            # 设置收集级别
            self.mylog.setLevel(conf.get_value('log_level', 'debug'))

            # 设置日志输出格式
            formatter = logging.Formatter(conf.get_value('log_format', 'format'))

            # 设置日志控制台输出
            hdr = logging.StreamHandler()
            hdr.setLevel(conf.get_value('log_level', 'debug'))
            hdr.setFormatter(formatter)

            # 设置日志文件输出
            folder = os.path.exists(constant.log_dir)
            if not folder:
                os.makedirs(constant.log_dir)
            fdr = logging.FileHandler(os.path.join(constant.log_dir, 'log_info.log'), encoding='utf-8')
            fdr.setLevel(conf.get_value('log_level', 'debug'))
            fdr.setFormatter(formatter)

            # 日志与收集器对接
            self.mylog.addHandler(hdr)
            self.mylog.addHandler(fdr)

        # 清除日志缓存
        # self.mylog.removeHandler(hdr)
        # self.mylog.removeHandler(fdr)
