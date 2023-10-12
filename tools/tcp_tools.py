import socket

from tools import constant
from tools.ConfTools import DoConf


class TcpTool:
    conf = DoConf(constant.globe_conf_dir)

    def __init__(self):
        # 创建套接字
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(
            (self.conf.get_value("data", "socket_servername"), int(self.conf.get_value("data", "socket_port"))))
        self.socket.settimeout(3)  # 设置3秒超时
        pass

    def __enter__(self):
        return self

    def send_msg(self, data):
        """
        发送消息
        :param data:
        :return:
        """
        self.socket.send(data)

    def get_msg(self, size):
        """
        获取消息
        :return:
        """
        return self.socket.recv(size)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        关闭socket连接
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.socket.close()
