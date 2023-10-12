import time

import jenkins
import requests

from operation.config import conf


def send_feishu_notify() -> None:
    """
    发送报告至飞书
    :return:
    """
    try:
        jenkins_url = conf.get('jenkins_job_info', 'jenkins_url')
        job_name = conf.get('jenkins_job_info', 'job_name')
        jen = jenkins.Jenkins(jenkins_url)
        number = jen.get_job_info(job_name)['lastBuild']["number"]
        name = jen.get_job_info(job_name)["displayName"]
        url = jen.get_job_info(job_name)['lastBuild']["url"]
        allure_url = url + "allure/"
        # 飞书机器人url
        webhook_url = conf.get("feishu_hook", "webhook")
        # result
        total = conf.get("test_result", "total")
        passed = conf.get("test_result", "passed")
        failed = conf.get("test_result", "failed")
        error = conf.get("test_result", "error")
        skipped = conf.get("test_result", "skipped")
        successful = conf.get("test_result", "successful")
        duration = conf.get("test_result", "duration")

        # 发送飞书通知
        currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        method = "post"
        headers = {
            'Content-Type': 'application/json'
        }
        json = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True,
                    "enable_forward": True
                },
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": F"运行时间: {currenttime}\n构建次数: {number}\n总用例数为: {total}\n通过用例数: {passed}\n失败用例数: {failed}\n错误用例数: {error}\n跳过用例数: {skipped}\n通过率为: {successful} %\n耗时: {duration} s",
                        "tag": "lark_md"
                    }
                }
                    , {
                        "actions": [{
                            "tag": "button",
                            "text": {
                                "content": "查看测试报告",
                                "tag": "lark_md"
                            },
                            "url": allure_url,
                            "type": "default",
                            "value": {}
                        }],
                        "tag": "action"
                    }],
                "header": {
                    "title": {
                        "content": "Trading System 测试报告",
                        "tag": "plain_text"
                    }
                }
            }
        }
        requests.request(method=method, url=webhook_url, headers=headers, json=json)
    except Exception as e:
        raise e


if __name__ == '__main__':
    send_feishu_notify()
