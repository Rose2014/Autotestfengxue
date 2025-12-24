# -*- coding: utf-8 -*-
# @File    : test_api_design.py
# @Software: PyCharm
# @Desc:测试-流程设计-流程模板

# 标准库导入
import allure
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
from pages.CBB.api_design_page import ApiDesignPage
from utils.data_utils.excel_handle import ExcelHandle

@allure.epic("流程设计")
@pytest.mark.apidesign
class TestApiDesign:
    """
    流程设计-接口设计
    """
    # 类级别变量，存储测试用例数据
    cases = ExcelHandle().read_excel_file(__file__)
    
    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        """
        前置条件：
        1. 系统管理员账号已登录
        2. 进入流程设计-接口设计页面
        """
        logger.info("\n---------------Start: 开始测试-------------\n")
        self.user_page = user_page
        self.api_design_page = ApiDesignPage(self.user_page)
        self.api_design_page.navigate()
        yield
        logger.info("\n---------------End: 结束测试-------------\n")
    
    @allure.story("test_001_创建REST类型的用户接口")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("case", cases["test_001_create_rest_userapi"], ids=lambda x: x["用例名称"])
    def test_001_create_rest_userapi(self, case):
        """
        测试用例：test_001_create_rest_userapi，创建REST类型的用户接口
        1. 点击“创建”按钮
        2. 选择接口分类为“用户”
        3. 输入接口名称
        4. 选择接口类型为“REST”
        5. 输入接口地址
        6. 选择请求方法为POST
        7. 选择调用方式为“同步”
        8. 选择应用“基础平台”
        9. 输入接口参数
        10. 填写接口描述
        11. 点击“确定”按钮
        """
        self.api_design_page.click_create_btn()
        self.api_design_page.select_api_category(case["接口分类"])
        self.api_design_page.input_api_name(case["接口名称"])
        self.api_design_page.select_api_type(case["接口类型"])
        self.api_design_page.input_api_path(case["接口地址"])
        self.api_design_page.select_request_method(case["请求方法"])
        self.api_design_page.select_async_type(case["调用方式"])
        self.api_design_page.select_api_app(case["应用"])
        self.api_design_page.input_request_params(case["接口参数"])
        self.api_design_page.input_api_desc(case["接口描述"])
        self.api_design_page.click_confirm_btn(type="新建")

    @allure.story("test_002_创建MQ类型的业务接口")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("case", cases["test_002_create_mq_bussnissapi"], ids=lambda x: x["用例名称"])
    def test_002_create_mq_bussnissapi(self, case):
        """
        测试用例：test_002_create_mq_bussnissapi，创建MQ类型的业务接口
        1. 点击“创建”按钮
        2. 选择接口分类为“业务接口”
        3. 输入接口名称
        4. 选择接口类型为“MQ”
        5. 选择消息发送方式为“全部实例”
        6. 选择应用“基础平台”
        7. 输入接口参数
        8. 填写接口描述
        9. 点击“确定”按钮
        """
        self.api_design_page.click_create_btn()
        self.api_design_page.select_api_category(case["接口分类"])
        self.api_design_page.input_api_name(case["接口名称"])
        self.api_design_page.select_api_type(case["接口类型"])
        self.api_design_page.select_msg_send_type(case["消息发送方式"])
        self.api_design_page.select_api_app(case["应用"])
        self.api_design_page.input_request_params(case["接口参数"])
        self.api_design_page.input_api_desc(case["接口描述"])
        self.api_design_page.click_confirm_btn(type="新建")

    @allure.story("test_003_创建处理接口")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("case", cases["test_003_create_handle_api"], ids=lambda x: x["用例名称"])
    def test_003_create_handle_api(self, case):
        """
        测试用例：test_003_create_handle_api，创建处理接口
        1. 点击“创建”按钮
        2. 选择接口分类为“处理接口”
        3. 输入接口名称
        4. 输入接口地址
        5. 选择请求方法为POST
        6. 选择调用方式为“异步”
        7. 选择应用“基础平台”
        8. 输入接口参数
        9. 填写接口描述
        10. 点击“确定”按钮
        """
        self.api_design_page.click_create_btn()
        self.api_design_page.select_api_category(case["接口分类"])
        self.api_design_page.input_api_name(case["接口名称"])
        self.api_design_page.input_api_path(case["接口地址"])
        self.api_design_page.select_request_method(case["请求方法"])
        self.api_design_page.select_async_type(case["调用方式"])
        self.api_design_page.select_api_app(case["应用"])
        self.api_design_page.input_request_params(case["接口参数"])
        self.api_design_page.input_api_desc(case["接口描述"])
        self.api_design_page.click_confirm_btn(type="新建")
    
    @allure.story("test_004_查看接口详情")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize("case", cases["test_004_check_api_detail"], ids=lambda x: x["用例名称"])
    def test_004_check_api_detail(self, case):
        """
        测试用例：test_004_check_api_detail，查看接口详情
        1. 在列表中点击接口名称
        2. 检查接口详情页面显示的接口信息是否与创建时一致
        """
        self.api_design_page.group_search(api_name=case["接口名称"], category=case["接口分类"], call_type=case["调用方式"])
        self.api_design_page.click_list_no1_item(keyword=case["接口名称"])
        self.api_design_page.check_api_detail(case)
        
    @allure.story("test_005_查看接口历史版本")
    @pytest.mark.run(order=5)
    @pytest.mark.parametrize("case", cases["test_005_check_api_version"], ids=lambda x: x["用例名称"])
    def test_005_check_api_version(self, case):
        """
        测试用例：test_005_check_api_version，查看接口历史版本
        1. 右键点击列表中接口名称
        2. 选择“历史版本”
        3. 检查历史版本弹框显示的历史版本信息是否正确
        """
        self.api_design_page.group_search(api_name=case["接口名称"], call_type=case["调用方式"])
        self.api_design_page.right_click_list_no1_item(keyword=case["接口名称"])
        self.api_design_page.select_menu_option(menu_option="历史版本")
        self.api_design_page.check_api_history_version(case)
        
    @allure.story("test_006_编辑接口")
    @pytest.mark.run(order=6)
    @pytest.mark.parametrize("case", cases["test_006_edit_api"], ids=lambda x: x["用例名称"])
    def test_006_edit_api(self, case):
        """
        测试用例：test_006_edit_api，编辑接口
        1. 点击列表中接口名称
        2. 修改接口信息
        3. 点击“确定”按钮
        4. 检查接口详情页面显示的接口信息是否与修改后一致
        """
        self.api_design_page.group_search(api_name=case["接口名称"], category=case["接口分类"]+"接口")
        self.api_design_page.right_click_list_no1_item(keyword=case["接口名称"])
        self.api_design_page.select_menu_option(menu_option="编辑")
        self.api_design_page.select_api_category(case["新接口分类"])
        self.api_design_page.input_api_name(case["新接口名称"])
        self.api_design_page.input_api_path(case["新接口地址"])
        self.api_design_page.input_api_desc(case["新接口描述"])
        self.api_design_page.click_confirm_btn(type="编辑")
        
    @allure.story("test_007_删除接口")
    @pytest.mark.run(order=7)
    @pytest.mark.parametrize("case", cases["test_007_delete_api"], ids=lambda x: x["用例名称"])
    def test_007_delete_api(self, case):
        """
        测试用例：test_007_delete_api，删除接口
        1. 勾选列表中接口
        2. 依次点击 更多操作 -> 删除 -> 确认删除
        3. 检查接口是否删除成功
        """
        self.api_design_page.group_search(api_name=case["接口名称"], category=case["接口分类"])
        self.api_design_page.click_no1_checkbox()
        self.api_design_page.click_more_actions(action="删除")
        self.api_design_page.confirm_delete(button="确认")
