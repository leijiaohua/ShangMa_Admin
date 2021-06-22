# coding=utf-8
import sys
import os

admin_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(admin_root)

from projects_core import http_method
from xlrd_xls import XlsData


# sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("ShangMa_Admin")[0])


class APIWrapper:
    requester = None  # [MUST HAVE] init requester to handle post/get http request

    def __init__(self):
        self.requester = http_method.HttpMethod

    def login(self, test_data_dict):
        """
        测试数据存储在.xls文件中.

        :param test_data_dict:
            解析.xls生成的测试数据（dict类型）
            包括：
                test_data_dict["url"]
                test_data_dict["body"]
                test_data_dict["header"]
                test_data_dict["data"]
                test_data_dict["return value"]
        :return:
            response
        """
        response = self.requester.get_request(url=test_data_dict["url"],
                                              headers=test_data_dict["header"],
                                              json_data=test_data_dict["body"])
        return response


if __name__ == "__main__":
    api = APIWrapper()
    path = "../data/test_data.xls"
    c = XlsData(path)
    data = c.get_case_by_name("test_login")
    test_dict = data[0]

    res = api.login(test_dict)
    print(res["text"])
