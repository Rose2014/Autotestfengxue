# -*- coding: utf-8 -*-
# @File    : test_module_type.py
# @Software: PyCharm
# @Desc:测试-流程设计-流程模板-流程类型（新建、删除）

# 标准库导入
import time
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
from pages.CBB.flow_module_page import FlowModulePage

@pytest.mark.cbb
class TestModuleType:
    """CBB-流程类型测试"""

    cases = {
        "create_and_delete_module_type": [
            {
                "title": "创建和删除流程类型",
                "moduleTypeName": f"自动化测试-{time.strftime('%Y%m%d%H%M%S')}1",
                "run": False
            }
        ]
    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        """
        前置条件：
        1. 系统管理员账号已登录
        2. 进入流程设计-流程模板页面
        """
        logger.info("\n---------------Start: 开始测试-------------\n")
        self.user_page = user_page
        self.flow_module_page = FlowModulePage(self.user_page)
        self.flow_module_page.navigate()
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @pytest.mark.parametrize("case", cases["create_and_delete_module_type"], ids=lambda x: x["title"])
    def test_001_create_and_delete_module_type(self,case):
        """
        在CBB应用下创建流程类型、删除流程类型
        """
        self.flow_module_page.click_create_module_type_button()
        self.flow_module_page.input_module_type_name(case.get("moduleTypeName"))
        self.flow_module_page.delete_module_type(case.get("moduleTypeName"))
        self.flow_module_page.search_module_type(case.get("moduleTypeName"))
    