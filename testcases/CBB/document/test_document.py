# -*- coding: utf-8 -*-
# @File    : test_document.py
# @Software: PyCharm
# @Desc:测试-流程设计-流程模板

# 标准库导入
import time
# 第三方库导入
import pytest
from loguru import logger
from config.global_vars import GLOBAL_VARS
from playwright.sync_api import Page
from pages.CBB.document_page import DocumentPage
from pages.CBB.product_manager_page import ProductManagerPage
from pages.panoramic_navigation_page import PanoramicNavigationPage
from utils.data_utils.faker_handle import FakerData

@pytest.mark.document
class TestDocument:
    """
    文档相关测试
    1. 创建文档
    2. 编辑文档
    3. 删除文档
    """

    cases = {
        "create_document": [
            {
                "title": "创建文档",
                "document_name": f"自动化测试-变更测试数据{time.strftime('%Y%m%d%H%M%S')}{FakerData.generate_random_int(100000,999999)}",
                "run": True,
            }
        ],

    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        """
        前置条件：
        1. 账号已登录
        2. 进入文档页面
        """
        logger.info("\n---------------Start: 开始测试-------------\n")
        
        #判断是否已登录
        self.user_page = user_page
        #全景导航进入到产品管理页面
        self.panoramic_navigation_page = PanoramicNavigationPage(self.user_page)
        self.panoramic_navigation_page.navigate()
        # self.panoramic_navigation_page.wait_for_load_state("networkidle")
        self.panoramic_navigation_page.click_panoramic_navigation_page_more()
        # self.panoramic_navigation_page.click_panoramic_navigation_page_get_more()
        self.panoramic_navigation_page.click_navigation_sidebar("产品设计","产品管理")
        #产品管理页面：进入到文档二级菜单页面
        product_name = "产品管理系统"
        self.product_manager_page = ProductManagerPage(self.user_page)
        self.product_manager_page.search_context(product_name)
        self.product_manager_page.click_product_name_in_context(product_name)
        self.product_manager_page.click_level2_menu("文档")
        self.product_manager_page.wait_for_load_state("networkidle")

        self.document_page = DocumentPage(self.user_page)
        
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @pytest.mark.parametrize("case", cases["create_document"], ids=lambda x: x["title"])
    def test_001_create_document(self,case):
        """
        测试用例：test_001_create_document
        创建文档
        1. 点击“创建”按钮
        2. 文档主要内容源选择“无内容”
        3. 点击“保存”按钮
        """
        document_name = case["document_name"]
        self.document_page.click_create_button()
        self.document_page.wait_create_document_page_displayed()
        self.document_page.input_document_name(document_name)
        self.document_page.select_main_content_source("无内容")
        self.document_page.click_save_button()
        self.document_page.wait_for_load_state("networkidle")
        