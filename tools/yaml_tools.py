import os
import yaml
from tools.constant import case_data_dir
from tools.LogTools import DoLogs

log = DoLogs(__name__)


class HandleYaml:
    """
    处理yaml文档
    """

    def __init__(self, file_name: str) -> None:
        """
        初始化对象
        :param file_name: yaml文件名
        """
        self.file_path = os.path.join(case_data_dir, file_name)
        print('111', self.file_path)
        # 判断传入文件是否存在yaml_case_data文件夹中
        if not os.path.exists(self.file_path):
            log.mylog.error(self.file_path + " Not Found, Please check the file path")
            raise FileNotFoundError

    def get_data(self) -> dict:
        """
        获取yaml文档中的数据
        :return:yaml中的数据
        """
        with open(self.file_path, encoding='utf-8') as file:
            self.yaml_data = yaml.full_load(file)
        return self.yaml_data

    def yml_list(self):
        """
        将yml测试数据处理成列表
        pytest.mark.parametrize方法需传递列表
        :return:
        """
        yml_list = []
        # self.yaml_data


if __name__ == '__main__':
    data = HandleYaml("test.yml").get_data()
    print(data["test_case_01"])
