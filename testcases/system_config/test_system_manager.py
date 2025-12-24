# -*- coding: utf-8 -*-
# @File    : test_system_manager.py
# @Software: PyCharm
# @Desc:系统管理-部门-创建用户

# 第三方库导入
import pytest
import allure
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from pages.system_Config.system_manager_page import SystemManagerPage
from utils.data_utils.excel_handle import ExcelHandle

@allure.epic("系统配置")
@pytest.mark.sys
class TestSystemManager:
    """
    系统管理-参与者
    """
    # 类级别变量，存储测试用例数据
    cases = ExcelHandle().read_excel_file(__file__)

    # cases = self.cases_data
    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        logger.info("\n---------------Start: 开始测试-------------\n")
        self.user_page = user_page
        self.system_manager_page = SystemManagerPage(self.user_page)
        self.system_manager_page.navigate()
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @allure.story("创建用户")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize("case", cases["test_001_create_user"], ids=lambda x: x["用例标题"])
    def test_001_create_user(self, case):
        """
        系统管理员创建用户
        """
        self.system_manager_page.click_members()
        self.system_manager_page.click_create_user_btn()
        self.system_manager_page.is_create_user_dialog()
        userid = case.get("工号")
        self.system_manager_page.input_userid(userid)
        self.system_manager_page.input_user_account(case.get("账号"))
        self.system_manager_page.input_user_cn(case.get("中文名"))
        self.system_manager_page.input_user_en(case.get("英文名"))
        self.system_manager_page.input_user_mail(case.get("邮箱"))
        self.system_manager_page.select_security_level(case.get("密级"))
        self.system_manager_page.input_user_phone(f"{case.get('手机')}")
        # self.system_manager_page.select_user_license(case.get("license")) 
        self.system_manager_page.click_ok_btn()
        
    @allure.story("初始化用户密码")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("case", cases["test_002_reset_password"], ids=lambda x: x["用例标题"])
    def test_002_reset_password(self, case):
        """
        系统管理员,重置用户密码
        """
        userid = case.get("工号")
        self.system_manager_page.search_user(userid)
        self.system_manager_page.reset_password(case.get("密码"))



