# coding=utf-8
import assert_utils
from assert_utils import assert_code
from lib import api_wrapper

apis = api_wrapper.APIWrapper()
asserter = assert_utils.Asserter


class XlsTester:

    @staticmethod
    def test_with_xls_data(test_case_name, test_params, xls_data):
        """
        通用的<excle类型测试数据> 测试用例。
        :param test_case_name:
            被测方法名，对应api_wrapper中封装好的方法名。
        :param test_params:
            测试数据。
        :param xls_data:
            xls测试数据总字典。
        :return:
        """

        # 调用封装好的api
        # 举例： 在api_wrapper中封装了一个match的方法，
        #       response = match(test_params)
        response = test_case_name(test_params)
        print("*" * 66)

        print(response)

        # 校验状态码
        if test_params["expect_code"] != "":
            assert_code(response["code"], test_params["expect_code"])

        # 校验文本
        if test_params["expect_text"] != "":
            asserter.assert_text_contain(response["body"], test_params["expect_text"])

        # 如生成了其他步骤依赖的数据，反写回依赖处
        if test_params["return_value"] != "":
            parts = test_params["return_value"].split("=")
            var_name = parts[0]  # 要替换的字段名称 如token

            keys = parts[1].split("-")  # 需要替换的字段所在的位置 header Authorization
            value = response
            for key in keys:
                value = value[key]

            return xls_data.set_dependent_value(var_name, value)
