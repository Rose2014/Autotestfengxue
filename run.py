# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @File    : run.py
# @Software: PyCharm
# @Desc: 框架主入口
"""
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python run.py  默认在test环境使用无头模式浏览器运行测试用例, 生成allure html report
  > python run.py -m demo 在test环境使用无头模式浏览器运行打了标记demo用例， 生成allure html report
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -browser webkit 使用webkit浏览器运行测试用例
  > python run.py -browser chromium webkit 使用chromium和webkit浏览器运行测试用例
  > python run.py -report=yes   生成allure html report
  > python run.py -mode=headed   使用有头模式运行
  > python run.py -env test -m 'projects or login' -report no -mode headless  在test环境，使用无头模式浏览器运行标记了project或者login的用例，并且生成allure html report
"""

# 标准库导入
import os
import argparse
# 第三方库导入
import pytest
from loguru import logger
# 本地应用/模块导入
from config.settings import LOG_INFO, RunConfig, ENV_VARS
from config.global_vars import GLOBAL_VARS
from config.path_config import REPORT_DIR, TRACING_DIR, CONF_DIR, ALLURE_RESULTS_DIR, ALLURE_HTML_DIR
from utils.report_utils.send_result_handle import send_result
from utils.logger_utils.loguru_log import capture_logs
from utils.report_utils.allure_handle import generate_allure_report


def run(**kwargs):
    try:
        # ------------------------ 捕获日志----------------------------
        capture_logs(log_info=LOG_INFO)

        logger.info("Starting Test")
        # ------------------------ 处理一下获取到的参数----------------------------
        logger.debug(f"run方法的入参：{kwargs}")
        env_key = kwargs.get("env", "") or None
        marks = kwargs.get("m", "") or None

        # 如果命令行没有传递browser， 默认使用RunConfig.browser的值
        browser = kwargs.get("browser", "") or None
        RunConfig.browser = browser if browser else RunConfig.browser

        # 如果命令行没有传递mode， 默认使用RunConfig.mode的值
        mode = kwargs.get("mode", "") or None
        RunConfig.mode = mode.lower() if mode else RunConfig.mode
        # ------------------------ 捕获日志----------------------------
        # ------------------------ 设置pytest相关参数 ------------------------
        arg_list = ["-vs", f"--maxfail={RunConfig.max_fail}", f"--reruns={RunConfig.rerun}",
                    f"--reruns-delay={RunConfig.reruns_delay}", f'--alluredir={ALLURE_RESULTS_DIR}',
                    '--clean-alluredir', f"--output={TRACING_DIR}"]

        if RunConfig.mode == "headed":
            arg_list.append("--headed")

        if isinstance(RunConfig.browser, list):
            for browser in RunConfig.browser:
                arg_list.append(f"--browser={browser.lower()}")
                # arg_list.extend(["--browser", f"{browser.lower()}"])

        if isinstance(RunConfig.browser, str):
            arg_list.append(f"--browser {RunConfig.browser.lower()}")

        if marks:
            arg_list.append(f"-m {marks}")
            # arg_list.extend(["-m", f"{marks}"])
        # ------------------------ 设置全局变量 ------------------------
        # 根据指定的环境参数，将运行环境所需相关配置数据保存到GLOBAL_VARS
        ENV_VARS["common"]["env"] = ENV_VARS[env_key]["host"]
        GLOBAL_VARS.update(ENV_VARS["common"])
        GLOBAL_VARS.update(ENV_VARS[env_key])
        # ------------------------ pytest执行测试用例 ------------------------
        logger.debug(f"pytest运行的参数：{arg_list}")
        pytest.main(args=arg_list)
        # ------------------------ 生成测试报告 ------------------------
        if kwargs.get("report") == "yes":
            report_path, attachment_path = generate_allure_report(allure_results=ALLURE_RESULTS_DIR,
                                                                  allure_report=ALLURE_HTML_DIR,
                                                                  windows_title=ENV_VARS["common"]["项目名称"],
                                                                  report_name=ENV_VARS["common"]["报告标题"],
                                                                  env_info={"运行环境": ENV_VARS["common"]["env"]},
                                                                  allure_config_path=os.path.join(CONF_DIR,
                                                                                                  "allure_config"),
                                                                  attachment_path=os.path.join(REPORT_DIR,
                                                                                               f'autotest_report.zip'))
            # ------------------------ 发送测试结果 ------------------------

            send_result(report_info=ENV_VARS["common"], report_path=report_path, attachment_path=attachment_path)
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="框架主入口")
    parser.add_argument("-env", default="test", help="输入运行环境：test 或 live")
    parser.add_argument("-m", help="选择需要运行的用例：python.ini配置的名称")
    parser.add_argument("-browser", nargs='*', help="浏览器驱动类型配置，支持如下类型：chromium, firefox, webkit")
    parser.add_argument("-mode", help="浏览器驱动类型配置，支持如下类型：headless, headed")
    parser.add_argument("-report", default="yes",
                        help="是否生成allure html report，支持如下类型：yes, no")
    args = parser.parse_args()
    run(**vars(args))

