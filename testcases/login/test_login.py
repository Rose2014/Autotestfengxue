# -*- coding: utf-8 -*-
# @File    : test_login.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from pages.login_page import LoginPage


@pytest.mark.login
class TestLogin:
    """登录测试"""
    cases = {
        "user_with_account": [
            {"title": "正确账号和密码登录成功", "login": "${default_user_login}",
             "password": "${default_user_password}", "run": True}
        ]
    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self, page: Page):
        logger.info("\n\n---------------Start: 开始测试-------------")
        self.login_page = LoginPage(page)
        self.login_page.navigate()
        self.login_page.is_login_page()
        yield
        # 清除登录cookies，避免影响其他登录用例
        page.context.clear_cookies()
        logger.info("\n---------------End: 结束测试-------------\n\n")

    @pytest.mark.parametrize("case", cases["user_with_account"], ids=lambda x: x["title"])
    def test_login_by_user_with_account(self, case,page:Page):
        """
        正确账号和密码登录成功
        """
        login = case.get("login")
        password = case.get("password")
        LoginPage(page).login_on_page_flow(login,password)

        logger.info("\n---------------: 登录测试结束-------------\n\n")



