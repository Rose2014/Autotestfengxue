# -*- coding: utf-8 -*-
# @File    : system_manager_page.py
# @Software: PyCharm
# @Desc:系统管理页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect
from loguru import logger

from config.global_vars import GLOBAL_VARS
# 本地应用/模块导入
from utils.base_utils.base_page import BasePage

class SystemManagerPage(BasePage):
    #系统配置用户相关字段定位
    #成员 页签
    locator_page_members = "[id='tab-members']"
    #信息 页签
    locator_page_infos = "[id='tab-infos']"
    #创建 按钮
    locator_page_create_user_btn = "[name='USER_CREATE']"
    #搜索框
    locator_page_search_input = "[placeholder='姓名/登录账号/邮箱/工号/手机号']"
    locator_page_search_input_btn = "//input[@placeholder='姓名/登录账号/邮箱/工号/手机号']/following-sibling::span"

    #创建用户相关字段定位
    #工号输入框
    locator_page_userid_input = "[placeholder='请填入工号']"
    #账号输入框
    locator_page_useraccount_input = "[name='name']"
    #中文名输入框
    locator_page_usercn_input = "[placeholder='请填入中文名']"
    #英文名输入框
    locator_page_useren_input = "[placeholder='请填入英文名']"
    #邮箱输入框
    locator_page_mail_input = "[placeholder='请填入邮箱']"
    #手机号输入框
    locator_page_phone_input = "[placeholder='请填入手机']"
    #密级 下拉选择
    locator_page_securityLevel_Dropdown_selection = "[placeholder='请填入密级']"
    locator_page_securityLevel_select_option = "//span[text()='{}']/.."
    #license授权 单选按钮
    locator_page_license_radio = "[id='FamRadio']"
    #确定按钮
    locator_page_user_ok_btn = "(//button/span[text()='确定'])[2]"
    #取消按钮
    locator_page_user_cancel_btn = "(//button/span[text()='取消'])[2]"

    @allure.step("访问系统管理页面：/system-participant/member?_s=SystemManagement")
    def navigate(self):
        """
        访问系统管理页面
        """
        self.visit("#/system-participant/member?_s=SystemManagement")

    @allure.step("点击【成员】页签")
    def click_members(self) -> None:
        """
        点击用户列表页面【成员】页签
        """
        self.click(self.locator_page_members)


    @allure.step("点击【信息】页签")
    def click_infos(self) -> None:
        """
        点击用户列表页面【信息】页签
        """
        self.click(self.locator_page_infos)

    @allure.step("在用户搜索框输入【{text}】，进行搜索")
    def search_user(self,text:str) -> None:
        """
        点击用户列表页面【信息】页签
        """
        self.input(self.locator_page_search_input,text)
        self.page.keyboard.press("Enter")


    @allure.step("校验用户【{text}】是否存在，用户应该存在")
    def assert_user(self,text:str) -> None:
        """
        校验用户是否存在
        """
        count = self.page.get_by_text(text).count()
        logger.info("用户[{}]的数量是{}", text, count)
        assert count > 2


    @allure.step("点击【创建】按钮")
    def click_create_user_btn(self) -> None:
        """
        点击创建用户按钮
        """
        self.click(self.locator_page_create_user_btn)
    @allure.step("检查【创建用户】弹框是否唤起")
    def is_create_user_dialog(self):
        expect(self.page.get_by_role("dialog",name="创建用户")).to_be_visible()

    @allure.step("在创建用户弹框页面输入用户工号")
    def input_userid(self,text:str) -> None:
        """
        在创建用户弹框页面输入用户工号
        """
        self.input(self.locator_page_userid_input,text)

    @allure.step("在创建用户弹框页面输入用户账号")
    def input_user_account(self, text: str) -> None:
        """
        在创建用户弹框页面输入用户账号
        """
        self.input(self.locator_page_useraccount_input, text)

    @allure.step("在创建用户弹框页面输入中文名")
    def input_user_cn(self, text: str) -> None:
        """
        在创建用户弹框页面输入用户中文名
        """
        self.input(self.locator_page_usercn_input, text)

    @allure.step("在创建用户弹框页面输入英文名")
    def input_user_en(self, text: str) -> None:
        """
        在创建用户弹框页面输入用户英文名
        """
        self.input(self.locator_page_useren_input, text)

    @allure.step("在创建用户弹框页面输入邮箱")
    def input_user_mail(self, text: str) -> None:
        """
        在创建用户弹框页面输入用户邮箱
        """
        self.input(self.locator_page_mail_input, text)

    @allure.step("选择密级【{text}】")
    def select_security_level(self,text:str) -> None:
        """
        选择密级，默认访客
        """
        self.click(self.locator_page_securityLevel_Dropdown_selection)
        self.click(self.locator_page_securityLevel_select_option.format(text))

    @allure.step("在创建用户弹框页面输入手机号")
    def input_user_phone(self, text: str) -> None:
        """
        在创建用户弹框页面输入用户手机号
        """
        self.input(self.locator_page_phone_input, text)

    @allure.step("在创建用户弹框页面license授权选择{text}")
    def select_user_license(self, text: str) -> None:
        """
        在创建用户弹框页面进行license授权选择
        """
        self.page.get_by_role("radio",name=text).filter(has_text=text).click()

    @allure.step("点击确定按钮")
    def click_ok_btn(self) -> None:
        """
        点击确定按钮
        """
        locator_ok_btn = self.page.get_by_role("button", name="确定")
        self.click(locator_ok_btn)

    @allure.step("点击取消按钮")
    def click_cancel_btn(self) -> None:
        """
        点击取消按钮
        """
        locator_cancel_btn = self.page.get_by_role("button", name="取消")
        self.click(locator_cancel_btn)