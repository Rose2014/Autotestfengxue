# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @File    : settings.py
# @Software: PyCharm
# @Desc: 项目配置文件
# 标准库导入
import os
# 本地应用/模块导入
from config.path_config import LOG_DIR

# ------------------------------------ 测试数据配置 ----------------------------------------------------#
ENV_VARS = {
    "common": {
        "报告标题": "UI自动化测试报告",
        "项目名称": "ERTX易特克思",
        "tester": "终验测试组",
        "department": "产品管理中心",
        "env": "live"
    },
    "test": {
        # 测试环境域名
        "host": "http://erdcloud-plat-web-erdcloud-plm-4.szcp.ddns.e-lead.cn/",
        # 密码加密的密钥
        "ace_key": "",
        "default_user_login": "erdcadmin",
        "default_user_password": "Pw!123456",
    },
    "live": {
        # 测试环境域名
        "host": "http://cbb-sit-1.apps.paas.szcp.ddns.e-lead.cn/",
        # 密码加密的密钥
        "ace_key": "",
        # 默认测试账号
        "default_user_login": "erdcadmin",
        "default_user_password": "Pw!123456",
    }
}


# ------------------------------------ pytest相关配置 ----------------------------------------------------#
class RunConfig:
    """
    运行测试配置
    """
    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = ["chromium"]

    # 运行模式（headless, headed）
    mode = "headed"

    # 窗口大小
    """
    playwright 默认启动的浏览器窗口大小是1280x720， 我们可以通过设置no_viewport参数来禁用固定的窗口大小 ，no_viewport 禁用窗口大小。
    """
    # 这个标识根据具体尺寸设置窗口大小. 如果已使用：browser_type_launch_args "args": ["--start-maximized"]， 则此处配置不生效
    window_size = {"width": 1920, "height": 1080}

    # 浏览器页面
    page = None

    # 失败重跑次数
    rerun = 0

    # 失败重跑间隔时间
    reruns_delay = 5

    # 当达到最大失败数，停止执行
    max_fail = "10"


# ------------------------------------ 配置信息 ----------------------------------------------------#
# 0表示默认不发送任何通知， 1 代表钉钉通知，2 代表企业微信通知， 3 代表邮件通知， 4 代表所有途径都发送通知
SEND_RESULT_TYPE = 0

# 指定日志收集级别和日志文件路径
LOG_INFO = [
    {"level": "INFO", "filename": os.path.join(LOG_DIR, "service_info.log")},
    # {"level": "TRACE", "filename": os.path.join(LOG_DIR, "service_full.log")}
]
"""
支持的日志级别：
    TRACE: 最低级别的日志级别，用于详细追踪程序的执行。
    DEBUG: 用于调试和开发过程中打印详细的调试信息。
    INFO: 提供程序执行过程中的关键信息。
    SUCCESS: 用于标记成功或重要的里程碑事件。
    WARNING: 表示潜在的问题或不符合预期的情况，但不会导致程序失败。
    ERROR: 表示错误和异常情况，但程序仍然可以继续运行。
    CRITICAL: 表示严重的错误和异常情况，可能导致程序崩溃或无法正常运行。
"""

# ------------------------------------ 邮件配置信息 ----------------------------------------------------#

# 发送邮件的相关配置信息
email = {
    "user": "liangwx@e-lead.cn",  # 发件人邮箱
    "password": "Elead202509@",  # 发件人邮箱授权码
    "host": "mail.e-lead.cn",
    "to": ['liangwx@e-lead.cn']  # 收件人邮箱
}

# ------------------------------------ 邮件通知内容 ----------------------------------------------------#
email_subject = f"UI自动化报告"
email_content = """
           各位同事, 大家好:

           自动化用例于${start_time}开始运行，运行时长：${run_time}s， 目前已执行完成。
           ---------------------------------------------------------------------------------------------------------------
           测试部门：${tester}
           所属部门：${department}
           项目环境：${env}
           ---------------------------------------------------------------------------------------------------------------
           执行结果如下:
           用例运行总数: ${total} 个
           成功率:  ${pass_rate} %
           通过用例个数（passed）:  ${passed} 个
           失败用例个数（failed）:  ${failed} 个
           异常用例个数（error）:   ${broken} 个
           跳过用例个数（skipped）: ${skipped}个
           

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 钉钉相关配置 ----------------------------------------------------#
ding_talk = {
    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=********",
    "secret": "****ding****"
}

# ------------------------------------ 钉钉通知内容 ----------------------------------------------------#
ding_talk_title = f"UI自动化报告"
ding_talk_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
            ---------------------------------------------------------------------------------------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${env} 
           ---------------------------------------------------------------------------------------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）: ${passed} 个
           - 失败用例个数（failed）: ${failed} 个
           - 异常用例个数（error）: ${broken} 个
           - 跳过用例个数（skipped）: ${skipped} 个
           - 失败重试用例个数 * 次数之和（rerun）: ${rerun} 个
           - 成  功   率: ${pass_rate} %

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
wechat = {
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=********",
}
# ------------------------------------ 企业微信通知内容 ----------------------------------------------------#
wechat_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
           --------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${env} 
           --------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）:<font color=\"info\"> ${passed} 个</font>
           - 失败用例个数（failed）: <font color=\"warning\"> ${failed}  个</font>
           - 异常用例个数（error）: <font color=\"warning\"> ${broken} 个</font>
           - 跳过用例个数（skipped）: <font color=\"comment\"> ${skipped} 个</font>
           - 失败重试用例个数 * 次数之和（rerun）: <font color=\"comment\"> ${rerun} 个</font>
           - 成  功   率: <font color=\"info\"> ${pass_rate} % </font>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
