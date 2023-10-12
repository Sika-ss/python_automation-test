from api.demo_api import demo_api
from operation.common.mixins import mixins
from tools import constant
from tools.ConfTools import DoConf
from tools.LogTools import DoLogs
from operation.common.data_process import data_process
from operation.common.result_base import ResultBase
import json
import jsonpath

log = DoLogs(__name__)


class DemoService:
    def __init__(self):
        self.result = ResultBase()
        self.conf = DoConf(constant.globe_conf_dir)

    def add_demo(self, data: dict, extraction: dict = None):
        """
        新增demo
        :param data:
        :param extraction:
        :return:
        """
        headers = {"Content-Type": "application/json"}
        headers = data_process.handle_header(headers)
        variable = data_process.handle_data(data, sign="NO")
        res = demo_api.add_demo(json=variable, headers=headers)
        response_text = res.text
        log.mylog.info(
            "新增xxxxxx ==>> 接口状态码 {}==>> 返回结果 ==>> {}".format(res.status_code, response_text))
        self.result.status_code = res.status_code
        self.result.success = False
        if response_text:
            self.result.success = True
            if extraction:
                mixins.extraction(extraction, response_text)
        else:
            self.result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.status_code, response_text)
        self.result.response = response_text

        return self.result

    def get_demo_list(self, data: dict, extraction: dict = None):
        """
        获取标准品种列表
        :param data:
        :param extraction:
        :return:
        """
        headers = {}
        headers = data_process.handle_header(headers)
        variable = data_process.handle_data(data, sign="NO")
        res = demo_api.get_demo(params=variable, headers=headers)
        response_text = res.text
        log.mylog.info(
            "获取xxxxxx列表 ==>> 接口状态码 {}==>> 返回结果 ==>> {}".format(res.status_code, response_text))
        self.result.success = False
        self.result.status_code = res.status_code
        if response_text:
            self.result.success = True
            if extraction:
                mixins.extraction(extraction, response_text)
                self.conf.set_value("data", "demo_id",
                                    jsonpath.jsonpath(json.loads(response_text), "$.data.data[*].id")[0])
        else:
            self.result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["status"], res.json()["message"])
        self.result.response = response_text
        return self.result

    def update_demo(self, data: dict, extraction: dict = None):
        """
        更新demo
        :param data:
        :param extraction:
        :return:
        """
        headers = {"Content-Type": "application/json"}
        headers = data_process.handle_header(headers)
        variable = data_process.handle_data(data, sign="NO")
        res = demo_api.update_demo(json=variable, headers=headers)
        response_text = res.text
        log.mylog.info(
            "更新xxxx ==>> 接口状态码 {}==>> 返回结果 ==>> {}".format(res.status_code, response_text))
        self.result.success = False
        self.result.status_code = res.status_code
        if response_text:
            self.result.success = True
            if extraction:
                mixins.extraction(extraction, response_text)
        else:
            self.result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["status"], res.json()["message"])
        self.result.response = response_text
        return self.result

    def delete_demo(self, data: dict, extraction: dict = None):
        """
        删除demo
        :param data:
        :param extraction:
        :return:
        """
        headers = {}
        headers = data_process.handle_header(headers)
        variable = data_process.handle_data(data, sign="NO")
        res = demo_api.delete_demo(json=variable, headers=headers)
        response_text = res.text
        log.mylog.info(
            "删除标准品种 ==>> 接口状态码 {}==>> 返回结果 ==>> {}".format(res.status_code, response_text))
        self.result.success = False
        self.result.status_code = res.status_code
        if response_text:
            self.result.success = True
            if extraction:
                mixins.extraction(extraction, response_text)
        else:
            self.result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json()["status"], res.json()["message"])
        self.result.response = response_text
        return self.result


demo_service = DemoService()
