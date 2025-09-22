# -*- coding: utf-8 -*-
# @File    : system_manager_page.py
# @Software: PyCharm
# @Desc:流程模板页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect
from loguru import logger
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage

class FlowModulePage(BasePage):
    #流程模板页面字段定位
    locator_page_flow_template = "//div[text()='流程模板']"

    @allure.step("访问流程设计-流程模板页面：/biz-bpm/processManagement/template?_s=bpmProcessManagement")
    def navigate(self):
        """
        访问流程设计-流程模板页面
        """
        self.visit("#/biz-bpm/processManagement/template?_s=bpmProcessManagement")

    #流程模板页面字段定位
    locator_page_create_hover = "//span[@title='CBB']/parent::span"
    locator_page_create_module_button = "//span[@title='CBB']/following-sibling::*[1]/button/i"
    @allure.step("点击【CBB一层流程类型】的【+】按钮")
    def click_create_module_button(self):
        """
        创建流程模板类型
        """
        self.hover(self.locator_page_create_hover)
        self.click(self.locator_page_create_module_button)

    @allure.step("输入流程模板类型名称:{text}")
    def input_module_type_name(self,text:str):
        """
        输入流程模板类型名称
        """
        self.page.get_by_role("treeitem", name="ᚻ CBB").get_by_role("textbox").fill(text)
        self.page.get_by_role("treeitem", name="ᚻ CBB").get_by_role("textbox").press("Enter")
        self.page.wait_for_timeout(3000)

    @allure.step("删除流程类型:{module_type_name}")
    def delete_module_type(self,module_type_name:str):
        """
        删除流程模板类型
        """
        locator_str = "//span[@title='{}']/parent::span".format(module_type_name)
        self.hover(locator_str)
        self.page.get_by_role("button", name="ᚚ").click()
        self.page.get_by_role("button", name="确定").click()
        self.page.wait_for_timeout(3000)
    
    @allure.step("搜索流程类型:{module_type_name}")
    def search_module_type(self,module_type_name:str):
        """
        搜索流程模板类型
        """
        self.page.get_by_role("textbox", name="搜索关键字").fill(module_type_name)
        self.page.get_by_role("textbox", name="搜索关键字").press("Enter")
        self.page.wait_for_timeout(3000)
        count = self.page.get_by_text(module_type_name).count()
        logger.info("搜索到的流程类型数量是{}", count)

