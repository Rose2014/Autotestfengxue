# -*- coding: utf-8 -*-
# @File    : api_design_page.py
# @Software: PyCharm
# @Desc:接口设计页面

# 标准库导入
# 第三方库导入
import allure
import json
from playwright.sync_api import expect
from config.global_vars import GLOBAL_VARS
from loguru import logger
import re
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage

class ApiDesignPage(BasePage):
    """
    流程设计-接口设计页面
    """

    @allure.step("访问流程设计-接口设计页面：/biz-bpm/processManagement/interface?_s=bpmProcessManagement")
    def navigate(self):
        """
        访问流程设计页面
        """
        self.visit("/#/biz-bpm/processManagement/interface?_s=bpmProcessManagement")

    @allure.step("点击创建按钮")
    def click_create_btn(self):
        """
        点击创建按钮
        """
        logger.info("点击创建按钮")
        # self.click(self.page.get_by_role("button", name="᳆ 创建"))
        locator_str = "//button[@businessname='接口创建']"
        self.click(locator_str)
    
    @allure.step("选择接口分类：{category}")
    def select_api_category(self, category: str):
        """
        选择接口分类，category取值可选：业务接口、处理接口、用户
        """
        logger.info(f"选择接口分类：{category}")
        self.click(self.page.get_by_role("textbox", name="请选择").nth(3))
        # self.wait(1)
        self.click(self.page.get_by_role("listitem").filter(has_text=category))
        # self.wait(1)

    @allure.step("选择接口类型：{api_type}")
    def select_api_type(self, api_type: str):
        """
        选择接口类型，api_type取值可选：DUBBO、REST、MQ
        """
        logger.info(f"选择接口类型：{api_type}")
        self.click(self.page.locator("label").filter(has_text=api_type))
    
    @allure.step("选择请求方法：{request_method}")
    def select_request_method(self, request_method: str):
        """
        选择请求方法，request_method取值可选：GET、POST、PUT
        """
        logger.info(f"选择请求方法：{request_method}")
        self.click(self.page.get_by_label("新增接口").get_by_role("textbox", name="请选择").nth(1))
        # self.wait(1)
        self.click(self.page.get_by_role("listitem").filter(has_text=request_method))
        # self.wait(1)
    
    @allure.step("输入接口名称：{api_name}")
    def input_api_name(self, api_name: str):
        """
        输入接口名称
        """
        logger.info(f"输入接口名称：{api_name}")
        # self.clear(self.page.locator(".el-input.el-input--medium.el-input--suffix.el-input--clearable.el-input--limit > .el-input__inner").first)
        # self.input(self.page.locator(".el-input.el-input--medium.el-input--suffix.el-input--clearable.el-input--limit > .el-input__inner").first, api_name)
        locator_str = "//input[@maxlength='64']"
        self.clear(locator_str)
        self.input(locator_str, api_name)

    @allure.step("输入接口地址：{api_path}")
    def input_api_path(self, api_path: str):
        """
        输入接口请求地址
        """
        logger.info(f"输入接口路径：{api_path}")
        locator_str = "//input[@maxlength='256']"
        self.clear(locator_str)
        self.input(locator_str, api_path)

    @allure.step("{type}接口，点击确认按钮")
    def click_confirm_btn(self,type: str):
        """
        点击确认按钮，type:新建，编辑
        校验新建接口走新建接口的请求，编辑接口走编辑接口的请求
        """
        logger.info(f"点击确认按钮：{type}接口")
        if type == "新建":
            # 新建，拦截create接口请求
            # 1. 开始等待一个请求（例如，URL中包含'/api/data'的请求）
            with self.page.expect_request(r"**/bpm/create**") as request_info: 
            # 2. 然后执行会触发该网络请求的页面操作
                self.click(self.page.get_by_role("button", name="确 定"))
            # 3. 在with块结束后，通过request_info获取请求对象
            request = request_info.value
            if request.method == "POST":
                try:
                    payload = request.post_data_json
                    logger.info(f"请求负载: {payload}")
                except:
                    logger.info(f"原始请求数据: {request.post_data}")
            # logger.info(f"点击确认按钮，触发请求：{request}")
        elif type == "编辑":
            # 新建，拦截create接口请求
            # 1. 开始等待一个请求（例如，URL中包含'/api/data'的请求）
            with self.page.expect_request(r"**/bpm/update**") as request_info: 
            # 2. 然后执行会触发该网络请求的页面操作
                self.click(self.page.get_by_role("button", name="确 定"))
            # 3. 在with块结束后，通过request_info获取请求对象
            request = request_info.value
            if request.method == "POST":
                try:
                    payload = request.post_data_json
                    logger.info(f"请求负载: {payload}")
                except:
                    logger.info(f"原始请求数据: {request.post_data}")
            # logger.info(f"点击确认按钮，触发请求：{request}")
        else:
            raise ValueError(f"不支持的类型：{type}")
        

    @allure.step("输入接口描述：{api_desc}")
    def input_api_desc(self, api_desc: str):
        """
        输入接口描述
        """
        logger.info(f"输入接口描述：{api_desc}")
        locator = self.page.locator("textarea").nth(1)
        self.clear(locator)
        self.input(locator,api_desc)
    
    @allure.step("选择应用：{app_name}")
    def select_api_app(self, app_name: str):
        """
        选择应用
        """
        logger.info(f"选择应用：{app_name}")
        self.click(self.page.get_by_role("textbox", name="请填入应用"))
        # self.wait(1)
        self.click(self.page.get_by_role("listitem").filter(has_text=app_name).locator("span"))
        # self.wait(1)

    @allure.step("选择调用方式：{async_type}")
    def select_async_type(self, async_type: str):
        """
        选择调用方式，async_type取值可选：同步、异步
        """
        logger.info(f"选择调用方式：{async_type}")
        self.click(self.page.get_by_label("新增接口").get_by_role("textbox", name="请选择").nth(2))
        # self.wait(1)
        self.click(self.page.get_by_role("listitem").filter(has_text=async_type))
        # self.wait(1)

    @allure.step("选择消息发送类型：{msg_send_type}")
    def select_msg_send_type(self, msg_send_type: str):
        """
        选择消息发送类型，msg_send_type取值可选：全部实例、全局一次、单一实例
        """
        logger.info(f"选择消息发送类型：{msg_send_type}")
        self.click(self.page.get_by_role("textbox", name="请选择").nth(4))
        self.click(self.page.get_by_role("listitem").filter(has_text=msg_send_type))

    @allure.step("输入接口参数：{request_params}")
    def input_request_params(self, request_params: str):
        """
        输入接口参数，request_params为json字符串
        """
        logger.info(f"输入接口参数：{request_params}")
        request_params = json.dumps(request_params, indent=2)
        # locator_str = "//span[contains(text(),'999999999')]/preceding-sibling::textarea"
        locator_str = "//textarea[@maxlength='999999999']"
        self.clear(locator_str)
        self.input(locator_str,request_params)

    @allure.step("通过[接口名称]字段搜索：{api_name}")
    def search_api_by_name(self, api_name: str):
        """
        通过[接口名称]字段搜索
        """
        logger.info(f"通过[接口名称]字段搜索：{api_name}")
        locator=self.page.get_by_role("textbox", name="请输入", exact=True)
        # input_name_locator=self.page.locator("#FamViewTableHeader").get_by_text("接口名称").nth(1)
        self.clear(locator)
        self.input(locator, api_name)
        # self.press(locator, "Enter")
    
    @allure.step("通过[接口类型]字段搜索：{api_type}")
    def search_api_by_api_type(self, api_type: str):
        """
        通过[接口类型]字段搜索，api_type取值可选：DUBBO、REST、MQ
        """
        logger.info(f"通过[接口类型]字段搜索：{api_type}")
        # selector_box = self.page.locator("div").filter(has_text=re.compile(r"^接口类型接口类型$")).get_by_role("textbox")
        selector_box = self.page.locator("#FamViewTableHeader").get_by_text("接口类型").nth(1)
        selector_option = self.page.get_by_role("listitem").filter(has_text=api_type)
        self.click(selector_box)
        self.click(selector_option)
    
    @allure.step("通过[接口分类]字段搜索：{category}")
    def search_api_by_category(self, category: str):
        """
        通过[接口分类]字段搜索，category取值可选：业务接口、处理接口、用户接口
        """
        logger.info(f"通过[接口分类]字段搜索：{category}")
        # selector_box = self.page.locator("div").filter(has_text=re.compile(r"^接口分类接口分类$")).get_by_role("textbox")
        selector_box = self.page.locator("#FamViewTableHeader").get_by_text("接口分类").nth(1)
        selector_option = self.page.get_by_role("listitem").filter(has_text=category)
        self.click(selector_box)
        self.click(selector_option)

        
    @allure.step("通过[调用方式]字段搜索：{call_type}")
    def search_api_by_call_type(self, call_type: str):
        """
        通过[调用方式]字段搜索，call_type取值可选：同步、异步
        """
        logger.info(f"通过[调用方式]字段搜索：{call_type}")
        selector_box = self.page.locator("#FamViewTableHeader").get_by_text("调用方式").nth(1)
        selector_option = self.page.get_by_role("listitem").filter(has_text=call_type)
        self.click(selector_box)
        self.click(selector_option)
        
        
    @allure.step("清空搜索条件")
    def clear_search_conditions(self):
        """
        清空搜索条件
        """
        logger.info("清空搜索条件")
        clear_btn_locator = self.page.get_by_role("button", name="清空条件")
        self.click(clear_btn_locator)
        
    @allure.step("混合搜索：接口名称={api_name}, 接口类型={api_type}, 接口分类={category}, 调用方式={call_type}")
    def group_search(self,api_name: str="", api_type: str="", category: str="", call_type: str=""):
        """
        混合搜索\n
        api_type取值范围：DUBBO、REST、MQ\n
        category取值范围：业务接口、处理接口、用户接口\n
        call_type取值范围：同步、异步\n
        """
        logger.info(f"混合搜索：接口名称={api_name}, 接口类型={api_type}, 接口分类={category}, 调用方式={call_type}")
        self.clear_search_conditions()
        if api_name:
            self.search_api_by_name(api_name)
        if api_type:
            self.search_api_by_api_type(api_type)
        if category:
            self.search_api_by_category(category)
        if call_type:
            self.search_api_by_call_type(call_type)

    @allure.step("点击列表中第1条数据")
    def click_list_no1_item(self,keyword: str=""):
        """
        点击列表中第1条数据
        """
        logger.info("点击列表中第1条数据")
        locator = self.page.get_by_role("cell", name=re.compile(rf"^{keyword}.*")).first.locator("span")
        self.click(locator)

    @allure.step("右键点击列表中第1条数据")
    def right_click_list_no1_item(self,keyword: str=""):
        """
        右键点击列表中第1条数据
        """
        logger.info("右键点击列表中第1条数据")
        locator = self.page.get_by_role("cell", name=re.compile(rf"^{keyword}.*")).first.locator("span")
        locator.click(button="right")

    @allure.step("选择右键菜单选项：{menu_option}")
    def select_menu_option(self,menu_option: str=""):
        """
        选择右键菜单选项,可选选项：编辑、历史版本、关联流程定义
        """
        logger.info(f"选择右键菜单选项：{menu_option}")
        self.click(self.page.locator("a").filter(has_text=menu_option))

    @allure.step("检查接口详情数据：{api_data}")
    def check_api_detail(self,api_data):
        """
        检查接口详情数据
        """
        
        for key, value in api_data.items():
            if key == "title" or key == "run" or key == "用例名称" or key == "序号":
                continue
            logger.info(f"检查接口详情是否包含指定关键字：{key} in {value}")
            expect(self.page.get_by_label("查看接口").get_by_text(re.compile(f".*{value}.*"), exact=True).first).to_be_visible()
    
    @allure.step("检查接口历史版本数据：{api_data}")
    def check_api_history_version(self,api_data):
        """
        检查接口历史版本数据
        """
        # logger.info(f"检查接口历史版本是否包含指定关键字：{keyword}")
        for key, value in api_data.items():
            logger.info(f"检查接口历史版本是否包含指定关键字：{key} in {value}")
            if key == "title" or key == "run" or key == "用例名称" or key == "序号":
                continue
            elif key == "version" or key == "历史版本":
                try:
                    expect(self.page.get_by_label("历史版本").get_by_text("1", exact=True).first).to_be_visible()
                except:
                    continue
            expect(self.page.get_by_label("历史版本").get_by_text(re.compile(rf".*{value}.*"), exact=True).first).to_be_visible()

    @allure.step("点击列表中第1条数据的复选框")
    def click_no1_checkbox(self):
        """
        点击列表中第1条数据的复选框
        """
        logger.info("点击列表中第1条数据的复选框")
        locator_str = "//tbody/tr[1]/td[1]"
        self.click(self.page.locator(locator_str).nth(1))
        
    @allure.step("点击更多操作按钮,选择操作项：{action}")
    def click_more_actions(self,action):
        """
        点点击更多操作按钮,可选操作项：删除，导入，导出
        """
        logger.info("点击列表中第1条数据的更多操作按钮")
        #第一种方法
        locator_str = "//div[@displaydesc='更多操作']"
        self.click(locator_str)
        #第二种方法
        # self.click(self.page.locator("#fam_action_button button").filter(has_text="操作"))
        #选择操作项
        self.click(self.page.get_by_role("listitem").filter(has_text=action))
    
    @allure.step("删除接口,二次确认，点击{button}按钮")
    def confirm_delete(self,button: str="确认"):
        """
        确认删除接口,二次确认,button:确认、取消
        """
        expect(self.page.get_by_text("你确定要删除数据吗？")).to_be_visible()
        logger.info("删除接口,二次确认，点击{button}按钮")
        if button == "确认":
            with self.page.expect_response(r"**/bpm/deleteByIds**") as response_info: 
                self.click(self.page.get_by_role("button", name="确 定"))
            response = response_info.value
            if response.status == 200:
                try:
                    payload = response.json()
                    logger.info(f"请求响应数据: {payload}")
                    expect(payload["data"]).to_equal(True)
                except:
                    logger.info(f"原始响应数据: {response.text()}")
        elif button == "取消":
            self.click(page.get_by_role("button", name="取 消"))
            expect(self.page.get_by_text("你确定要删除数据吗？")).to_be_hidden()
        else:
            raise ValueError(f"不支持的按钮：{button}")
