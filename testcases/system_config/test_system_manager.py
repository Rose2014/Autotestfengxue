# -*- coding: utf-8 -*-
# @File    : test_lotest_system_manager.py
# @Software: PyCharm
# @Desc:

# 标准库导入
from datetime import datetime
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from pages.login_page import LoginPage
from pages.systemmanager.system_manager_page import SystemManagerPage
from pages.panoramic_navigation_page import PanoramicNavigationPage
from config.global_vars import GLOBAL_VARS
from utils.data_utils.faker_handle import FakerData

@pytest.mark.system_manager
class TestSystemManager:
    """系统管理模块功能测试"""
    cases = {
        "create_user": [
            {
                "title": "系统管理员正确创建用户，密级：访客，License:否",
                "userId": "AutoTestUI"+datetime.now().strftime("%Y%m%d%H%M%S"),
                "userAccount": "AutoTestUI"+datetime.now().strftime("%Y%m%d%H%M%S"),
                "userCn":"AutoTestUI"+datetime.now().strftime("%Y%m%d%H%M%S"),
                "userEn":"AutoTestUI"+datetime.now().strftime("%Y%m%d%H%M%S"),
                "securityLevel":"访客",
                "mail":FakerData().generate_email(lan="en"),
                "phone":FakerData().generate_phone(lan="zh"),
                "license":"否",
                "run": True
            }
        ]
    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self, page: Page):
        logger.info("\n\n---------------Start: 开始测试-------------")
        users = {
            "login": GLOBAL_VARS['default_user_login'],
            "password": GLOBAL_VARS['default_user_password']
        }
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.is_login_page()
        login = users.get("login")
        password = users.get("password")
        login_page.login_on_page_flow(login, password)
        pn_page = PanoramicNavigationPage(page)
        pn_page.is_home_page()
        pn_page.click_panoramic_navigation_page_more()
        pn_page.click_panoramic_navigation_page_get_more()
        pn_page.click_navigation_sidebar("系统配置","系统管理")

        yield
        # 清除登录cookies，避免影响其他用例
        page.context.clear_cookies()
        logger.info("\n---------------End: 结束测试-------------\n\n")

    @pytest.mark.parametrize("case", cases["create_user"], ids=lambda x: x["title"])
    def test_system_manager_create_user(self,case, page: Page):
        """
        系统管理员进行系统初始化数据配置
        用户数据配置
        创建用户
        """
        system_manager_page = SystemManagerPage(page)
        system_manager_page.click_members()
        system_manager_page.click_create_user_btn()
        system_manager_page.is_create_user_dialog()
        userid = case.get("userId")
        system_manager_page.input_userid(userid)
        system_manager_page.input_user_account(case.get("userAccount"))
        system_manager_page.input_user_cn(case.get("userCn"))
        system_manager_page.input_user_en(case.get("userEn"))
        system_manager_page.input_user_mail(case.get("mail"))
        system_manager_page.select_security_level(case.get("securityLevel"))
        system_manager_page.input_user_phone(f"{case.get('phone')}")
        system_manager_page.select_user_license(case.get("license"))
        system_manager_page.click_ok_btn()
        page.wait_for_timeout(3000)
        system_manager_page.search_user(userid)
        page.wait_for_timeout(2000)
        system_manager_page.assert_user(userid)
        # system_manager_page.search_user("AutoTestUI20250822172901")
        # system_manager_page.assert_user("AutoTestUI20250822172901")
        page.wait_for_timeout(5000)


