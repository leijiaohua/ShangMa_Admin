# coding=utf-8

import xlrd
import json

"""
使用xlrd读取excle的数据，并保存为字典形式
"""


class XlsData:
    # NO.    用例方法名    接口名    header参数    body参数    预期状态码    预期包含文本   依赖字段
    COL_CASE_ID = 0

    COL_CASE_NAME = 1
    COL_API_NAME = 2
    COL_METHOD = 3
    COL_HEADER = 4
    COL_BODY = 5
    COL_CODE = 6
    COL_EXPECT_TEXT = 7
    COL_RETURN_VALUE = 8

    # host总是在第一行
    ROW_HOST = 1
    COL_CONFIG_KEY = 1
    COL_CONFIG_VALUE = 2

    test_dict = {}
    config_dict = {}

    def __init__(self, xls_path, data_sheet="test_data", config_sheet="config"):
        self.data = xlrd.open_workbook(xls_path)
        self.case_table = self.data.sheet_by_name(data_sheet)
        self.row_num = self.case_table.nrows
        self.col_num = self.case_table.ncols

        self.config_table = self.data.sheet_by_name(config_sheet)

        self.__create_test_data_dict()

    def __get_config_dict(self):
        # 解析config工作表，获取每个接口对应的url
        config_dict = dict()
        host = self.config_table.cell_value(self.ROW_HOST, self.COL_CONFIG_VALUE)

        for i in range(2, self.config_table.nrows):
            api_name = self.config_table.cell_value(i, self.COL_CONFIG_KEY)
            api_path = self.config_table.cell_value(i, self.COL_CONFIG_VALUE)

            api_name = str(api_name).strip()
            api_path = str(api_path).strip()

            config_dict[api_name] = host + api_path

        return config_dict

    def get_case_by_name(self, case_name):
        return list(self.test_dict[case_name].values())

    def get_test_data_dict(self):
        return self.test_dict

    def __create_test_data_dict(self):
        """
        Contruct test data dict.
        :return:
        """
        if self.row_num <= 1:
            print("Empty test data")
            return

        config_dict = self.__get_config_dict()
        self.config_dict = config_dict

        test_dict = {}

        for i in range(1, self.row_num):
            test_case_id = self.case_table.cell_value(i, self.COL_CASE_ID)
            test_case_name = self.case_table.cell_value(i, self.COL_CASE_NAME)
            formatted_name = str(test_case_name).strip()

            if formatted_name == "":
                continue

            if formatted_name not in test_dict:
                test_dict[formatted_name] = {}

            detail_data_dict = {}
            api_name = self.case_table.cell_value(i, self.COL_API_NAME)
            body = self.case_table.cell_value(i, self.COL_BODY)
            header = self.case_table.cell_value(i, self.COL_HEADER)
            expect_code = self.case_table.cell_value(i, self.COL_CODE)
            expect_text = self.case_table.cell_value(i, self.COL_EXPECT_TEXT)
            return_value = self.case_table.cell_value(i, self.COL_RETURN_VALUE)

            detail_data_dict["url"] = config_dict[api_name]

            if body != "":
                body = body.replace("\n", "")
                # detail_data_dict["body"] = json.dumps(body, strict=False)
                detail_data_dict["body"] = body
            else:
                detail_data_dict["body"] = ""

            if header != "":
                header = header.replace("\n", "")
                # detail_data_dict["header"] = json.dumps(header, strict=False)
                detail_data_dict["header"] = header
            else:
                detail_data_dict["header"] = ""

            detail_data_dict["expect_code"] = expect_code
            detail_data_dict["expect_text"] = expect_text
            detail_data_dict["return_value"] = return_value

            test_dict[formatted_name][test_case_id] = detail_data_dict
            self.test_dict = test_dict

        return test_dict

    # 接口之间有依赖，使用此方法替换值
    @staticmethod
    def set_dependent_value(self, name, value):
        """

        :param self:
        :param name: need replace name
        :param value: need replace value
        :return: replaced dict

        """
        test_dict = self.test_dict
        var_to_repalce = "{{%s}}" % name
        value_to_replace = value

        # search target var name in test_dict
        for (case_name, case_data) in list(test_dict.items()):
            for (case_id, case_params) in list(case_data.items()):
                str_body = json.dumps(case_params["body"])
                str_header = json.dumps(case_params["header"])
                if var_to_repalce in str_body:
                    params = "body"
                    str_old_value = str_body
                elif var_to_repalce in str_header:
                    params = "header"
                    str_old_value = str_header
                else:
                    continue

                new_value = str(str_old_value).replace(var_to_repalce, value_to_replace)
                test_dict[case_name][case_id][params] = json.loads(new_value, strict=False)

        return test_dict


if __name__ == "__main__":
    path = "../admin_project/test_data.xls"
    c = XlsData(path)
    data = c.test_dict
    print(data["test_login"][1])
