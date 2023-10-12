# -*- coding:utf-8 -*-
import sys
import os
import time

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import redis

from tools.LogTools import DoLogs

log = DoLogs(__name__)


class RedisTool:

    def __init__(self):
        st = time.time()
        self.r = redis.StrictRedis(host='175.178.190.236', port=6379, decode_responses=True)
        et = time.time()
        print("连接redis消耗时长{}".format(et - st))

    def set_data(self, msg):
        """
        向集合中添加元素
        :param msg: MQ消息中提取的消息ID
        :return:
        """
        self.r.expire("im_message_id_list", 600)
        self.r.sadd("im_message_id_list", msg)
        # log.mylog.info(f"--------redis存储的消息是：{msg}--------------")

    def check_data(self, msg):
        """
        检查消息ID是否在集合中
        :param msg: 消息接口响应获取的message_id
        :return:
        """
        st = time.time()
        result = self.r.sismember("im_message_id_list", msg)
        et = time.time()
        print("检查redis所消耗的时长{}".format(et - st))
        return result
        # return self.r.sismember("im_message_id_list", msg)


redis_obj = RedisTool()
# print(redis_obj.check_data(44492))
