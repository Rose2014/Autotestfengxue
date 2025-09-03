# -*- coding: utf-8 -*-
# @File    : login_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
import allure
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage


class LoginPage(BasePage):
    # 网页登录，账号、密码、登录按钮定位
    locator_page_username = "[placeholder='请输入登录账号/工号/邮箱/手机号']"
    locator_page_password = "[placeholder='请输入密码']"
    locator_page_login_btn = "//button/span[contains(text(), '登录')] "
    #登录页标识
    locator_page_login_tip = "//h1[text()='登录']"
    # 密码错误提示语
    #locator_wrong_pwd_tip = ""

    @allure.step("访问登录页面：/erdc-login-erdcloud")
    def navigate(self):
        """
        访问登录页面
        """
        self.visit("#/erdc-login-erdcloud")

    def is_login_page(self):
        """
        确定是登录页面
        """
        self.is_element_visible(self.locator_page_login_tip)

    @allure.step("网页登录：输入用户名：{login}")
    def input_username_on_page(self, login):
        """
        网页登录：输入用户名
        """
        self.input(locator=self.locator_page_username, text=login)

    @allure.step("网页登录：输入密码：{password}")
    def input_password_on_page(self, password):
        """
        网页登录：输入密码
        """
        self.input(locator=self.locator_page_password, text=password)

    @allure.step("网页登录：点击【登录】按钮")
    def submit_login_on_page(self):
        """
        网页登录：点击登录按钮
        """
        self.click(locator=self.locator_page_login_btn)

    # --------------------- 流程 -------------------------------------
    @allure.step("网页登录：输入用户名：{login}，输入密码：{password}，点击【登录】按钮")
    def login_on_page_flow(self, login, password):
        """
        完整登录操作 --> 网页登录：输入用户名，密码，点击登录按钮
        """
        self.input_username_on_page(login)
        self.input_password_on_page(password)
        self.submit_login_on_page()
        self.page.wait_for_timeout(3000)
