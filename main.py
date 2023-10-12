import pytest
from tools.constant import report_dir
from tools.send_feishu_notify import send_feishu_notify

pytest.main(['-s', r'--alluredir={}'.format(report_dir)])
# 如果在本地调试,则不需要调用发送结果报告
send_feishu_notify()
