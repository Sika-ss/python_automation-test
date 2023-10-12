import allure
import pytest as pytest

from operation.common.mixins import mixins
from operation.demo_api_controller import demo_service
from tools.LogTools import DoLogs
from tools.yaml_tools import HandleYaml

data = HandleYaml("test.yml").get_data()

log = DoLogs(__name__)

pytestmark = pytest.mark.all


@allure.severity(allure.severity_level.NORMAL)
@allure.epic("针对Demo功能的测试")
class TestDemo:

    @allure.story("接口1--新增xxxx")
    @allure.title("新增xxxxx--{title}")
    @pytest.mark.symbol
    @pytest.mark.parametrize("title, data, validate", data["create_demo"])
    @pytest.mark.run(order=1)
    def test_add_demo(self, title, data, validate):
        log.mylog.info("*************** 开始执行用例 ***************")
        result = demo_service.add_demo(data)
        mixins.response_assert(result, validate)  # 进行断言
        log.mylog.info("*************** 结束执行用例 ***************")

    @allure.story("接口2--查询zzz")
    @allure.title("查询zzzz--{title}")
    @pytest.mark.symbol
    @pytest.mark.parametrize("title, data, validate,extraction", data["get_demo"])
    @pytest.mark.run(order=2)
    def test_get_core_symbol_list(self, title, data, validate, extraction):
        log.mylog.info("*************** 开始执行用例 ***************")
        result = demo_service.get_demo_list(data, extraction)
        mixins.response_assert(result, validate)  # 进行断言
        log.mylog.info("*************** 结束执行用例 ***************")

    @allure.story("接口2--更新xxxxxx")
    @allure.title("更新xxxx--{title}")
    @pytest.mark.symbol
    @pytest.mark.parametrize("title, data, validate", data["update_demo"])
    @pytest.mark.run(order=2)
    def test_update_core_symbol(self, title, data, validate):
        log.mylog.info("*************** 开始执行用例 ***************")
        result = demo_service.update_demo(data)
        mixins.response_assert(result, validate)  # 进行断言
        log.mylog.info("*************** 结束执行用例 ***************")

    @allure.story("接口3--删除xxxx")
    @allure.title("删除xxxx--{title}")
    @pytest.mark.symbol
    @pytest.mark.parametrize("title, data, validate", data["delete_demo"])
    @pytest.mark.run(order=3)
    def test_delete_core_symbol(self, title, data, validate):
        log.mylog.info("*************** 开始执行用例 ***************")
        result = demo_service.delete_demo(data)
        mixins.response_assert(result, validate)  # 进行断言
        log.mylog.info("*************** 结束执行用例 ***************")
