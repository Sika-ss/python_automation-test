import json
import sys
import os
import time

from tools.mysql_tools import ConMysql
from tools.redis_tool import redis_obj
from operation.common.result_base import ResultBase
from operation.common.data_process import DataProcess

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import jsonpath
from tools.LogTools import DoLogs

log = DoLogs(__name__)


def check_code(func):
    """
    检查状态码
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        if args[1].status_code == 200:
            func(*args, **kwargs)
        elif args[1].status_code != 0:
            assert args[2][0]["expected_value"] == args[1].status_code
        else:
            # 匹配不上就不判断status_code
            pass

    return wrapper


class Mixins:

    @check_code
    def response_assert(self, result: object, validate):
        assert_list = DataProcess.handle_expected(validate)
        assert_list = assert_list
        if assert_list:
            for key in assert_list:
                condition = key.get('condition')  # 断言条件
                if condition != "mysql":
                    actual_value = jsonpath.jsonpath(json.loads(result.response),
                                                     key.get('actual_value'))  # 实际值的jsonpath表达式
                else:
                    actual_value = key.get('actual_value')
                expected_value = key.get('expected_value')  # 预期值
                try:
                    if condition == 'equal':
                        assert expected_value == actual_value[0]
                    elif condition == 'NotNone':
                        assert actual_value
                    elif condition == 'greater':
                        assert len(actual_value[0]) > expected_value
                    elif condition == 'MQ':
                        time.sleep(1)  # 等待3秒消费队列
                        actual_value = redis_obj.check_data(actual_value[0])
                        assert actual_value == expected_value
                    elif condition == 'mysql':
                        with ConMysql() as con_obj:
                            actual_value = con_obj.read_fetchone(actual_value)
                            for key, value in actual_value.items():
                                assert expected_value == value
                    else:
                        log.mylog.error("没有匹配对应条件")
                except (AssertionError, Exception) as e:
                    log.mylog.error(f"断言的类型{condition}，实际结果:{actual_value}，预期结果是:{expected_value}")
                    log.mylog.info("\n")
                    raise e

    def extraction(self, data: dict, response):
        """
        接口响应提取
        :param data:
        :param response:
        :return:
        """
        extraction = DataProcess.handle_extra(data)
        print(f"debug:{extraction}")
        key = None
        try:
            for key, value in extraction.items():
                setattr(ResultBase, key, jsonpath.jsonpath(json.loads(response), value)[0])
                log.mylog.info("提取的参数值为{}:{}".format(key, getattr(ResultBase, key)))
                log.mylog.info("\n")
        except Exception as e:
            log.mylog.info(f"提取{key}参数失败,报错如下{e.args}")
            log.mylog.info("\n")


mixins = Mixins()
