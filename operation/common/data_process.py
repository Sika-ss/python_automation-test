import json
import struct
import sys
import os
from uuid import uuid4

from requests_toolbelt import MultipartEncoder

from operation.common import convert_json

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from tools import constant
from tools.LogTools import DoLogs
from tools.context import param_replace

log = DoLogs(__name__)


class DataProcess:

    @classmethod
    def handle_path(cls, url: str) -> str:
        """
        路径参数处理
        :param path_str: 带提取表达式的字符串 #host#/security/city/businessArea/updateById/#id#
        return  https://test-omsinfra.kfang.com/security/city/businessArea/updateById/1
        """
        url = param_replace(url)
        DoLogs(__name__).mylog.info(f'请求地址: {url}')
        return url

    @classmethod
    def handle_header(cls, header_str: dict, platform: str = None, url: str = None, data: dict = None) -> dict:
        """
        处理header，将相关签名的信息加入到请求头
        :param header_str: 用例栏中的header
        :param url: url
        :param data: 请求体
        :return: 返回完整的请求头
        """
        if header_str:
            header_str = param_replace(header_str)
            headers = eval(header_str)
            # if platform == 'online':
            #     headers = dict(header, **get_online_sign(url, data))  # 外网小程序签名逻辑
            # else:
            # if url.find(DoConf(constant.globe_conf_dir).get_value("data", "online_host")) != -1:
            #     headers = dict(header, **get_online_sign(url, data))  # 外网小程序签名逻辑
            # elif url.find('web-im-communication') != -1:  # IM接口的请求头不参与签名
            #     headers = header
            # elif url.find(DoConf(constant.globe_conf_dir).get_value("data", "host")) != -1:
            #     headers = dict(header, **get_sign(token=getattr(ExtractData, "token")))  #
            # elif url.find(DoConf(constant.globe_conf_dir).get_value("data", "host_coop")) != -1:
            #     headers = dict(header, **get_sign(token=getattr(ExtractData, "token")))
            # elif url.find(DoConf(constant.globe_conf_dir).get_value("data", "agent_host")) != -1:
            #     headers = dict(header, **get_sign(token=getattr(ExtractData, "token")))
            # else:  # openApi接口不参与签名
            #     headers = header
            # # DoLogs(__name__).mylog.info(f'请求头: {headers}')
            # headers = dict(header, **get_sign(token=getattr(ResultBase, "token")))  # 房客宝和OMS的签名逻辑
            return headers

    @classmethod
    def handle_data(cls, variable, sign: str = "YES") -> dict:
        """

        :param variable:
        :param sign:目前只有IM的签名在请求体里
        :return:
        """
        if variable:
            if sign == "YES":
                data = param_replace(variable)
                # variable = get_im_sign(data)
                # if url.find('web-im-communication') != -1 and title.find('腾讯回调函数') == -1:
                #     variable = get_im_sign(data)
                # else:
                #     variable = convert_json(data)
            else:
                data = param_replace(variable)
                variable = convert_json(data)
            return variable

    @classmethod
    def handle_files(cls, variable: str, headers: str) -> tuple:
        """
        文件上传的请求体参数处理
        :param variable: 请求体参数
        :param headers: 请求头
        :return:返回处理后的请求体和请求头元组
        """
        variable = eval(param_replace(variable))
        headers = eval(param_replace(headers))
        key = list(variable)[0]
        file_obj = MultipartEncoder(fields=dict(variable, **{
            key: (variable[key], open(os.path.join(constant.data_dir, variable[key]), 'rb'),
                  'text/plain')}),
                                    boundary=uuid4().hex)
        headers["Content-Type"] = file_obj.content_type
        return file_obj, headers

    @classmethod
    def handle_expected(cls, expected: str) -> dict:
        """
        处理接口断言的预期值
        :param expected:
        :return:
        """
        try:
            expected = eval(param_replace(expected))
        except Exception:
            DoLogs(__name__).mylog.info('空参数无法执行eval()')
        return expected

    @classmethod
    def handle_extra(cls, extraction: dict) -> dict:
        """
        处理需要进行接口传递的数据
        :param extraction:
        :return:
        """
        try:
            extraction = eval(param_replace(extraction))
        except Exception:
            DoLogs(__name__).mylog.info('空参数无法执行eval()')
        return extraction

    @classmethod
    def handle_sql(cls, sql: str) -> str:
        """
        处理sql数据
        :param sql:
        :return:
        """
        try:
            sql = param_replace(sql)
            sql = eval(sql)
        except Exception:
            DoLogs(__name__).mylog.info('参数替换失败')
        return sql

    @classmethod
    def tcp_handle_data(cls, variable, sign: str = "YES"):
        if sign == "YES":
            pass
        else:
            data = param_replace(variable)
            body = json.dumps(eval(data)).encode()
            header = struct.pack("<HH", len(body) + 4, 8192)
            res = header + body
            return res


data_process = DataProcess()
