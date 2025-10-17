# -*- coding: utf-8 -*-
# @File    : test_flowmodule.py
# @Software: PyCharm
# @Desc:测试-流程设计-流程模板

# 标准库导入
import time
# 第三方库导入
import pytest
from loguru import logger
from playwright.sync_api import Page
from pages.CBB.flow_module_page import FlowModulePage

@pytest.mark.cbb
class TestFlowModule:
    """CBB-流程模板测试"""
    cases = {
        "create_flow_module": [
            {
                "title": "创建简单流程模板",
                "moduleTypeName": "自动化",
                "moduleName": f"自动化测试{time.strftime('%Y%m%d%H%M%S')}",
                "moduleId": f"PROC_{time.strftime('%Y%m%d%H%M%S')}",
                "moduleDesc": f"自动化测试流程-模板描述{time.strftime('%Y%m%d%H%M%S')}",
                "nodeName": f"自动化测试节点{time.strftime('%Y%m%d%H%M%S')}",
                "nodeDesc": f"自动化测试节点-描述{time.strftime('%Y%m%d%H%M%S')}",
                "nodeFlowDesc": f"自动化测试节点-流程指引{time.strftime('%Y%m%d%H%M%S')}",
                "run": False
            }
        ],
        "disable_flow_module": [
            {
                "title": "禁用流程模板",
                "moduleTypeName": "自动化",
                "moduleName": "自动化测试",
                "run": True
            }
        ],
        "delete_flow_module": [
            {
                "title": "删除流程模板",
                "moduleTypeName": "自动化",
                "moduleName": "自动化测试",
                "run": True
            }
        ],
        "create_new_flow": [
            {
                "title": "发起简单流程",
                "moduleTypeName": "自动化",
                "moduleName": "自动化测试",
                "flowModuleName": f"自动化测试-发起流程-{time.strftime('%Y%m%d%H%M%S')}",
                "flowModuleDesc": f"自动化测试-发起流程-描述-{time.strftime('%Y%m%d%H%M%S')}",
                "run": False
            }
        ],
    }

    @pytest.fixture(autouse=True)
    def setup_teardown_for_each(self,user_page: Page):
        logger.info("\n---------------Start: 开始测试-------------\n")
        self.user_page = user_page
        self.flow_module_page = FlowModulePage(self.user_page)
        self.flow_module_page.navigate()
        yield
        logger.info("\n---------------End: 结束测试-------------\n")

    @pytest.mark.parametrize("case", cases["create_flow_module"], ids=lambda x: x["title"])
    def test_create_flow_module(self,case):
        """
        测试-流程设计-流程模板-创建流程模板
        """
        self.flow_module_page.search_module_type(case.get("moduleTypeName"))
        self.flow_module_page.click_module_type(case.get("moduleTypeName"))
        self.flow_module_page.create_flow_module(case.get("moduleName"),case.get("moduleId"),case.get("moduleDesc"),case.get("nodeName"),case.get("nodeDesc"),case.get("nodeFlowDesc"))
        self.flow_module_page.check_flow_module_exist(case.get("moduleName"))
    
    @pytest.mark.parametrize("case", cases["disable_flow_module"], ids=lambda x: x["title"])
    def test_disable_flow_module(self,case):
        """
        测试-流程设计-流程模板-禁用流程模板
        """
        self.flow_module_page.search_module_type(case.get("moduleTypeName"))
        self.flow_module_page.click_module_type(case.get("moduleTypeName"))
        self.flow_module_page.filter_version_state("已检入")
        self.flow_module_page.search_flow_module(case.get("moduleName"))
        self.flow_module_page.disable_flow_module(case.get("moduleName"))
    
    @pytest.mark.parametrize("case", cases["delete_flow_module"], ids=lambda x: x["title"])
    def test_delete_flow_module(self,case):
        """
        测试-流程设计-流程模板-删除流程模板
        """
        self.flow_module_page.search_module_type(case.get("moduleTypeName"))
        self.flow_module_page.click_module_type(case.get("moduleTypeName"))
        self.flow_module_page.filter_version_state("已检入")
        self.flow_module_page.search_flow_module(case.get("moduleName"))
        self.flow_module_page.filter_isenable(False)
        self.flow_module_page.delete_flow_module(case.get("moduleName"))

    @pytest.mark.parametrize("case", cases["create_new_flow"], ids=lambda x: x["title"])
    def test_create_new_flow(self,case):
        """
        测试-流程设计-流程模板-发起简单流程
        """     
        self.flow_module_page.search_module_type(case.get("moduleTypeName"))
        self.flow_module_page.click_module_type(case.get("moduleTypeName"))
        self.flow_module_page.filter_version_state("已检入")
        self.flow_module_page.create_new_flow(case.get("moduleName"),case.get("flowModuleName"),case.get("flowModuleDesc"))

