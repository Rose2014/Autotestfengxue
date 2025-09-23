# -*- coding: utf-8 -*-
# @File    : system_manager_page.py
# @Software: PyCharm
# @Desc:流程模板页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect
from loguru import logger
import re
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
        self.page.wait_for_timeout(3000)

    #流程模板页面字段定位
    locator_page_create_hover = "//span[@title='CBB']/parent::span"
    locator_page_create_module_type_button = "//span[@title='CBB']/following-sibling::*[1]/button/i"
    @allure.step("点击【CBB一层流程类型】的【+】按钮")
    def click_create_module_type_button(self):
        """
        创建流程类型
        """
        self.hover(self.locator_page_create_hover)
        self.click(self.locator_page_create_module_type_button)  

    @allure.step("输入流程类型名称:{text}")
    def input_module_type_name(self,text:str):
        """
        输入流程类型名称
        """
        self.page.get_by_role("treeitem", name="ᚻ CBB").get_by_role("textbox").fill(text)
        self.page.get_by_role("treeitem", name="ᚻ CBB").get_by_role("textbox").press("Enter")
        self.page.wait_for_timeout(3000)

    @allure.step("删除流程类型:{module_type_name}")
    def delete_module_type(self,module_type_name:str):
        """
        删除流程类型
        """
        locator_str = "//span[@title='{}']/parent::span".format(module_type_name)
        self.hover(locator_str)
        self.page.get_by_role("button", name="ᚚ").click()
        self.page.get_by_role("button", name="确定").click()
        self.page.wait_for_timeout(3000)
    
    @allure.step("搜索流程类型:{module_type_name}")
    def search_module_type(self,module_type_name:str):
        """
        搜索流程类型
        """
        self.page.get_by_role("textbox", name="搜索关键字").fill(module_type_name)
        self.page.get_by_role("textbox", name="搜索关键字").press("Enter")
        self.page.wait_for_timeout(3000)
        count = self.page.get_by_text(module_type_name).count()
        logger.info("搜索到的流程类型数量是{}", count)
    

    @allure.step("点击流程类型:{module_type_name}")
    def click_module_type(self,module_type_name:str):
        """
        点击流程类型
        """
        locator_str = re.compile(r".*{}.*".format(module_type_name), re.IGNORECASE)
        allure.step("点击流程类型:{}".format(locator_str))
        self.page.get_by_text(locator_str).first.click()
        self.page.wait_for_timeout(3000)
    
    locator_page_create_module_button = "//button[text()='创建流程模板']"
    @allure.step("点击流程模板【创建】按钮")
    def click_create_flow_module_btn(self):
        """
        点击流程模板【创建】按钮
        """
        self.page.get_by_role("button", name="创建").click()
        self.page.wait_for_timeout(3000)

    def create_flow_module(self,module_name:str,module_id:str,module_desc:str,node_name:str,node_desc:str,node_flow_desc:str):
        """
        创建简单流程模板
        """
        self.click_create_flow_module_btn()
        self.page.wait_for_timeout(3000)
        self.input_flow_module_name(module_name)
        self.input_flow_module_id(module_id)
        self.input_flow_module_desc(module_desc)
        self.page.wait_for_timeout(3000)
        self.create_simple_flow_module(node_name,node_desc,node_flow_desc)


    @allure.step("输入流程模板名称:{text}")
    def input_flow_module_name(self,text:str):
        """
        输入流程模板名称
        """
        self.page.get_by_role("textbox", name="请输入").nth(2).fill(text)
    
    @allure.step("输入流程模板标识:{text}")
    def input_flow_module_id(self,text:str):
        """
        输入流程模板标识
        """
        self.page.get_by_role("textbox", name="请输入").nth(3).fill(text)
        self.page.wait_for_timeout(1500)
    
    @allure.step("输入流程模板描述:{text}")
    def input_flow_module_desc(self,text:str):
        """
        输入流程模板描述
        """
        self.page.wait_for_timeout(1500)
        self.page.locator("textarea").click()
        self.page.wait_for_timeout(3000)
        self.page.locator("textarea").fill(text)
        self.page.wait_for_timeout(1500)

    @allure.step("创建简单流程模板:节点名称:{nodeName},节点描述:{node_desc},节点流程指引:{flow_desc}")
    def create_simple_flow_module(self,nodeName:str,node_desc:str,flow_desc:str):
        """
        创建简单流程模板
        """
        
        allure.step("点击开始事件")
        self.page.get_by_title("创建开始事件").click()
        self.page.get_by_role("dialog", name="dialog").get_by_role("img").click()
        allure.step("点击追加任务")
        self.page.get_by_title("追加任务").click()
        self.page.wait_for_timeout(1500)
        allure.step("输入任务节点名称:{nodeName}")
        self.page.get_by_role("textbox", name="请填入名称").click()
        self.page.get_by_role("textbox", name="请填入名称").fill(nodeName)
        allure.step("输入任务节点描述:{node_desc}")
        self.page.get_by_role("textbox", name="请填入描述").click()
        self.page.wait_for_timeout(1500)
        self.page.get_by_role("textbox", name="请填入描述").fill(node_desc)
        allure.step("输入任务节点流程指引:{flow_desc}")
        self.page.get_by_role("textbox", name="请填入流程指引").click()
        self.page.wait_for_timeout(1500)
        self.page.get_by_role("textbox", name="请填入流程指引").fill(flow_desc)
        self.page.wait_for_timeout(1500)
        allure.step("点击追加结束事件")
        self.page.get_by_title("追加结束事件").dblclick()
        self.page.wait_for_timeout(3000)
        allure.step("点击【保存】按钮")
        self.page.get_by_role("button", name="保存").click()
        self.page.wait_for_timeout(1500)
        allure.step("点击【确定】按钮")
        self.page.get_by_role("button", name="确定").click()
        self.page.wait_for_timeout(5000)
    
    @allure.step("校验流程模板是否存在:{module_name}")
    def check_flow_module_exist(self,module_name:str):
        """
        校验流程模板是否存在
        """
        self.page.wait_for_timeout(1500)
        locator = self.page.get_by_role("cell", name=module_name).locator('span').first
        logger.info(f"--> 断言 | 流程模板存在 | 模板名称： {module_name}")
        expect(locator).to_be_visible()

    
    @allure.step("筛选流程模板版本状态:{state}")
    def filter_version_state(self,state:str):
        """
        筛选流程模板版本状态
        """
        self.page.get_by_role("cell", name="版本状态").get_by_role("emphasis").click()
        # self.page.get_by_role("cell", name="版本状态 Ჲ").get_by_role("emphasis").click()
        self.page.locator("#customSelect").get_by_role("textbox", name="请选择").click()
        self.page.get_by_role("list").get_by_text(state, exact=True).click()
        self.page.get_by_role("button", name="确定").click()
        self.page.wait_for_timeout(3500)

    @allure.step("搜索流程模板:{module_name}")
    def search_flow_module(self,module_name:str):
        """
        搜索流程模板
        """
        self.page.get_by_role("textbox", name="请输入", exact=True).click()
        self.page.get_by_role("textbox", name="请输入", exact=True).fill(module_name)
        self.page.get_by_role("textbox", name="请输入", exact=True).press("Enter")
        self.page.wait_for_timeout(3500)
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        elements = self.page.get_by_text(locator_str)
        assert elements.count() > 0, "未找到流程模板"

    @allure.step("禁用流程模板:{module_name}")
    def disable_flow_module(self,module_name:str):
        """
        禁用流程模板
        """
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        locator = self.page.get_by_text(locator_str).first
        module_name = locator.inner_text()
        self.page.get_by_role("rowgroup").filter(has_text=module_name).locator("button").first.click()
        self.page.wait_for_timeout(1000)
        self.page.get_by_text("禁用",exact=True).click()
        self.page.wait_for_timeout(1500)
        locator = self.page.get_by_role("rowgroup").filter(has_text=module_name).filter(has_text='已检入').filter(has_text='否')
        assert locator.count() > 0, "未找到禁用的流程模板"

    
    @allure.step("删除流程模板:{module_name}")
    def delete_flow_module(self,module_name:str):
        """
        删除流程模板
        """
