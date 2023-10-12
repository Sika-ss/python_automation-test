# -*- coding:utf-8 -*-
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import requests

from tools.LogTools import DoLogs

log = DoLogs(__name__)


class SendRequest:

    def __init__(self):
        self.session = requests.sessions.session()

    def get(self, url, **kwargs):
        return self.http_request(url, "GET", **kwargs)

    def post(self, url, **kwargs):
        return self.http_request(url, "POST", **kwargs)

    def put(self, url, **kwargs):
        return self.http_request(url, "PUT", **kwargs)

    def delete(self, url, **kwargs):
        return self.http_request(url, "DELETE", **kwargs)

    def http_request(self, url, method, **kwargs):
        self.request_log(url, method, **kwargs)
        if method == 'GET':
            return self.session.request(method, url, **kwargs)
        if method == 'PUT':
            return self.session.request(method, url, **kwargs)
        if method == 'POST':
            return self.session.request(method, url, **kwargs)
        if method == 'DELETE':
            return self.session.request(method, url, **kwargs)

    def request_log(self, url, method, params=None, data=None, json=None, headers=None):
        log.mylog.info("接口请求地址 ==>> {}".format(url))
        log.mylog.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        log.mylog.info("接口请求头 ==>> {}".format(headers))
        if params:
            log.mylog.info("接口请求 params 参数 ==>> {}".format(params))
        elif data:
            log.mylog.info("接口请求体 data 参数 ==>> {}".format(data))
        elif json:
            log.mylog.info("接口请求体 json 参数 ==>> {}".format(json))
        else:
            log.mylog.info("接口请求体参数为空")
