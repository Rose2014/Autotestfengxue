# -*- coding: utf-8 -*-
# @File    : flow_module_page.py
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
    #流程模板页面字段定位
    locator_page_create_hover = "//span[@title='公共构建模块']/parent::span"
    locator_page_create_module_type_button = "//span[@title='公共构建模块']/following-sibling::*[1]/button/i"

    @allure.step("访问流程设计-流程模板页面：/biz-bpm/processManagement/template?_s=bpmProcessManagement")
    def navigate(self):
        """
        访问流程设计-流程模板页面
        """
        self.visit("/#/biz-bpm/processManagement/template?_s=bpmProcessManagement")

    @allure.step("点击【公共构建模块一层流程类型】的【+】按钮")
    def click_create_module_type_button(self):
        """
        点击【公共构建模块一层流程类型】的【+】按钮
        """
        self.hover(self.locator_page_create_hover)
        self.click(self.locator_page_create_module_type_button)

    @allure.step("输入流程类型名称:{text}")
    def input_module_type_name(self,text:str):
        """
        输入流程类型名称
        """
        locator = self.page.get_by_role("treeitem", name="ᚻ 公共构建模块").get_by_role("textbox")
        self.input(locator,text)
        self.press(locator,"Enter")
        # self.page.wait_for_timeout(3000)

    @allure.step("删除流程类型:{module_type_name}")
    def delete_module_type(self,module_type_name:str):
        """
        删除流程类型
        """
        locator_str = "//span[@title='{}']/parent::span".format(module_type_name)
        self.hover(locator_str)
        logger.info(f"点击流程类型【{module_type_name}】的【删除】图标")
        self.click(self.page.get_by_role("button", name="ᚚ"))
        logger.info("点击删除流程类型二次确认的【确定】按钮")
        self.click(self.page.get_by_role("button", name="确 定"))
        # self.page.wait_for_timeout(3000)
    
    @allure.step("搜索流程类型:{module_type_name}")
    def search_module_type(self,module_type_name:str):
        """
        搜索流程类型
        """
        locator = self.page.get_by_role("textbox", name="搜索关键字")
        self.input(locator,module_type_name)
        self.press(locator,"Enter")
        # self.page.wait_for_timeout(3000)
        count = self.page.get_by_text(module_type_name).count()
        logger.info("搜索到的流程类型数量是{}", count)
    

    @allure.step("点击流程类型:{module_type_name}")
    def click_module_type(self,module_type_name:str):
        """
        点击流程类型
        """
        locator_str = re.compile(r".*{}.*".format(module_type_name), re.IGNORECASE)
        logger.info(f"点击流程类型：{locator_str}")
        self.click(self.page.get_by_text(locator_str).first)
        # self.page.wait_for_timeout(3000)
    
    @allure.step("点击流程模板【创建】按钮")
    def click_create_flow_module_btn(self):
        """
        点击流程模板【创建】按钮
        """
        locator = self.page.get_by_role("button", name="创建")
        self.click(locator)
        # self.wait_for_load_state("networkidle")

    def create_flow_module(self,module_name:str,module_id:str,module_desc:str,node_name:str,node_desc:str,node_flow_desc:str):
        """
        创建简单流程模板
        """
        self.click_create_flow_module_btn()
        self.input_flow_module_name(module_name)
        self.input_flow_module_id(module_id)
        self.input_flow_module_desc(module_desc)
        self.create_simple_flow_module(node_name,node_desc,node_flow_desc)


    @allure.step("输入流程模板名称:{text}")
    def input_flow_module_name(self,text:str):
        """
        输入流程模板名称
        """
        logger.info(f"输入流程模板名称：{text}")
        self.page.wait_for_selector("//div[text()='基础配置']",state="visible",timeout=10000)
        self.input(self.page.get_by_role("textbox", name="请输入").nth(2),text)
        # self.wait(1)
    
    @allure.step("输入流程模板标识:{text}")
    def input_flow_module_id(self,text:str):
        """
        输入流程模板标识
        """
        logger.info(f"输入流程模板标识：{text}")
        self.input(self.page.get_by_role("textbox", name="请输入").nth(3),text)
        self.wait(2)
    
    @allure.step("输入流程模板描述:{text}")
    def input_flow_module_desc(self,text:str):
        """
        输入流程模板描述
        """
        self.wait(1)
        self.clear(self.page.locator("textarea"))
        self.wait(1)
        logger.info(f"输入流程模板描述：{text}")
        self.input(self.page.locator("textarea"),text)
        self.wait(1)

    @allure.step("创建简单流程模板:节点名称:{nodeName},节点描述:{node_desc},节点流程指引:{flow_desc}")
    def create_simple_flow_module(self,nodeName:str,node_desc:str,flow_desc:str):
        """
        创建简单流程模板
        """
        logger.info("点击开始事件")
        self.click(self.page.get_by_title("创建开始事件"))
        self.click(self.page.get_by_role("dialog", name="dialog").get_by_role("img"))
        self.wait(1)
        logger.info("点击追加任务")
        self.click(self.page.get_by_title("追加任务"))
        self.wait(1)
        logger.info(f"输入任务节点名称:{nodeName}")
        self.input(self.page.get_by_role("textbox", name="请填入名称"),nodeName)
        self.wait(1)
        logger.info(f"输入任务节点描述:{node_desc}")
        self.click(self.page.get_by_role("textbox", name="请填入描述"))
        self.input(self.page.get_by_role("textbox", name="请填入描述"),node_desc)
        logger.info(f"输入任务节点流程指引:{flow_desc}")
        self.input(self.page.get_by_role("textbox", name="请填入流程指引"),flow_desc)
        self.wait(1)
        self.input(self.page.get_by_role("textbox", name="请填入流程指引"),flow_desc)
        self.wait(1)
        logger.info("点击追加结束事件")
        self.page.get_by_title("追加结束事件").dblclick()
        self.wait(1)
        logger.info("点击【保存】按钮")
        self.click(self.page.get_by_role("button", name="保存"))
        self.wait(1)
        logger.info("点击【确定】按钮")
        self.click(self.page.get_by_role("button", name="确定"))
        self.wait_for_load_state()
    
    @allure.step("校验流程模板是否存在:{module_name}")
    def check_flow_module_exist(self,module_name:str):
        """
        校验流程模板是否存在
        """
        self.wait(1)
        locator = self.page.get_by_role("cell", name=module_name).locator('span').first
        logger.info(f"--> 断言 | 流程模板存在 | 模板名称： {module_name}")
        expect(locator).to_be_visible()

    
    @allure.step("筛选流程模板版本状态:{state}")
    def filter_version_state(self,state:str):
        """
        筛选流程模板版本状态
        """
        logger.info(f"筛选【版本状态】列，选择：{state}")
        self.click(self.page.get_by_role("cell", name="版本状态").get_by_role("emphasis"))
        self.click(self.page.locator("#customSelect").get_by_role("textbox", name="请选择"))
        self.click(self.page.get_by_role("list").get_by_text(state, exact=True))
        self.click(self.page.get_by_role("button", name="确认"))
        # self.page.wait_for_timeout(3500)

    
    @allure.step("筛选启用否:{isenable}")
    def filter_isenable(self,isenable:bool):
        """
        筛选启用否
        """
        logger.info(f"筛选【是否启用】列，选择：{isenable}")
        enable_str = "是" if isenable else "否"
        self.click(self.page.get_by_role("cell", name="启用否").get_by_role("emphasis"))
        self.click(self.page.locator("#customSelect").get_by_role("textbox", name="请选择"))
        self.click(self.page.get_by_role("listitem").filter(has_text=enable_str))
        self.click(self.page.get_by_role("button", name="确认"))
        # self.page.wait_for_timeout(3500)

    @allure.step("搜索流程模板名称:{module_name}")
    def search_flow_module(self,module_name:str):
        """
        搜索流程模板
        """
        locator = self.page.get_by_role("textbox", name="请输入", exact=True)
        self.click(locator)
        self.input(locator,module_name)
        self.press(locator,"Enter")
        self.wait(1)
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        elements = self.page.get_by_text(locator_str)
        if elements.count() == 0:
            logger.info(f"没有搜索到相匹配的流程模板：{module_name}")
            return None
        else:
            logger.info(f"搜索到[{elements.count()}]个相匹配结果 | 搜索关键字：{module_name}")
            return elements

    @allure.step("禁用流程模板:{module_name}")
    def disable_flow_module(self,module_name:str):
        """
        禁用流程模板
        """
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        locator = self.page.get_by_text(locator_str).first
        module_name = locator.text_content()
        self.right_click_flow_module(module_name)
        self.click_right_menu("禁用")
        logger.info(f"筛选【是否启用】列，选择：否")
        self.filter_isenable(False)
        self.wait(1)
        logger.info(f"校验流程模板是否禁用 | 模板名称：{module_name}")
        self.check_flow_module_exist(module_name)

    @allure.step("删除流程模板失败,流程模板已被使用:{module_name}")
    def delete_flow_module(self,module_name:str):
        """
        删除流程模板失败,流程模板已被使用
        """
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        locator = self.page.get_by_text(locator_str).first
        module_name = locator.text_content()
        self.right_click_flow_module(module_name)
        self.click_right_menu("删除")
        logger.info(f"点击二次【确认】按钮")
        self.click(self.page.get_by_role("button", name="确认"))
        self.wait(2)
        elements = self.page.get_by_text("流程模板已被使用, 不能删除")
        assert elements.count() > 0, "删除流程模板失败"
        logger.info(f"删除流程模板失败 | 模板名称：{module_name}")

    @allure.step("右键点击流程模板:{module_name}")
    def right_click_flow_module(self,module_name:str):
        """
        右键点击流程模板
        """
        logger.info(f"右键点击模板名称：{module_name}")
        self.page.get_by_role("cell", name=module_name).locator("span").click(button="right")
        self.wait(1)

    @allure.step("点击流程模板右键菜单:{menu_name}")
    def click_right_menu(self,menu_name:str):
        """
        点击流程模板右键菜单(编辑、撤销编辑、禁用、启用、流程图、删除、BPMN、发起流程、检入、查看记录)
        """
        self.click(self.page.get_by_text(menu_name,exact=True))
        self.wait(1)


    @allure.step("发起简单流程:{flow_module_name}")
    def create_new_flow(self,module_name:str,flow_module_name:str,flow_module_desc:str):
        """
        发起简单流程
        """
        locator_str = re.compile(r".*{}.*".format(module_name), re.IGNORECASE)
        locators = self.page.get_by_text(locator_str)
        logger.info(f"查找【{module_name}】流程模板，共{locators.count()}个")
        module_name = locators.first.text_content()
        self.right_click_flow_module(module_name)
        self.click_right_menu("发起流程")
        self.input("//input[@placeholder='请填入流程名称']",flow_module_name)
        self.input("//textarea[@placeholder='请填入流程描述']",flow_module_desc)
        self.click(self.page.get_by_role("button", name="提交"))
        self.is_element_visible(self.page.get_by_text("流程发起成功"))
        logger.info(f"发起简单流程成功 | 流程名称：{flow_module_name}")
