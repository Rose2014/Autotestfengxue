# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息

# 标准库导入
import time
import os
from datetime import datetime
# 第三方库导入
from loguru import logger
import pytest
import allure
# 本地应用/模块导入
from config.path_config import REPORT_DIR
from config.global_vars import GLOBAL_VARS
from utils.data_utils.data_handle import data_handle

# 本地插件注册
pytest_plugins = ['plugins.pytest_playwright']  # noqa
"""
添加本地插件后需要在 pytest.ini 中禁用 pip 安装的 pytest-playwright 插件
[pytest]
addopts = -p no:playwright
"""


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        # 设置浏览器尺寸（browser_type_launch_args中参数"args": ["--start-maximized"]， 已开启全屏，则此处不需额外设置尺寸）
        # "viewport": RunConfig.window_size,
        "no_viewport": True,  # 与browser_type_launch_args中参数"args": ["--start-maximized"]配合使用。
        "record_video_size": {"width": 1920, "height": 1080},  # 录制视频尺寸
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """重写pytest_playwright夹具browser_type_launch_args，
        增加browser自定义启动参数"""
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"],  # 浏览器窗口最大化
        "devtools": False,
    }


# ------------------------------------- START: pytest钩子函数处理---------------------------------------#
def pytest_configure(config):
    """
    全局配置base_url
    """
    config.option.base_url = GLOBAL_VARS.get("host")


def pytest_runtest_call(item):  # noqa
    # 动态添加测试类的 allure.feature()， 注意测试类一定要写文档注释，否则这里会显示为空
    if item.parent._obj.__doc__:  # noqa
        allure.dynamic.feature(item.parent._obj.__doc__)  # noqa


def pytest_collection_modifyitems(config, items):
    """
    pytest_collection_modifyitems 是在用例收集完毕之后被调用，可以用来调整测试用例执行顺序；
        它有三个参数，分别是：

        session：会话对象；
        config：配置对象；
        items：用例对象列表；
        这三个参数分别有不同的作用，都可以拿来单独使用，修改用例执行顺序主要是使用 items 参数！
    """
    for item in items:
        # 注意这里的"case"需要与@pytest.mark.parametrize("case", cases)中传递的保持一致
        if "case" in item.fixturenames:
            case = item.callspec.params["case"]
            # 判断用例是否需要执行，如果不执行则跳过
            if not case.get("run"):
                item.add_marker(pytest.mark.skip(reason="用例数据中，标记了该用例为false，不执行"))
            # 对用例数据进行处理，将关键字${key}， 与全局变量GLOBAL_VARS中的值进行替换。例如${login}， 替换成GLOBAL_VARS["login"]的值。
            item.callspec.params["case"] = data_handle(case, GLOBAL_VARS)


def pytest_terminal_summary(terminalreporter, config):
    """
    收集测试结果
    """
    _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])
    try:
        # 获取pytest传参--reruns的值
        reruns_value = int(config.getoption("--reruns"))
        _RERUN = int(_RERUN / reruns_value)
    except Exception:
        reruns_value = "未配置--reruns参数"
        _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _XPASSED = len([i for i in terminalreporter.stats.get('xpassed', []) if i.when != 'teardown'])
    _XFAILED = len([i for i in terminalreporter.stats.get('xfailed', []) if i.when != 'teardown'])

    _TOTAL = terminalreporter._numcollected

    _DURATION = time.time() - terminalreporter._sessionstarttime

    session_start_time = datetime.fromtimestamp(terminalreporter._sessionstarttime)
    _START_TIME = f"{session_start_time.year}年{session_start_time.month}月{session_start_time.day}日 " \
                  f"{session_start_time.hour}:{session_start_time.minute}:{session_start_time.second}"

    test_info = f"各位同事, 大家好:\n" \
                f"自动化用例于 {_START_TIME}- 开始运行，运行时长：{_DURATION:.2f} s， 目前已执行完成。\n" \
                f"--------------------------------------\n" \
                f"#### 执行结果如下:\n" \
                f"- 用例运行总数: {_TOTAL} 个\n" \
                f"- 跳过用例个数（skipped）: {_SKIPPED} 个\n" \
                f"- 实际执行用例总数: {_PASSED + _FAILED + _XPASSED + _XFAILED} 个\n" \
                f"- 通过用例个数（passed）: {_PASSED} 个\n" \
                f"- 失败用例个数（failed）: {_FAILED} 个\n" \
                f"- 异常用例个数（error）: {_ERROR} 个\n" \
                f"- 重跑的用例数(--reruns的值): {_RERUN} ({reruns_value}) 个\n"
    try:
        _RATE = (_PASSED + _XPASSED) / (_PASSED + _FAILED + _XPASSED + _XFAILED) * 100
        test_result = f"- 用例成功率: {_RATE:.2f} %\n"
        logger.success(f"{test_info}{test_result}")
    except ZeroDivisionError:
        test_result = "- 用例成功率: 0.00 %\n"
        logger.critical(f"{test_info}{test_result}")

    # 这里是方便在流水线里面发送测试结果到钉钉/企业微信的
    with open(file=os.path.join(REPORT_DIR, "test_result.txt"), mode="w", encoding="utf-8") as f:
        f.write(f"{test_info}{test_result}")

# ------------------------------------- END: pytest钩子函数处理---------------------------------------#
