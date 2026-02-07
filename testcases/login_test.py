#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : login_test.py
# @Software: PyCharm
# @Desc: 登录页面测试用例

# 第三方库导入
import pytest
import allure
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from config.settings import RunConfig
from pages.login_page import LoginPage
from utils.data_utils.excel_handle import ExcelHandle


@allure.epic("登录模块")
class TestLoginPage:
    """
    登录页面用例
    """
    cases = ExcelHandle().read_excel_file(__file__)
    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self, page: Page):
        logger.info("\n---------------Start: 开始测试-------------\n")
        page.set_viewport_size(RunConfig.window_size)
        self.page = page
        self.login_page = LoginPage(self.page)
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @allure.story("打开登录页")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("case", cases["test_001_open_login_page"], ids=lambda x: x["用例标题"])
    def test_001_open_login_page(self, case):
        """
        打开登录页面并检查页面元素
        """
        self.login_page.navigate()
        self.login_page.is_login_page()

    @allure.story("登录成功")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("case", cases["test_002_login_success"], ids=lambda x: x["用例标题"])
    def test_002_login_success(self, case):
        """
        使用默认账号登录并校验进入主页面
        """
        login = case.get("账号")
        password = case.get("密码")
        assert login and password, "用例数据未提供账号或密码"
        self.login_page.navigate()
        self.login_page.is_login_page()
        self.login_page.login_on_page_flow(login, password)
        self.login_page.is_home_page()
