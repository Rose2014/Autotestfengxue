# -*- coding: utf-8 -*-
# @File    : excel_handle.py
# @Software: PyCharm
# @Desc: 读取excel测试数据

from openpyxl import load_workbook
import os
import allure
from loguru import logger
from config.path_config import TEST_DATA_DIR
from utils.files_utils.files_handle import get_files

class ExcelHandle:
    def __init__(self):
        """
        初始化ExcelHandle类
        """
        self.workbook = None
        self.excel_files = get_files(TEST_DATA_DIR, end='.xlsx')

    @allure.step("读取测试类【{class_file}】的测试数据")
    def read_excel_file(self,class_file: str = None):
        """
        读取Excel文件
        :param class_file: 测试类文件路径，例如：testcases/system_config/test_system_manager.py
        """
        try:
            class_file_name = os.path.splitext(os.path.basename(class_file))[0]
            sheet_dict = {}
            for file in self.excel_files:
                print(f"file: {file}")
                if class_file_name in file:
                    self.workbook = load_workbook(file, data_only=True)
                    worksheet_names = self.workbook.sheetnames
                    for sheet_name in worksheet_names:
                        sheet = self.workbook[sheet_name]
                        rows = list[str](sheet.rows)
                        # 获取标题行
                        titles = [i.value for i in rows[0]]
                        sheet_data = []
                        for item in rows[1:]:
                            # 将单元格值转换为字符串，特别是布尔值
                            values = [str(i.value) if i.value is not None else None for i in item]
                            sheet_data.append(dict(zip(titles, values)))
                        sheet_dict[sheet_name] = sheet_data
            
            self.close()
            # print(f"sheet_dict: {sheet_dict}")
            logger.info(f"sheet_dict: {sheet_dict}")
            return sheet_dict
        except Exception as e:
            print(f"读取Excel文件出错: {e}")
            self.close()
            return None

    def close(self):
        """
        关闭工作簿
        """
        if self.workbook:
            self.workbook.close()
    


# 测试主方法
if __name__ == "__main__":
    """
    测试主方法，可直接运行
    示例用法：python excel_handle.py
    """
    import sys
    import os
    
    # 将项目根目录添加到Python搜索路径
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # 示例1：使用默认Excel文件
    print("=== 示例1：使用默认Excel文件 ===")
    try:
        excel_handle = ExcelHandle()
        sheet_dict = excel_handle.read_excel_file("test_system_manager")
        print(sheet_dict)
    except Exception as e:
        print(f"示例1出错: {e}")
    