"""
pytest相关参数：以下也可通过pytest.ini配置
     --reruns: 失败重跑次数
     --reruns-delay 失败重跑间隔时间
     --count: 重复执行次数
    -v: 显示错误位置以及错误的详细信息
    -s: 等价于 pytest --capture=no 可以捕获print函数的输出
    -q: 简化输出信息
    -m: 运行指定标签的测试用例
    -x: 一旦错误，则停止运行
    --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
    "--reruns=3", "--reruns-delay=2"
    -s：这个选项表示关闭捕获输出，即将输出打印到控制台而不是被 pytest 截获。这在调试测试时很有用，因为可以直接查看打印的输出。

    --cache-clear：这个选项表示在运行测试之前清除 pytest 的缓存。缓存包括已运行的测试结果等信息，此选项可用于确保重新执行所有测试。

    --capture=sys：这个选项表示将捕获标准输出和标准错误输出，并将其显示在 pytest 的测试报告中。

    --self-contained-html：这个选项表示生成一个独立的 HTML 格式的测试报告文件，其中包含了所有的样式和资源文件。这样，您可以将该文件单独保存，在没有其他依赖的情况下查看测试结果。

    --reruns=0：这个选项表示在测试失败的情况下不重新运行测试。如果设置为正整数，例如 --reruns=3，会在测试失败时重新运行测试最多 3 次。

    --reruns-delay=5：这个选项表示重新运行测试的延迟时间，单位为秒。默认情况下，如果使用了 --reruns 选项，pytest 会立即重新执行失败的测试。如果指定了 --reruns-delay，pytest 在重新运行之前会等待指定的延迟时间。

    -p no:faulthandler 是 pytest 的命令行选项之一，用于禁用 pytest 插件 faulthandler。

    faulthandler 是一个 pytest 插件，它用于跟踪和报告 Python 进程中的崩溃和异常情况。它可以在程序遇到严重错误时打印堆栈跟踪信息，并提供一些诊断功能。

    使用 -p no:faulthandler 选项可以禁用 faulthandler 插件的加载和运行。这意味着 pytest 将不会使用该插件来处理和报告崩溃和异常情况。如果您确定不需要 faulthandler 插件的功能，或者遇到与其加载有关的问题，可以使用这个选项来禁用它。

    请注意，-p no:faulthandler 选项只会禁用 faulthandler 插件，其他可能存在的插件仍然会正常加载和运行。如果您想禁用所有插件，可以使用 -p no:all 选项。
    
    
    pytest-playwright 插件有3 个参数，可以在用例失败的时候调用。
        --tracing 是否为每个测试记录轨迹。on、off或retain-on-failure（默认值：off）。
        --video 是否为每次测试录制视频。on、off或retain-on-failure（默认值：off）。
        --screenshot 是否在每次测试后自动捕获屏幕截图。on、off或only-on-failure（默认值：off）。

 allure相关参数：
    –-alluredir这个选项用于指定存储测试结果的路径
    
-m标记：
    在pytest中，如果需要为-m参数传递多个值，可以使用以下方式：
    
    pytest -m "value1 and value2"
    这里使用双引号将多个值括起来，并使用and关键字连接它们。这将告诉pytest只运行标记为value1和value2的测试。
    
    如果你想要运行标记为value1或value2的测试，可以使用or关键字：
    
    pytest -m "value1 or value2"
    你还可以使用not关键字来排除某个标记。例如，下面的命令将运行除了标记为value1的所有其他测试：
    
    pytest -m "not value1"
    这样，你就可以根据需要在pytest中使用-m参数传递多个值，并根据标记运行相应的测试。
    

如何解决pytest参数化时出现的Unicode编码问题？
    这个问题的原因是Pytest默认将IDs视为ASCII字符串，并在测试报告中按原样显示。由于中文字符不属于ASCII字符范围，因此Pytest会将其转换为Unicode编码表示。

    解决方案:
    我们可以在pytest.ini文件中加上如下配置：disable_test_id_escaping_and_forfeit_all_rights_to_community_support = True

"""
