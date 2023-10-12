from websocket import create_connection

from operation.common.result_base import ResultBase
from tools import constant
from tools.ConfTools import DoConf


class WebsocketTool:
    conf = DoConf(constant.globe_conf_dir)

    def __init__(self, path):
        self.ws = create_connection(
            self.conf.get_value("data", "ws_host") + path + f"?token={getattr(ResultBase, 'token')}")
        self.ws.settimeout(3)  # 设置3秒超时

    def __enter__(self):
        return self

    def send_msg(self, data):
        """
        发送消息
        :param data:消息内容
        :return:
        """
        self.ws.send(data)

    def get_msg(self):
        """
        将websocket的消息返回
        :return:
        """
        return self.ws.recv()

    def get_connection_status(self):
        """
        获取连接状态
        :return:
        """
        return self.ws.getstatus()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭websocket
        self.ws.close()


if __name__ == '__main__':
    with WebsocketTool("/v2/stream") as ws:
        print(ws.get_connection_status())
