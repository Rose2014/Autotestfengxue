# -*- coding: utf-8 -*-
# @File    : product_manager_page.py
# @Software: PyCharm
# @Desc:产品管理页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect
from config.global_vars import GLOBAL_VARS
from loguru import logger
import re
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage

class ProductManagerPage(BasePage):
    """
    产品管理页面
    """

    @allure.step("搜索产品:{product_name}")
    def search_context(self, product_name: str):
        """
        搜索产品
        :param product_name: 产品名称
        :return:
        """
        self.input(self.page.get_by_role("textbox", name="输入名称关键字"), product_name)

    @allure.step("在上下文列表点击产品名称:{product_name}")
    def click_product_name_in_context(self, product_name: str):
        """
        在上下文列表点击产品名称
        :param product_name: 产品名称
        :return:
        """
        self.click(self.page.get_by_role("treeitem", name=product_name).locator("div").nth(1))

    @allure.step("点击二级菜单:{menu_name}")
    def click_level2_menu(self, menu_name: str):
        """
        点击二级菜单
        :param menu_name: 二级菜单名称
        :return:
        """
        self.click(self.page.get_by_text(menu_name, exact=True))
