# -*- coding: utf-8 -*-
# @File    : base_page
# @Software: PyCharm
# @Desc: Playwright UI自动化基础操作封装


# 标准库导入
import os
import re
import json
from typing import Union, Pattern, Optional, Literal, AnyStr
# 第三方库导入
import allure
from loguru import logger
from playwright.sync_api import Page, Locator
from playwright.sync_api import expect


def _safe_locator_str(locator):
    """
    安全地将Locator对象转换为字符串，确保中文字符不被转义
    """
    if isinstance(locator, Locator):
        # 将Locator对象转换为字符串
        locator_str = str(locator)
        # 尝试解码Unicode转义序列
        try:
            # 查找并解码所有Unicode转义序列
            decoded_str = re.sub(r'\\u([0-9a-fA-F]{4})', 
                               lambda x: chr(int(x.group(1), 16)), 
                               locator_str)
            decoded_str = decoded_str.replace("\\","",)             
            return decoded_str
        except:
            # 如果解码失败，返回原始字符串
            return locator_str
    return str(locator)


class BasePage:
    """
    Playwright UI自动化基础操作封装
    """

    def __init__(self, page: Page):
        self.page = page
        self.context = self.page.context
        self.pages = self.context.pages

    # --------------------------------- 导航 ---------------------------------#
    """
     • goto(url, **kwargs)：导航到指定的URL
     • go_back()：后退到浏览器历史记录中的上一页
     • go_forward()：前进到浏览器历史记录中的下一页
     • reload(**kwargs)：重新加载当前页面
    """

    @allure.step("--> 访问页面，路由：{url}，超时时间： {timeout} 秒")
    def visit(self, url: str, timeout=5) -> None:
        """
        访问页面
        :param url: url
        :param timeout: 超时时间，默认是50000ms
        """
        logger.info(f"--> 访问页面，路由：{url}")
        self.page.goto(url, timeout=timeout * 1000)
        self.wait_for_load_state()

    @allure.step("--> 刷新页面，且状态为：{state}， 超时时间： {timeout} 秒")
    def refresh(self, timeout=5,
                state: Optional[Literal["domcontentloaded", "load", "networkidle"]] = 'networkidle') -> None:
        """
        刷新页面
        :param timeout: 超时时间，默认是50000ms
        :param state: Optional[Literal["domcontentloaded", "load", "networkidle"]] = 'networkidle'
        官方默认是默认为 load， 该方法默认是networkidle
        state:
        domcontentloaded - 等到加载DOMContentLoaded事件
        load - 等到加载load事件
        networkidle - 等到500 ms没有网络请求
        """
        logger.info(f"--> 刷新页面，且状态为：{state}， 超时时间： {timeout} 秒")
        self.page.reload(timeout=timeout * 1000, wait_until=state)

    # --------------------------------- 等待 ---------------------------------#
    @allure.step("--> 强制等待{timeout}秒")
    def wait(self, timeout=3):
        """
        强制等待，单位是秒\n
        仅应用于调试目的。在生产环境中使用计时器的测试将变得不稳定。应改用网络事件、选择器可见性变化等信号作为替代方案。
        """
        logger.info(f'--> 强制等待{timeout}秒')
        self.page.wait_for_timeout(timeout * 1000)

    @allure.step("--> 等待页面加载，且状态为：{state}, 超时{timeout}秒")
    def wait_for_load_state(self,
                            state: Optional[Literal["domcontentloaded", "load", "networkidle"]] = 'load',
                            timeout=30):
        """
        在页面达到所需的加载状态时返回
        官方默认的timeout单位是毫秒，这里timeout传参默认是秒
        官方默认是默认为 load， 该方法默认是networkidle
        state:
        domcontentloaded - 等到加载DOMContentLoaded事件
        load - 等到加载load事件
        networkidle - 等到500 ms没有网络请求
        """
        logger.info(f'--> 等待页面加载，且状态为:{state}')
        self.page.wait_for_load_state(state, timeout=timeout * 1000)

    # --------------------------------- 页面操作和交互---------------------------------#
    def click(self, locator: Union[str,Locator], timeout=30) -> None:
        """
        点击操作
        :param locator: 元素定位
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            # 使用安全的字符串转换函数确保中文正确显示
            logger.info(f"--> 点击元素 | 元素定位：{safe_locator}")
            with allure.step(f"--> 点击元素 | 元素定位：{safe_locator}"):
                if isinstance(locator, str):
                    self.page.click(locator)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.click()
        except Exception as e:
            # 错误日志中也使用安全的字符串转换
            logger.error(f"--> 点击元素 | 元素定位：{safe_locator}，报错：{e}")
            raise f"--> 点击元素 | 元素定位：{safe_locator}，报错：{e}"

    def check(self, locator: Union[str,Locator], timeout=30) -> None:
        """
        勾选checkbox
        :param locator: 元素定位
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> checkbox勾选元素 | 元素定位：{safe_locator}")
            with allure.step(f"--> checkbox勾选元素 | 元素定位：{safe_locator}"):
                if isinstance(locator, str):
                    self.page.check(locator, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.check()
        except Exception as e:
            logger.error(f"--> checkbox勾选元素 | 元素定位：{safe_locator}，报错：{e}")
            raise f"--> checkbox勾选元素 | 元素定位：{safe_locator}，报错：{e}"

    def uncheck(self, locator: Union[str,Locator], timeout=30) -> None:
        """
        取消勾选checkbox
        :param locator: 元素定位
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> checkbox取消勾选元素 | 元素定位： {safe_locator}")
            with allure.step(f"--> checkbox取消勾选元素 | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.uncheck(locator, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.uncheck()
        except Exception as e:
            logger.error(f"--> checkbox取消勾选元素 | 元素定位：{safe_locator}，报错：{e}")
            raise f"--> checkbox取消勾选元素 | 元素定位： {safe_locator}，报错：{e}"

    def hover(self, locator: Union[str,Locator], timeout=30) -> None:
        """
        悬浮在某元素上
        :param locator: 元素定位
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 鼠标悬浮在元素上，元素定位： {safe_locator}")
            with allure.step(f"--> 鼠标悬浮在元素上，元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.hover(locator, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.hover()
        except Exception as e:
            logger.error(f"--> 鼠标悬浮在元素上 | 元素定位：{safe_locator}，报错：{e}")
            raise f"--> 鼠标悬浮在元素上 | 元素定位： {safe_locator}，报错：{e}"

    def focus(self, locator:Union[str,Locator], timeout=30) -> None:
        """ 聚焦定位元素 """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.debug(f'--> 聚焦定位元素，元素定位： {safe_locator}')
            with allure.step(f"--> 聚焦定位元素，元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.focus(locator, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.focus()
        except Exception as e:
            logger.error(f"--> 聚焦定位元素 | 元素定位：{safe_locator}，报错：{e}")
            raise f"--> 聚焦定位元素 | 元素定位： {safe_locator}，报错：{e}"

    def input(self, locator: Union[str,Locator], text: str, timeout=30) -> None:
        """
        输入内容
        :param locator: 元素定位
        :param text: 输入的内容
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        
        try:
            logger.info(f"--> 输入内容： {text} | 元素定位： {safe_locator}")
            with allure.step(f"--> 输入内容： {text} | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.fill(selector=locator, value=text, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.fill(value=text)
        except Exception as e:
            logger.error(f"--> 输入内容： {text} | 元素定位： {safe_locator}， 报错：{e}")
            raise f"--> 输入内容： {text} | 元素定位： {safe_locator}， 报错：{e}"


    def type(self, locator: Union[str,Locator], text: str, timeout=30) -> None:
        """
        一个字符一个字符的输入,模拟键盘的操作，键入内容
        :param locator: 元素定位
        :param text: 输入的内容
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 键盘键入内容： {text} | 元素定位： {safe_locator}")
            with allure.step(f"--> 键盘键入内容： {text} | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.type(selector=locator, text=text, timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.type(text)  
        except Exception as e:
            logger.error(f"--> 键盘键入内容： {text} | 元素定位： {safe_locator}， 报错：{e}")
            raise f"--> 键盘键入内容： {text} | 元素定位： {safe_locator}， 报错：{e}"

    def clear(self, locator: Union[str,Locator], timeout=30) -> None:
        """
        清除元素内容
        :param locator: 元素定位
        :param timeout: 超时时间，默认是30秒
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f'--> 清除元素内容，元素定位： {safe_locator}')
            with allure.step(f"--> 清除元素内容，元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.fill(locator,"",timeout=timeout * 1000)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    locator.fill("")

        except Exception as e:
            logger.error(f"--> 清除元素内容 | 元素定位： {safe_locator}， 报错：{e}")
            raise f"--> 清除元素内容 | 元素定位： {safe_locator}， 报错：{e}"

    def select_option(self, locator: Union[str,Locator], option: Union[str,list[str],int], timeout=30) -> None:
        """
        选择option
        :param locator: 元素定位
        :param option: 选项内容
        :param timeout: 超时时间，默认是30秒
        :这种方法会等待遇到与指定选择器相匹配的元素，会等待完成相关的可操作性检查，会一直等待直到<select>元素中包含了所有指定的选项，
        然后才会选中这些选项。如果目标元素并非<select>元素，那么这种方法会抛出错误；不过，如果该元素位于某个带有关联控件的<label>元素内部，
        那么就会使用该关联控件来代替<select>元素进行操作。该方法会返回那些已被成功选中的选项值所组成的数组，并且会在所有指定的选项都被选中后触发“变化事件”及“输入事件”
        :
        ```
        py
        # 根据值或标签进行单选匹配
        select_option(\"select#colors\", \"blue\")
        # 根据标签进行单选匹配
        select_option(\"select#colors\", label=\"blue\")
        # 根据标签下标单选匹配
        select_option(\"select#colors\", index=1)
        # 多选匹配
        select_option(\"select#colors\", value=[\"red\", \"green\", \"blue\"])
        '''
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 选择选项： {option} | 元素定位： {safe_locator}")
            with allure.step(f"--> 选择选项： {option} | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    if isinstance(option, int):
                        self.page.select_option(selector=locator, index=option)
                    else:
                        self.page.select_option(selector=locator, value=option)  
                elif isinstance(locator, Locator):
                    locator.wait_for(state="visible",timeout=timeout * 1000)
                    if isinstance(option, int):
                        locator.select_option(index=option)
                    else:
                        locator.select_option(value=option)           
        except Exception as e:
            logger.error(f"--> 选择选项： {option} | 元素定位： {safe_locator}， 报错：{e}")
            raise f"--> 选择选项： {option} | 元素定位： {safe_locator}， 报错：{e}"

    def upload_file(self, locator: Union[str,Locator], file_path: str) -> None:
        """
        上传文件
        :param locator: 元素定位
        :param file_path: 文件路径
        """
        if os.path.isfile(file_path):
            safe_locator = _safe_locator_str(locator)
            logger.info(f"--> 上传文件： {file_path} | 元素定位： {safe_locator}")
            with allure.step(f"--> 上传文件： {file_path} | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.set_input_files(selector=locator, files=file_path)
                elif isinstance(locator, Locator):
                    locator.set_input_files(file_path)
            self.wait(timeout=1)
        else:
            logger.error(f"ERROR --> 上传文件失败，附件未找到，请检查{file_path}下是否存在该文件")
            raise ValueError(f"--> 上传文件失败，附件未找到，请检查{file_path}下是否存在该文件")

    @allure.step("--> 执行js脚本： {js}, 可选参数：{args}")
    def execute_js(self, js, *args) -> None:
        """
        执行javascript脚本
        :param js: javascript脚本
        """
        logger.info(f"--> 执行js脚本： {js}, 可选参数：{args}")
        self.page.evaluate(js, *args)

    def press(self, locator: Union[str,Locator], keyboard: str) -> None:
        """
        :param locator: 元素定位
        :param keyboard: 键
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 按{keyboard}键 | 元素定位： {safe_locator}")
            with allure.step(f"--> 按{keyboard}键 | 元素定位： {safe_locator}"):
                if isinstance(locator, str):
                    self.page.press(locator, keyboard)
                elif isinstance(locator, Locator):
                    locator.press(keyboard)
        except Exception as e:
            logger.error(f"--> 按{keyboard}键 | 元素定位： {safe_locator}， 报错：{e}")
            raise f"--> 按{keyboard}键 | 元素定位： {safe_locator}， 报错：{e}"

    @allure.step("--> 截图， 全屏={full_page} | 元素定位： {locator}， 图片保存路径：{path}")
    def screenshot(self, path, full_page=True, locator:str=None):
        """截图功能，默认截取全屏，如果传入定位器表示截取元素"""
        if locator is not None:
            logger.info(f"--> 截图， 全屏={full_page} | 元素定位： {locator}， 图片保存路径：{path}")
            self.page.locator(locator).screenshot(path=path)
            return path
        logger.info(f"--> 截图， 全屏={full_page} | 元素定位： {locator}， 图片保存路径：{path}")
        self.page.screenshot(path=path, full_page=full_page)
        allure.attach.file(path, name=path)
        return path

    # --------------------------------- 页面元素定位 ---------------------------------#

    @allure.step("--> 获取所有的元素 | 元素定位：{locator}")
    def get_all_elements(self, locator: str) -> Union[list, None]:
        """
        获取所有符合定位的元素
        :param locator: 元素定位
        :return: 元素/None
        """
        try:
            logger.info(f"--> 获取所有的元素 | 元素定位： {locator}")
            elems = self.page.query_selector_all(locator)
            allure.attach(str(elems), name="elems", attachment_type=allure.attachment_type.TEXT)
            logger.success(f"--> 获取到的元素：{elems}")
            return elems
        except Exception as e:
            logger.error(f"ERROR --> 获取所有的元素失败 | 元素定位： {locator}，报错信息：{e} ")
            raise e

    def get_text(self, locator: Union[str,Locator]) -> Union[str, None]:

        """
        获取元素的文本内容
        :param locator: 元素定位
        :return: 文本值/None
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 获取元素文本值 | 元素定位： {safe_locator}")
            with allure.step(f"--> 获取元素文本值 | 元素定位： {safe_locator}"):
                text_value = ""
                if isinstance(locator, str):
                    self.page.locator(locator).wait_for(state="attached")
                    text_value = self.page.locator(locator).text_content()
                elif isinstance(locator, Locator):
                    locator.wait_for(state="attached")
                    text_value =locator.text_content()
            logger.success(f"--> 获取到的文本值： {text_value}")
            allure.attach(text_value, name="text_value", attachment_type=allure.attachment_type.TEXT)
            return text_value
        except Exception as e:
            logger.error(f"ERROR --> 获取元素文本值 | 元素定位： {safe_locator}，报错信息：{e} ")
            raise e

    @allure.step("--> 获取所有符合定位要求的元素的文本内容 | 元素定位： {locator}")
    def get_all_elements_text(self, locator:str) -> Union[list, None]:
        """
        获取所有符合定位要求的元素的文本内容
        :param locator: 元素定位
        :return: 文本值/None
        """
        try:
            logger.info(f"--> 获取所有符合定位要求的元素的文本内容 | 元素定位： {locator}")
            elements = self.get_all_elements(locator)
            elems_text = [element.text_content() for element in elements]
            logger.success(f"--> 获取所有符合定位要求的元素的文本内容：{elems_text}")
            allure.attach(str(elems_text), name="elems_text", attachment_type=allure.attachment_type.TEXT)
            return elems_text
        except Exception as e:
            logger.error(f"ERROR --> 获取所有符合定位要求的元素的文本内容 | 元素定位： {locator}，报错信息：{e} ")
            raise e

    def get_element_attribute(self, locator: Union[str,Locator], attr_name: str) -> Union[str, None]:
        """
        获取元素属性值
        :param locator: 元素定位
        :param attr_name: 属性名称
        :return: 元素属性值
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 根据元素的属性获取对应属性值 | 元素定位： {safe_locator}, 属性名称：{attr_name}")
            attr_value = ""
            with allure.step(f"--> 根据元素的属性获取对应属性值 | 元素定位： {safe_locator}, 属性名称：{attr_name}"):
                if isinstance(locator, str):
                    self.page.locator(locator).wait_for(state="attached")
                    attr_value = self.page.locator(locator).get_attribute(name=attr_name)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="attached")
                    attr_value = locator.get_attribute(name=attr_name)
            logger.success(f"--> 获取到的属性值：{attr_value}")
            allure.attach(attr_value, name="attr_value", attachment_type=allure.attachment_type.TEXT)
            return attr_value
        except Exception as e:
            logger.error(f"--> 获取元素属性值 | 元素定位： {safe_locator}，报错信息：{e} ")
            return None

    def get_inner_text(self, locator: Union[str,Locator]) -> Union[str, None]:
        """
        获取元素的文本内容
        :param locator: 元素定位
        :return: 内部文本值
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 获取元素的文本内容 | 元素定位： {safe_locator}")
            with allure.step(f"--> 获取元素的文本内容 | 元素定位： {safe_locator}"):
                text_value = ""
                if isinstance(locator, str):
                    self.page.locator(locator).wait_for(state="attached")
                    text_value = self.page.inner_text(selector=locator)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="attached")
                    text_value = locator.inner_text()
            logger.success(f"--> 获取到的元素文本内容：{text_value}")
            allure.attach(text_value, name="text_value", attachment_type=allure.attachment_type.TEXT)
            return text_value
        except Exception as e:
            logger.error(f"ERROR-->获取元素的文本内容 | 元素定位： {locator}，报错信息：{e} ")
            return None

    def get_inner_html(self, locator: Union[str,Locator]) -> Union[str, None]:
        """
        获取元素的整个html源码内容
        :param locator: 元素定位
        :return: html值
        """
        safe_locator = _safe_locator_str(locator)
        try:
            logger.info(f"--> 获取元素的整个html源码内容 | 元素定位： {safe_locator}")
            with allure.step(f"--> 获取元素的整个html源码内容 | 元素定位： {safe_locator}"):
                html_value = ""
                if isinstance(locator, str):
                    self.page.locator(locator).wait_for(state="attached")
                    html_value = self.page.inner_html(selector=locator)
                elif isinstance(locator, Locator):
                    locator.wait_for(state="attached")
                    html_value = locator.inner_html()
            logger.success(f"--> 获取元素的整个html值：{html_value}")
            allure.attach(html_value, name="html_value", attachment_type=allure.attachment_type.TEXT)
            return html_value
        except Exception as e:
            logger.error(f"ERROR-->获取元素的整个html源码内容 | 元素定位： {locator}，报错信息：{e} ")
            return None

    @allure.step("获取当前页面的url")
    def get_page_url(self) -> AnyStr:
        """
        获取当前页面的url
        :return: url值
        """
        try:
            logger.info(f"--> 获取当前页面的url")
            url_value = self.page.url
            allure.attach(url_value, name="URL Value", attachment_type=allure.attachment_type.TEXT)
            logger.success(f"--> 获取到的url值：{url_value}")
            return url_value
        except Exception as e:
            logger.error(f"ERROR --> 获取当前页面的url，报错信息：{e} ")
            return None

    # --------------------------------- 断言（页面断言） ---------------------------------#
    """
    主要有四个断言方法
        • to_have_title 确保页面具有给定的标题 
        • not_to_have_title  确保页面不具有给定的标题 
        • to_have_url 确保页面导航到给定的URL
        • not_to_have_url 确保页面没有导航到给定的URL
    """

    @allure.step("--> 断言 | 验证页面存在标题： {title}， 超时时间： {timeout} 秒")
    def have_title(self, title: Union[str], timeout=5) -> None:
        """
        断言：检查页面是否存在指定的标题；存在则通过，不存在则失败；
        :param title: 页面标题，接受一个字符串参数或正则表达式参数
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证页面存在标题： {title}")
        expect(self.page).to_have_title(title_or_reg_exp=title, timeout=timeout * 1000)

    @allure.step("--> 断言 | 验证页面不存在标题： {title}， 超时时间： {timeout} 秒")
    def not_have_title(self, title: str, timeout=5) -> None:
        """
        断言：检查页面是否存在指定的标题；不存在则通过，存在则失败；
        :param title: 页面标题，接受一个字符串参数或正则表达式参数
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证页面不存在标题： {title}")
        expect(self.page).not_to_have_title(title_or_reg_exp=title, timeout=timeout * 1000)

    @allure.step("--> 断言 | 验证页面存在URL： {url}， 超时时间： {timeout} 秒")
    def have_url(self, url: Union[str], timeout=5) -> None:
        """
        断言：检查页面是否存在指定的 URL；存在则通过，不存在则失败；
        :param url: 页面标题，接受一个字符串参数或正则表达式参数
        :param timeout: 超时时间， 默认5000ms
        """
        try:
            logger.info(f"--> 断言 | 验证页面存在URL： {url}")
            expect(self.page).to_have_url(url_or_reg_exp=url, timeout=timeout * 1000)
        except Exception as e:
            logger.error(f"--> 断言 | 验证页面存在URL： {url}， 报错：{e}")
            raise e

    @allure.step("--> 断言 | 验证页面不存在URL： {url}， 超时时间： {timeout} 秒")
    def not_have_url(self, url: str, timeout=5) -> None:
        """
        断言：检查页面是否存在指定的 URL；不存在则通过，存在则失败；
        :param url: 页面标题，接受一个字符串参数或正则表达式参数
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证页面不存在URL： {url}")
        expect(self.page).not_to_have_url(url_or_reg_exp=url, timeout=timeout * 1000)

    # --------------------------------- 断言（可见与不可见） ---------------------------------#
    @allure.step("--> 断言 | 验证元素被可见 | 元素定位： {locator}")
    def is_element_visible(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证元素是否可见
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素被可见 | 元素定位： {locator}")
        
        if isinstance(locator,str):
            expect(self.page.locator(locator)).to_be_visible()
        else:
            expect(locator).to_be_visible()

    # --------------------------------- 断言（常用的断言方法） ---------------------------------#
    """
    expect(locator).to_be_checked()	Checkbox is checked
    expect(locator).to_be_disabled()	Element is disabled
    expect(locator).to_be_editable()	Element is enabled
    expect(locator).to_be_empty()	Container is empty
    expect(locator).to_be_enabled()	Element is enabled
    expect(locator).to_be_focused()	Element is focused
    expect(locator).to_be_hidden()	Element is not visible
    expect(locator).to_be_visible()	Element is visible
    expect(locator).to_contain_text()	Element contains text
    expect(locator).to_have_attribute()	Element has a DOM attribute
    expect(locator).to_have_class()	Element has a class property
    expect(locator).to_have_count()	List has exact number of children
    expect(locator).to_have_css()	Element has CSS property
    expect(locator).to_have_id()	Element has an ID
    expect(locator).to_have_js_property()	Element has a JavaScript property
    expect(locator).to_have_text()	Element matches text
    expect(locator).to_have_value()	Input has a value
    expect(locator).to_have_values()	Select has options selected
    expect(page).to_have_title()	Page has a title
    expect(page).to_have_url()	Page has a URL
    expect(api_response).to_be_ok()	Response has an OK status
    """

    @allure.step("--> 断言 | 验证元素checkbox被选中 | 元素定位： {locator}")
    def is_checkbox_checked(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证复选框是否被选中
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素checkbox被选中 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator,str):
            elem = self.page.locator(locator)
        expect(elem).to_be_checked()

    @allure.step("--> 断言 | 验证元素被禁用 | 元素定位： {locator}")
    def is_element_disabled(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证元素是否被禁用
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素被禁用 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_disabled()

    @allure.step("--> 断言 | 验证输入框可编辑 | 元素定位： {locator}")
    def is_input_editable(self, locator: Union[str,Locator], timeout=5) -> None:
        """
        断言：验证输入框是否可编辑
        :param locator: 元素定位
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证输入框可编辑 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_editable(timeout=timeout * 1000)

    @allure.step("--> 断言 | 验证容器为空 | 元素定位： {locator}")
    def is_container_empty(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证容器是否为空
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证容器为空 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_empty()

    @allure.step("--> 断言 | 验证元素为启用状态 | 元素定位： {locator}")
    def is_element_enabled(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证元素是否启用
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素为启用状态 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_enabled()

    @allure.step("--> 断言 | 验证元素获得焦点 | 元素定位： {locator}")
    def is_element_focused(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证元素是否获得焦点
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素获得焦点 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_focused()

    @allure.step("--> 断言 | 验证元素被隐藏 | 元素定位： {locator}")
    def is_element_hidden(self, locator: Union[str,Locator]) -> None:
        """
        断言：验证元素是否隐藏
        :param locator: 元素定位
        """
        logger.info(f"--> 断言 | 验证元素被隐藏 | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_be_hidden()

    @allure.step("--> 断言 | 验证输入框具有值(预期)： {value} | 元素定位： {locator}")
    def is_input_have_value(self, locator: Union[str,Locator], value: str, timeout=5) -> None:
        """
        断言：验证输入框是否具有指定的值
        :param locator: 元素定位
        :param value: 指定值
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证元素具有值(预期)： {value} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_value(value=value, timeout=timeout * 1000)

    @allure.step("--> 断言 | 验证输入框不具有值(预期)： {value} | 元素定位： {locator}")
    def is_input_not_have_value(self, locator: Union[str,Locator], value: str, timeout=5) -> None:
        """
        断言：验证输入框是否具有指定的值
        :param locator: 元素定位
        :param value: 指定值
        :param timeout: 超时时间， 默认5000ms
        """
        logger.info(f"--> 断言 | 验证元素具有值(预期)： {value} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).not_to_have_value(value=value, timeout=timeout * 1000)

    @allure.step("--> 断言 | 验证元素具有： {text} | 元素定位： {locator}")
    def have_text(self, locator: Union[str,Locator], text: str) -> None:
        """
        断言：验证元素是否具有指定的文本内容
        :param locator: 元素定位
        :param text: 文本内容
        """
        logger.info(f"--> 断言 | 验证元素具有： {text} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_text(text)

    @allure.step("--> 断言 | 验证元素包含： {text} | 元素定位： {locator}")
    def contain_text(self, locator: Union[str,Locator], text: str) -> None:
        """
        断言：验证元素是否包含指定的文本
        :param locator: 元素定位
        :param text: 文本内容
        """
        logger.info(f"--> 断言 | 验证元素包含： {text} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_contain_text(text)

    @allure.step("---> 断言 | 验证元素具有类属性(预期)： {class_name} | 元素定位： {locator}")
    def is_element_have_class(self, locator: Union[str,Locator], class_name: str) -> None:
        """
        断言：验证元素是否具有指定的类属性
        :param locator: 元素定位
        :param class_name: 预期类名称
        """
        logger.info(f"---> 断言 | 验证元素具有类属性(预期)： {class_name} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_class(class_name)

    @allure.step("--> 断言 | 验证元素具有属性(预期)： {attr_name} | 元素定位： {locator}")
    def is_element_have_attr(self, locator: Union[str,Locator], attr_name: str) -> None:
        """
        断言：验证元素是否具有指定的属性
        :param locator: 元素定位
        :param attr_name: 预期元素属性名称
        """
        logger.info(f"--> 断言 | 验证元素具有属性(预期)： {attr_name} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_attribute(attr_name)

    @allure.step("---> 断言 | 验证元素具有指定个数(预期)： {elem_count} | 元素定位： {locator}")
    def is_element_count(self, locator: Union[str,Locator], elem_count: int) -> None:
        """
        断言：验证元素个数是否与期望值相等
        :param locator: 元素定位
        :param elem_count: 预期元素个数
        """
        logger.info(f"---> 断言 | 验证元素具有指定个数(预期)： {elem_count} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_count(elem_count)

    @allure.step("---> 断言 | 验证元素具有CSS属性(预期)： {css_value} | 元素定位： {locator}")
    def is_element_have_css(self, locator: Union[str,Locator], css_value: Union[str, Pattern[str]]) -> None:
        """
        断言：验证元素个数是否与期望值相等
        :param locator: 元素定位
        :param css_value: css属性，接收str以及正则表达式， 例如"button"， 或者"display", "flex"
        """
        logger.info(f"---> 断言 | 验证元素具有CSS属性(预期)： {css_value} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_css(css_value)

    @allure.step("---> 断言 | 验证元素具有ID(预期)： {id_name} | 元素定位： {locator}")
    def is_element_have_id(self, locator: Union[str,Locator], id_name: str) -> None:
        """
        断言：验证元素是否具有指定的ID
        :param locator: 元素定位
        :param id_name: 元素id属性
        """
        logger.info(f"---> 断言 | 验证元素具有ID(预期)： {id_name} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_css(id_name)

    @allure.step("---> 断言 | 验证元素具有JavaScript属性(预期)： {js_value} | 元素定位： {locator}")
    def is_element_have_js_property(self, locator: Union[str,Locator], js_value: str) -> None:
        """
        断言：用于验证元素是否具有指定的JavaScript属性
        :param locator: 元素定位
        :param js_value: 元素id属性
        """
        logger.info(f"---> 断言 | 验证元素具有JavaScript属性(预期)： {js_value} | 元素定位： {locator}")
        elem = locator
        if isinstance(locator, str):
            elem = self.page.locator(locator)
        expect(elem).to_have_js_property(js_value)

    # --------------------------------- 断言（自定义） ---------------------------------#
    @allure.step("--> 断言 | 验证元素的属性 {attr_name} 具有值(预期)： {value} | 元素定位： {locator}")
    def is_element_attr_have_value(self, locator: Union[str,Locator], attr_name: str, value: str) -> None:
        """
        断言：验证元素的某个属性具有指定的值
        :param locator: 元素定位
        :param attr_name: 元素属性名称
        :param value: 文本内容
        """
        logger.info(f"--> 断言 | 验证元素的属性 {attr_name} 具有值(预期)： {value} | 元素定位： {locator}")
        actual_value = ""
        if isinstance(locator, str):
            actual_value = self.get_element_attribute(locator=locator, attr_name=attr_name)
        elif isinstance(locator, Locator):
            actual_value = locator.get_attribute(attr_name)
        logger.info(f"--> 验证元素的属性 {attr_name} 实际值： {actual_value}")
        assert value == actual_value

    # --------------------------------- 断言（判断页面元素状态checkbox和radio） ---------------------------------#
    """
    page对象调用的判断方法, 传一个selector 定位参数
        • page.is_checked(selector: str) # checkbox or radio 是否选中
        • page.is_disabled(selector: str) # 元素是否可以点击或编辑
        • page.is_editable(selector: str) # 元素是否可以编辑
        • page.is_enabled(selector: str) # 是否可以操作
        • page.is_hidden(selector: str) # 是否隐藏
        • page.is_visible(selector: str) # 是否可见
        
    locator 对象调用的判断方法
        • locator.is_checked()
        • locator.is_disabled()
        • locator.is_editable()
        • locator.is_enabled()
        • locator.is_hidden()
        • locator.is_visible()
    元素句柄 的判断方法
        • element_handle.is_checked()
        • element_handle.is_disabled()
        • element_handle.is_editable()
        • element_handle.is_enabled()
        • element_handle.is_hidden()
        • element_handle.is_visible()
    """

