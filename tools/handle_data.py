
from jsonpath import jsonpath


def get_value(parameters: dict, key: str, index=None) -> any:
    """
    从Parameters中获取想要的值，当存在多个key时，可传入index指定获取哪个，会将响应体中的key对应的value存在列表keys中，顺序为从外到里
    :param parameters: dict字典数据
    :param key: 想要获取value的key
    :param index: 元素下标,从0开始
    :return: key对应的value元素
    """
    if isinstance(parameters, dict):
        keys = jsonpath(parameters, "$..{}".format(key))
        if keys is False:
            return "key:'{}' not in {}".format(key, parameters)
        elif len(keys) == 1:
            return keys[0]
        elif index is None and len(keys) != 1:
            return keys
        elif index is not None and len(keys) != 1:
            try:
                return keys[index]
            except IndexError as e:
                raise e
    else:
        return "The parameters type is not dict."


def get_yaml_test_data(one_case_data: dict) -> any:
    """
    处理每条用例读取后的数据
    :param one_case_data: 单条用例的全部数据,对用用例方法中接收的data
    :return: yaml用例文件中单个用例的用例名，路径，方法名，测试数据,预期结果
    使用：
    在测试用例中，通过parametrize进行参数化，“data”接收的是所有用例，test方法中传入的data接收的是单条用例，是get_yaml_test_data方法接收的参数
    例：
    @pytest.mark.parametrize("data", case_data["inquire"])
    def test(self, data):
        通过一行代码接收全部的参数
        case_name, uri, method, input_data, expected = get_yaml_test_data(data)
    如果需要对参数进行额外处理，则可以对input_data进行加工，如有多个预期结果，则需要分别取出
    """
    case_name = get_value(one_case_data, "case_name")
    uri = get_value(one_case_data, "uri")
    method = get_value(one_case_data, "method")
    input_data = get_value(one_case_data, "parameter")
    expected = get_value(one_case_data, "expected")
    return case_name, uri, method, input_data, expected
