# -*- coding: utf-8 -*-
# @File    : conftest
# @Software: PyCharm
# @Desc:

# 标准库导入
import os
import json
import time
# 第三方库导入
import pytest
from jsonpath import jsonpath
from loguru import logger
from playwright.sync_api import Page
# 本地应用/模块导入
from config.path_config import BASE_DIR
from config.global_vars import GLOBAL_VARS
from pages.login_page import LoginPage
from pages.panoramic_navigation_page import PanoramicNavigationPage


@pytest.fixture(scope="function")
def user_page(new_context):
    """
    创建default_user_page, 加载default_user.json数据
    :return:
    """
    users = {
        "login": GLOBAL_VARS['default_user_login'],
        "password": GLOBAL_VARS['default_user_password']
    }
    # 如果读取用户登录数据成功且用户cookies没有过期，则免登录
    if is_login_valid(users["login"]):
        context = new_context(storage_state=is_login_valid(users["login"]))
        page = context.new_page()
    else:
        # 读取用户登录数据失败或者已过期，需要登录
        logger.warning("登录已过期")
        context = new_context()
        page = page_login_save_cookies(users, context.new_page())

    yield page

def is_login_valid(login):
    user_json_path = os.path.join(BASE_DIR, ".auth", f"{login}.json")
    logger.info(f"user_json_path:{user_json_path}")
    try:
        with open(user_json_path, 'r', encoding='utf-8') as file:
            user_json = json.load(file)
            # logger.debug(f"成功读取用户JSON文件内容{user_json}")
        expires = jsonpath(user_json, "$.cookies[?(@.name=='locale')].expires")[0]
        if expires and time.time() < expires:
            logger.debug(f"{user_json_path}，用户登录态未过期，无需重新登录，可直接使用")
            return user_json_path
        else:
            logger.debug(f"{user_json_path}，未正确获取到用户登录态或已过期，需重新登录")
            return None
    except:
        logger.debug(f"{user_json_path}内容为空，无法读取，或者内容错误，无法提取过期时间，需重新登录")
        return None


def page_login_save_cookies(users, page: Page):
    """
    用户登录并且保存cookies
    """
    LoginPage(page).navigate()
    LoginPage(page).is_login_page()
    LoginPage(page).login_on_page_flow(users["login"], users["password"])
    # 断言：登录成功
    
    PanoramicNavigationPage(page).is_home_page()
    page.wait_for_timeout(3000)
    user_json_path = os.path.join(BASE_DIR, ".auth", f"{users['login']}.json")
    # 在本地会保存登录cookies
    page.context.storage_state(path=user_json_path)

    return page
