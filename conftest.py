import time

from tools.ConfTools import DoConf
from tools import constant

dc = DoConf(constant.globe_conf_dir)


def pytest_terminal_summary(terminalreporter):
    """
    统计运行信息,在邮件中显示
    :param terminalreporter: 内部使用的终端测试报告对象
    :return:
    """
    total = str(terminalreporter._numcollected)
    passed = str(len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown']))
    failed = str(len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown']))
    error = str(len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown']))
    skipped = str(len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown']))
    successful = str(
        "{:.2f}".format(len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100))
    # 运行总时长,terminalreporter._sessionstarttime 会话开始时间
    duration = str("{:.2f}".format(time.time() - terminalreporter._sessionstarttime))
    # 将测试结果写入ini配置文件中
    dc.set_value("test_result", "total", total)
    dc.set_value("test_result", "passed", passed)
    dc.set_value("test_result", "failed", failed)
    dc.set_value("test_result", "error", error)
    dc.set_value("test_result", "skipped", skipped)
    dc.set_value("test_result", "successful", successful)
    dc.set_value("test_result", "duration", duration)
