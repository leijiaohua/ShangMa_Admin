# coding=utf-8
import sys
import os
import pytest

admin_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(admin_root)

from admin_project.api_wrapper import APIWrapper
from common import xlrd_xls
from admin_project.xls_tester import XlsTester
from common import assert_utils

asserter = assert_utils.Asserter
apis = APIWrapper()

"""
1、对于模块和代码不在同一目录的情况下，在脚本开头加上sys.path.append("模块路径")，把路径添加到系统的环境变量。
   环境变量的内容会自动添加到模块搜索路径中
"""


# admin_project_root = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
# sys.path.append(admin_project_root)


class TestXlsData:
    # (xls文件路径)
    test_data = xlrd_xls.XlsData("test_data.xls")

    xls_data = None

    def __test_with_xls_data(self, func, test_data_list):
        """

        :param func:
        :param test_data_list:
        :return:
        """
        self.xls_data = XlsTester.test_with_xls_data(func, test_data_list, self.test_data)

    @pytest.mark.HIGH
    @pytest.mark.LOGIN
    @pytest.mark.parametrize("test_data", test_data.get_case_by_name("test_login"))  # test_match为xls文件中的测试用例名
    def test_match(self, test_data):
        """
        假设新增的测试用例方法名为test_aaa，用来测试api_wrapper中封装好的aaa()方法，需要做以下几件事情，
        0. copy paste test_login 的全部内容，给你的新方法起一个合适的名字，替换替换掉test_login这个方法
            注意命名规则应遵守：test_<模块名>_<被测接口>_<测试场景>
        1. 标注中
               @pytest.maker.parametrize("test_data", test_data.get_case_by_name(”<此处替换为测试用例名>“))
            -->@pytest.maker.parametrize("test_data", test_data.get_case_by_name(”test_aaa“))
        2. 方法体中：
               self.__test_with_xls_data(<这里替换为api_wrapper里面测试的方法名>， test_data)
            -->self.__test_with_xls_data(api.aaa， test_data)

        :param test_data:
        :return:
        """
        self.__test_with_xls_data(apis.login, test_data)


if __name__ == "__main":
    pytest.main(["-s", "test_suite.py", "--html", "./report.html"])
