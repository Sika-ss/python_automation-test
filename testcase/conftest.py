import os
import sys

from tools import constant
from tools.ConfTools import DoConf
from tools.HttpRequest import SendRequest
from tools.context import param_replace
from operation.common.data_process import data_process
from operation.common.mixins import mixins

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])

import pytest
from tools.LogTools import DoLogs

log = DoLogs(__name__)

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

conf = DoConf(constant.globe_conf_dir)
host = conf.get_value('data', 'host')


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的name和nodeid的中文显示在控制台上
    """
    for i in items:
        i.name = i.name.encode("utf-8").decode("unicode_escape")
        i._nodeid = i.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.fixture(scope="class")
def get_token():
    """
    获取token
    :return:
    """
    session = SendRequest()
    json = {"u": "@@account@@", "p": "@@pwd@@"}
    headers = {'Content-Type': 'application/json'}
    headers = data_process.handle_header(headers)
    json = eval(param_replace(json))
    res = session.post(f"{host}/auth", json=json, headers=headers)
    response_text = res.text
    if response_text:
        log.mylog.info("获取token ==>> 返回结果 ==>> {}".format(response_text))
        mixins.extraction({'token': '$.data'}, response_text)
