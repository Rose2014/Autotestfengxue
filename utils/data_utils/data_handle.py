# -*- coding: utf-8 -*-
# @File    : data_handle.py
# @Software: PyCharm
# @Desc:
# 标准库导入
import random  # 导包不能移除，否则random.choice这种就不能处理了
import json
import re, uuid
import os
import base64
from datetime import datetime, timedelta
import copy
# 第三方库导入
from loguru import logger
from string import Template
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar
# 本地应用/模块导入
from utils.data_utils.faker_handle import FakerData
from utils.data_utils.eval_data_handle import eval_data
from utils.files_utils.files_handle import file_to_base64, filepath_to_base64, get_files
from config.path_config import FILES_DIR
from utils.tools.aes_encrypt_decrypt import Encrypt


class DataHandle:
    def __init__(self):
        # 实例化FakerData类，避免反复实例，提高性能。
        self.FakerDataClass = FakerData()
        # 获取FakerData类所有自定义方法
        self.method_list = [method for method in dir(FakerData) if
                            callable(getattr(FakerData, method)) and not method.startswith("__")]

    def process_cookie_jar(self, data):
        """
        将任意数据里的RequestsCookieJar，转成dict，再转换成JSON 格式的字符串（序列化）
        :param data: 待处理的数据
        """
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.process_cookie_jar(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = self.process_cookie_jar(item)
        elif isinstance(data, RequestsCookieJar):
            data = json.dumps(dict_from_cookiejar(data))
        return data

    def replace_and_store_placeholders(self, pattern, text, resultAsDict=True):
        """
        提取字符串中符合正则表达式的元素，同时用一个唯一的uuid来替换原有字符串
        例如：
        原字符串：user_id: ${user_id}, user_name: ${user_name}
        替换后的原字符串：user_id: e1c6fc74-2f21-49a9-8d0c-de16650c6364, user_name: 50c74155-5cb5-4809-bc5d-277addf8c3e7
        暂存的需要被处理的关键字或函数：{'e1c6fc74-2f21-49a9-8d0c-de16650c6364': {0: '${user_id}', 1: 'user_id'}, '50c74155-5cb5-4809-bc5d-277addf8c3e7': {0: '${user_name}', 1: 'user_name'}}
        """
        placeholders = {}

        def replace(match):
            placeholder = str(uuid.uuid4())  # 使用uuid生成唯一的占位符
            placeholders[placeholder] = {0: f'${match.group(1)}', 1: match.group(1)}  # 将提取到的字符串存储到字典中
            return placeholder

        # 使用正则表达式进行字符串匹配和替换，同时指定替换次数为 1
        replaced_text = re.sub(pattern, replace, text, count=1)
        while replaced_text != text:
            text = replaced_text
            replaced_text = re.sub(pattern, replace, text, count=1)

        if resultAsDict:
            return replaced_text, placeholders
        else:
            # 构造结果字符串
            result = '{\n'
            for key, value in placeholders.items():
                result += f"    '{key}': {{0: \"{value[0]}\", 1: \"{value[1]}\"}},\n"
            result += '}'
            return replaced_text, result

    def data_handle(self, obj, source=None):
        obj = copy.deepcopy(eval_data(obj))
        # obj = eval_data(obj)
        return self.data_handle_(obj, source)

    def data_handle_(self, obj, source=None):
        """
        递归处理字典、列表中的字符串，将${}占位符替换成source中的值
        """
        func = {}
        keys = {}

        source = {} if not source or not isinstance(source, dict) else source
        # logger.trace(f"source={source}")

        # 处理一下source，检测到里面存在RequestsCookieJar，转成dict，再转换成JSON 格式的字符串（序列化）。
        # 避免传递过来一个RequestsCookieJar，替换后变成了'RequestsCookieJar'，导致cookies无法使用的问题
        source = self.process_cookie_jar(data=source)

        # 如果进来的是字符串，先将各种类型的表达式处理完
        if isinstance(obj, str):
            # 先把python表达式找出来存着，这里会漏掉一些诸如1+1的表达式
            pattern = r"\${([^}]+\))}"  # 匹配以 "${" 开头、以 ")}" 结尾的字符串，并在括号内提取内容，括号内不能包含"}"字符
            obj, func = self.replace_and_store_placeholders(pattern, obj)

            # 模板替换
            should_eval = 0
            if obj.startswith("${") and obj.endswith("}"):
                if source.get(obj[2:-1]) and not isinstance(source[obj[2:-1]], str):
                    should_eval = 1
            obj = Template(obj).safe_substitute(source)
            if should_eval == 1:
                obj = eval_data(obj)

            if not isinstance(obj, str):
                return self.data_handle(obj)

            # 再找一遍剩余的${}跟第一步的结果合并，提取漏掉的诸如1+1的表达式(在此认为关键字无法替换的都是表达式，最后表达式也无法处理的情况就报错或者原样返回)
            pattern = r'\$\{([^}]+)\}'  # 定义匹配以"${"开头，"}"结尾的字符串的正则表达式
            obj, func_temp = self.replace_and_store_placeholders(pattern, obj)
            func.update(func_temp)
            # 进行函数调用替换
            obj = self.invoke_funcs(obj, func)
            if not isinstance(obj, str):
                return self.data_handle(obj)
            # 直接返回最后的结果
            return obj
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                obj[index] = self.data_handle(item, source)
            return obj
        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.data_handle(value, source)
            return obj
        else:
            return obj

    def invoke_funcs(self, obj, funcs):
        """
        调用方法，并将方法返回的结果替换到obj中去
        """
        for key, funcs in funcs.items():  # 遍历方法字典调用并替换
            func = funcs[1]
            # logger.debug("invoke func : ", func)
            try:
                if "." in func:
                    if func.startswith("faker."):
                        # 英文的faker数据：self.faker = Faker()
                        faker = self.FakerDataClass.faker
                        obj = self.deal_func_res(obj, key, eval(func))
                    elif func.startswith("fk_zh."):
                        # 中文的faker数据： self.fk_zh = Faker(locale='zh_CN')
                        fk_zh = self.FakerDataClass.fk_zh
                        obj = self.deal_func_res(obj, key, eval(func))
                    else:
                        obj = self.deal_func_res(obj, key, eval(func))
                else:
                    func_parts = func.split('(')
                    func_name = func_parts[0]
                    func_args_str = ''.join(func_parts[1:])[:-1]
                    if func_name in self.method_list:  # 证明是FakerData类方法
                        method = getattr(self.FakerDataClass, func_name)
                        res = eval(f"method({func_args_str})")  # 尝试直接调用
                        obj = self.deal_func_res(obj, key, res)
                    else:  # 不是FakerData类方法，但有可能是 1+1 这样的
                        obj = self.deal_func_res(obj, key, eval(func))
            except:
                logger.warning("Warn: --------函数：%s 无法调用成功, 请检查是否存在该函数-------" % func)
                obj = obj.replace(key, funcs[0])

        return obj

    def deal_func_res(self, obj, key, res):
        obj = obj.replace(key, str(res))
        try:
            if not isinstance(res, str):
                obj = eval(obj)
        except:
            msg = (f"\nobj --> {obj}\n"
                   f"函数返回值 --> {res}\n"
                   f"函数返回值类型 --> {type(res)}\n")
            logger.warning(
                f"\nWarn: --------处理函数方法后，尝试eval({obj})失败，可能原始的字符串并不是python表达式-------{msg}")
        return obj


def get_file_content(file_name):
    """
    获取文件二进制内容
    :param file_name: 文件名称
    :return:
    """
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.exists(file_path):
        # 如果文件是一个真实存在的路径，则返回文件二进制内容
        return file_to_base64(file_path=file_path)
    else:
        # 若文件不存在，则尝试以文件扩展名随机选择一个文件
        logger.warning(f"图片不存在，将获取传入文件名后缀，随机取对应类型的文件， 路径：{file_path}")
        file_extension = os.path.splitext(file_name)[1]
        files = get_files(target=FILES_DIR, end=file_extension)
        if files:
            # 返回文件二进制内容
            return file_to_base64(file_path=random.choice(files))
        else:
            logger.warning(f"找不到该文件后缀对应的同类型文件，将返回空， 传入的文件名：{file_name}")
            return None


def list_to_str(target):
    """
   将列表中的元素转换为字符串，并用逗号分隔。

   :param target: 要转换为字符串的列表。
   :return: 以逗号分隔的字符串。
   """
    if isinstance(target, list):
        # 过滤掉列表中的None值
        filtered_list = [str(item) for item in target if item is not None]
        # 使用逗号连接字符串
        return ",".join(filtered_list)
    else:
        return target


def string_to_base64(input_string: str):
    """
    将字符串转换为Base64格式
    """
    base64_bytes = base64.b64encode(input_string.encode('utf-8'))
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def str_to_list(target):
    """
    将字符串转换为列表，字符串中以逗号分隔的元素将转换为列表中的元素。
    """
    if isinstance(target, str):
        return [target]
    else:
        return target


def none_to_null(target):
    """
    将'None'转成空字符串
    """
    if target == 'None':
        return ""
    else:
        return target


def get_file_base64(file_name):
    """
    返回文文件内容的base64编码
    """
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.exists(file_path):
        # 如果文件是一个真实存在的路径，则返回base64编码内容
        return file_to_base64(file_path=file_path)
    else:
        logger.warning(f"找不到该文件，将返回空， 传入的文件名：{file_name}")
        return None


def get_filepath_base64(file_name):
    """
    返回文件路径的base64编码
    """
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.exists(file_path):
        # 如果文件是一个真实存在的路径，则返回base64编码内容
        return filepath_to_base64(file_path=file_path)

    else:
        logger.warning(f"找不到该文件，将返回空， 传入的文件名：{file_name}")
        return None


def get_base64_content(input_string: str):
    """
    获取base64编码内容
    """
    byte_string = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(byte_string)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def base64_decode(encoded_string):
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        return f"Error decoding: {str(e)}"


def update_wiki_sidebar(sidebar_content, new_page_name):
    """
    获取wiki sideber的base64编码内容，将新页面追加到后面，再重新编码返回
    """
    _sidebar_content = base64_decode(sidebar_content)
    new_sidebar_content = _sidebar_content + f"\n[[{new_page_name}]]"
    return string_to_base64(new_sidebar_content)


def get_current_week(start_or_end="start"):
    """
    获取当前日期，并根据参数返回本周的开始或结束日期。

    参数:
    - start_or_end: 字符串，指定返回本周的开始日期（"start"）还是结束日期（"end"）。

    返回:
    - 本周开始或结束日期的字符串表示，格式为"月日"（例如："01月01日"）。
    """
    # 获取当前日期
    today = datetime.today()
    # 计算今天是本周的第几天（0代表周一，1代表周二，以此类推）
    current_weekday = today.weekday()

    if start_or_end == "start":
        # 计算本周的周一
        res = today - timedelta(days=current_weekday)
    elif start_or_end == "end":
        # 计算本周的周日
        res = today - timedelta(days=current_weekday) + timedelta(days=6)
    else:
        # 如果参数非法，返回当前日期的周一
        logger.error(f"Invalid value for start_or_end: {start_or_end}. Defaulting to 'start'.")
        res = today - timedelta(days=current_weekday)

    return res.strftime("%m月%d日")


def aes_encrypt_data(target_str: str, ace_key):
    """
    使用AES-CBC对称加密算法对密码进行加密
    """
    ace = Encrypt(key=ace_key, iv=ace_key)
    return ace.aes_encrypt(target_str)


# 声明data_handle方法，这样外部就可以直接import data_handle来使用了
data_handle = DataHandle().data_handle
