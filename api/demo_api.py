from operation.common.data_process import data_process
from tools import constant
from tools.ConfTools import DoConf
from tools.HttpRequest import SendRequest

conf = DoConf(constant.globe_conf_dir)
host = conf.get_value('data', 'admin_host')


class Demo(SendRequest):
    """
    Mock功能相关接口
    """

    def __init__(self):
        super(Demo, self).__init__()

    def add_demo(self, **kwargs):
        """
        添加数据
        :param kwargs:
        :return:
        """
        return self.post(f"{host}/create", **kwargs)

    def get_demo(self, **kwargs):
        """
        查询数据
        :param kwargs:
        :return:
        """
        return self.get(f"{host}/get", **kwargs)

    def update_demo(self, **kwargs):
        """
        更新数据
        :param kwargs:
        :return:
        """
        old_path = f"{host}/update/@@demo_id@@"
        new_path = data_process.handle_path(old_path)
        return self.delete(f"{new_path}", **kwargs)

    def delete_demo(self, **kwargs):
        """
        删除数据
        :param kwargs:
        :return:
        """
        old_path = f"{host}/delete/@@demo_id@@"
        new_path = data_process.handle_path(old_path)
        return self.delete(f"{new_path}", **kwargs)


demo_api = Demo()
