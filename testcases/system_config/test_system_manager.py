# -*- coding: utf-8 -*-
# @File    : test_system_manager.py
# @Software: PyCharm
# @Desc:系统管理-部门-创建用户

# 标准库导入
import time
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from pages.system_manager.system_manager_page import SystemManagerPage
from utils.data_utils.faker_handle import FakerData

@pytest.mark.system_manager
class TestSystemManager:
    """系统管理模块功能测试"""
    cases = {
        "create_user": [
            {
                "title": "系统管理员正确创建用户，密级：访客，License:否",
                "userId": f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}1",
                "userAccount": f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}1",
                "userCn":f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}1",
                "userEn":f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}1",
                "securityLevel":"访客",
                "mail":FakerData().generate_email(lan="en"),
                "phone":FakerData().generate_phone(lan="zh"),
                "license":"否",
                "run": True
            },
            {
                "title": "系统管理员正确创建用户，密级：内部，License:是",
                "userId": f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}2",
                "userAccount": f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}2",
                "userCn":f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}2",
                "userEn":f"AutoTestUI{time.strftime('%Y%m%d%H%M%S')}2",
                "securityLevel":"访客",
                "mail":FakerData().generate_email(lan="en"),
                "phone":FakerData().generate_phone(lan="zh"),
                "license":"否",
                "run": True
            }
        ]
    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        logger.info("\n---------------Start: 开始测试-------------\n")
        self.user_page = user_page
        self.system_manager_page = SystemManagerPage(self.user_page)
        self.system_manager_page.navigate()
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @pytest.mark.parametrize("case", cases["create_user"], ids=lambda x: x["title"])
    def test_system_manager_create_user(self, case):
        """
        系统管理员进行系统初始化数据配置
        用户数据配置
        创建用户
        """
        self.system_manager_page.click_members()
        self.system_manager_page.click_create_user_btn()
        self.system_manager_page.is_create_user_dialog()
        userid = case.get("userId")
        self.system_manager_page.input_userid(userid)
        self.system_manager_page.input_user_account(case.get("userAccount"))
        self.system_manager_page.input_user_cn(case.get("userCn"))
        self.system_manager_page.input_user_en(case.get("userEn"))
        self.system_manager_page.input_user_mail(case.get("mail"))
        self.system_manager_page.select_security_level(case.get("securityLevel"))
        self.system_manager_page.input_user_phone(f"{case.get('phone')}")
        self.system_manager_page.select_user_license(case.get("license"))
        self.system_manager_page.click_ok_btn()
        self.user_page.wait_for_timeout(3000)
        self.system_manager_page.search_user(userid)
        self.user_page.wait_for_timeout(2000)
        self.system_manager_page.assert_user(userid)
        self.user_page.wait_for_timeout(5000)


