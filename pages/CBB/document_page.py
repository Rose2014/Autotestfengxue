# -*- coding: utf-8 -*-
# @File    : document_page.py
# @Software: PyCharm
# @Desc:文档相关页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect
from config.global_vars import GLOBAL_VARS
from loguru import logger
import re
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage

class DocumentPage(BasePage):
    """
    文档相关页面
    """

    @allure.step("点击创建按钮")
    def click_create_button(self):
        """
        点击创建按钮
        :return:
        """
        locator_str_xpath = "//button[@businessname='文档创建']"
        self.click(locator_str_xpath)

    def wait_create_document_page_displayed(self):
        """
        等待创建文档页面显示
        :return:
        """
        locator_str_xpath = "//span[text()='主要内容源']"
        self.page.wait_for_selector(locator_str_xpath, state="visible")

    @allure.step("输入文档名称:{document_name}")
    def input_document_name(self, document_name: str):
        """
        输入文档名称
        :param document_name: 文档名称
        :return:
        """
        locator_str_xpath = "//input[@placeholder='请输入名称' and @app-name='CBB']"
        self.input(locator_str_xpath, document_name)

    @allure.step("选择主要内容源:{main_content_source_option}")
    def select_main_content_source(self, main_content_source_option: str):
        """
        选择主要内容源
        :param main_content_source: 主要内容源
        :return:
        """
        self.page.get_by_role("textbox", name="请填入请选择").click()
        self.page.get_by_role("listitem").filter(has_text=main_content_source_option).click()

    @allure.step("点击保存按钮")
    def click_save_button(self):
        """
        点击保存按钮
        :return:
        """
        locator_str_xpath = "//button/span[text()='保存']"
        self.click(locator_str_xpath)
