# -*- coding:utf-8 -*-
import json
import sys, os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import pika
from tools.redis_tool import redis_obj
from tools.LogTools import DoLogs
from tools.constant import globe_conf_dir
from tools.ConfTools import DoConf

cfg = DoConf(globe_conf_dir)
log = DoLogs(__name__)


def callback(ch, method, properties, body):
    res = json.loads(body.decode('utf-8'))
    # log.mylog.info(f"---------------监听获取的消息为：{res}------------------")
    msg_id = res["msgId"]
    redis_obj.set_data(msg_id)


class RabbitMq:

    def __init__(self):
        log.mylog.info("----------------开始初始化--------------")
        self.credentials = pika.PlainCredentials(cfg.get_value('mq_data', 'mq_username'),
                                                 cfg.get_value('mq_data', 'mq_pwd'))  # 登录RabbitMQ后台
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(cfg.get_value('mq_data', 'mq_host'), 5672, '/', self.credentials,
                                      connection_attempts=3, retry_delay=3))  # 创建连接，每隔三秒连接一次最多三次
        self.channel = self.connection.channel()  # 创建信道
        log.mylog.info("----------------初始化完成--------------")

    def producer(self, queue, content):
        """
        rabbitMQ发送消息
        :param queue:队列名
        :param content:消息内容
        :return:
        """
        try:
            self.channel.queue_declare(queue=queue, durable=True)  # 声明队列
            self.channel.basic_publish(exchange='', routing_key=queue, body=bytes(str(content), encoding="utf8"))
            log.mylog.info("消息发送成功")
        except Exception:
            log.mylog.error("消息发生失败")

    def consumer(self):
        """
        消费消息
        :return:
        """
        # exchange = cfg.get_value("mq_data", "im_exchange")
        # result = self.channel.queue_declare(queue='test_cx', exclusive=True)
        # queue_name = result.method.queue
        # self.channel.queue_bind(exchange=exchange, queue='test_cx')  # 绑定到队列
        self.channel.basic_consume('test_cx', on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()


if __name__ == '__main__':
    mq = RabbitMq()  # 创建MQ对象
    mq.consumer()
