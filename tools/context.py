import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import json
import string

from faker import Faker
import re
import time
import hashlib
import random
import datetime
import configparser
from tools.ConfTools import DoConf
from tools import constant
from operation.common.result_base import ResultBase


def param_replace(data) -> str:
    """
    替换data中带##的字段
    :param data:
    :return:
    """
    if data:
        data = str(data)
        p = "@@(.*?)@@"
        while re.search(p, data):
            params = re.search(p, data)
            params1 = params.group(1)
            try:
                params2 = DoConf(constant.globe_conf_dir).get_value('data', params1)
                if type(params2) != str:
                    params2 = str(params2)
            except configparser.NoOptionError as e:
                if hasattr(ResultBase, params1):
                    params2 = getattr(ResultBase, params1)
                    if type(params2) != str:
                        params2 = str(params2)
                elif params1 == 'get_now_time(1)':
                    exec(params1)  # exec可以执行python代码
                    params2 = getattr(ResultBase, 'date')
                elif params1 == 'generate_name()':
                    exec(params1)
                    params2 = getattr(ResultBase, 'person_name')
                elif params1 == 'generate_id_card()':
                    exec(params1)
                    params2 = getattr(ResultBase, 'person_idcard')
                elif params1 == 'generate_phone()':
                    exec(params1)
                    params2 = getattr(ResultBase, 'person_number')
                elif params1 == 'generate_title()':
                    exec(params1)
                    params2 = getattr(ResultBase, 'title')
                elif params1 == 'get_timestamp()':
                    exec(params1)
                    params2 = getattr(ResultBase, 'timestamp')
                else:
                    print("找不到相关值")
                    params2 = 'None'
                    # raise e
            data = re.sub(p, str(params2), data, count=1)
    return data


def get_random_number(data=None):
    """
    生成一个当前日期和随机数的组合
    :param data:
    :return:
    """
    if data:
        today = datetime.datetime.now().strftime('%m%d')
        num = random.randint(1, 100)
        data = data + "_" + today + str(num)
        return data


def get_now_time(istime: int = 0):
    """
     获取当前时间
    :param istime: 标记是否返回详细时间
    :return: 返回当前时间
    """
    if istime:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    setattr(ResultBase, 'date', date)
    return date


def modify_date(data):
    if data:
        # 匹配2020-07-06T19:00:00这样的日期，然后取T后面的值
        p = "A\\d{4}-\\d{2}-\\d{2}(T\\d{2}:\\d{2}:\\d{2})A"
        p1 = "B(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2})B"
        while re.search(p, data):
            params1 = re.search(p, data).group(1)
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            update_time = today + params1
            # 替换所传参数中的日期
            data = re.sub(p, update_time, data, count=1)
        # 匹配以"B()B"包裹的日期字段，并替换为当前日期
        if re.search(p1, data):
            today = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S')
            data = re.sub(p1, today, data, count=1)
    return data


def data_format(data=None):
    """
    python不支持相关java的数据类型，所以调整一下
    :param data:
    :return:
    """
    if not isinstance(data, str):
        data = str(data).replace('null', 'None').replace('true', 'True').replace('false', 'False')
    return data


def generate_id_card():
    """
    :return:返回身份证
    """
    fake = Faker("zh_CN")
    person_idcard = fake.ssn()
    setattr(ResultBase, 'person_idcard', person_idcard)
    return person_idcard


def generate_phone():
    """
    :return: 返回电话号码
    """
    fake = Faker("zh_CN")
    person_number = fake.phone_number()
    setattr(ResultBase, 'person_number', person_number)
    return person_number


def generate_name():
    """
    :return: 返回姓名
    """
    fake = Faker("zh_CN")
    person_name = fake.name()
    setattr(ResultBase, 'person_name', person_name)
    return person_name


def get_timestamp():
    """
    :return: 返回当前13位时间戳
    """
    timestamp = int(round(time.time() * 1000))
    setattr(ResultBase, 'timestamp', timestamp)
    return timestamp


def generate_title():
    """
    随机生成title
    """
    title = get_random_number("测试数据")
    setattr(ResultBase, 'title', title)


if __name__ == '__main__':
    # print(generate_name())
    # print(generate_id_card())
    # print(generate_phone())
    # print(get_sms_code())
    # print(generate_title())
    a = Faker()
    print(a.company())
