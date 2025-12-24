# -*- coding: utf-8 -*-
# @File    : panoramic_navigation_page.py
# @Software: PyCharm
# @Desc:全景导航页面

# 标准库导入
# 第三方库导入
import allure
from playwright.sync_api import expect

# 本地应用/模块导入
from utils.base_utils.base_page import BasePage


class PanoramicNavigationPage(BasePage):
    """
    全景导航页面
    """

    #homepage logo标识
    locator_page_home_tip = "//img[@class='logo-img']"
    #进入全景导航 【更多>>】定位
    locator_page_in_panoramic_navigation_more = "//div[contains(text(),'更多>>')]"
    #收藏更多导航
    locator_page_in_panoramic_navigation_get_more1 = "//span[text()='收藏更多导航']"
    locator_page_in_panoramic_navigation_get_more2 = "//span[text()='添加更多导航']"
    # 自定义导航条
    locator_page_custom_navigation = "//span[text()='自定义导航条']"
    # 自定义导航条弹出框 返回、确定、取消
    locator_page_custom_navigation_back = "//i[@class='el-icon-back']"
    locator_page_custom_navigation_ok = "//button/span[text()='确 定']"
    locator_page_custom_navigation_cancel = "//button/span[text()='取 消']"
    # 自定义导航 -> 删除特定导航
    locator_page_custom_navigation_delete = "//span[text()='{}']/following-sibling::i"
    # 全景导航侧边栏 -> 系统配置
    locator_page_navigation_system_setting = "(//span[text()='系统配置'])[1]"
    #全景导航侧边栏
    locator_page_navigation_sidebar = "(//span[text()='{}'])[2]"


    @allure.step("访问仪表盘页面：/#/system-dashboard/dashboard?appName=ALL&_s=DashboardPortal")
    def navigate(self):
        """
        访问流程设计-流程模板页面
        """
        self.visit("/#/system-dashboard/dashboard?appName=ALL&_s=DashboardPortal")

    @allure.step("检查是否进入主页面")
    def is_home_page(self):
        """
        确定当前页面是主页面
        """
        # self.is_element_visible( self.page.locator(".portal-logo"))
        expect(self.page.locator(".portal-logo")).to_be_visible(timeout=10000)

    @allure.step("全景导航：点击主页侧边栏导航【更多>>】，收藏更多导航")
    def click_panoramic_navigation_page_more(self):
        """
            全景导航：点击主页侧边栏导航【更多>>】
        """

        # self.click(locator=self.locator_page_in_panoramic_navigation_more)
        try:
            self.page.locator(".portal-navigation").click()
        except:
            try:
                self.click(self.page.get_by_text("更多")) 
            except:
                elment_handle =self.page.wait_for_selector(self.locator_page_in_panoramic_navigation_more, state="visible", timeout=8000)
                elment_handle.click()

    @allure.step("全景导航：点击弹出框【收藏更多导航】")
    def click_panoramic_navigation_page_get_more(self):
        """
            全景导航：点击弹出框【收藏更多导航】
        """
        try:
            elment_handle =self.page.wait_for_selector(self.locator_page_in_panoramic_navigation_get_more1, state="visible", timeout=8000)
            elment_handle.click()
        except:
            self.click(self.page.get_by_text("添加更多导航"))
            

    @allure.step("全景导航：点击弹出框【自定义导航条】")
    def click_custom_navigation(self):
        """
            全景导航：点击弹出框【自定义导航条】
        """
        self.click(locator=self.locator_page_custom_navigation)

    @allure.step("全景导航：点击【自定义导航条】弹出框【取消】按钮，取消自定义导航操作")
    def click_custom_navigation(self):
        """
            全景导航：点击【自定义导航条】弹出框【取消】按钮，取消自定义导航操作
        """
        self.click(locator=self.locator_page_custom_navigation_cancel)

    @allure.step("全景导航：点击【自定义导航条】弹出框【返回】图标，取消自定义导航操作")
    def click_custom_navigation(self):
        """
            全景导航：点击【自定义导航条】弹出框【返回】图标，取消自定义导航操作
        """
        self.click(locator=self.locator_page_custom_navigation_back)

    @allure.step("全景导航：删除自定义导航条上【{navigation_name}】")
    def delete_custom_navigation(self, navigation_name:str):
        """
            全景导航：删除自定义导航条上指定的导航
        """
        locator_str = self.locator_page_custom_navigation_delete.format(navigation_name)
        self.click(locator=locator_str)

    @allure.step("全景导航：点击侧边栏【{navigation_name}】下的【{navigation_sub_name}】，进入【{navigation_sub_name}】页面")
    def click_navigation_sidebar(self, navigation_name:str,navigation_sub_name:str):
        """
            全景导航：点击侧边栏指定功能下的子功能，进入指定子功能页面
        """
        # locator_parent_str = self.locator_page_navigation_sidebar.format(navigation_name)
        # locator_sub_str = self.locator_page_navigation_sidebar.format(navigation_sub_name)
        # self.click(locator=locator_parent_str)
        # self.click(locator=locator_sub_str)
        self.click(self.page.get_by_text(navigation_name).first)
        # element_handle = self.page.wait_for_selector("//span[text()='产品管理']", state="visible", timeout=8000)
        self.click(self.page.get_by_text(navigation_sub_name).first)
        # self.click("//span[text()='产品管理']")
