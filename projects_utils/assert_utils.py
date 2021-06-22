# coding=utf-8
import json
import sys
import importlib

importlib.reload(sys)


class Asserter:

    def __init__(self):
        pass

    @staticmethod
    def assert_body_attr(body, attr_name, expect_value, ignore_case=False):
        """
        verify value of a specified body attribute. body[body_attr] == expect_value
        :param body: response body in dict
        :param attr_name: attribute name to verify
        :param expect_value: expect text contained by value of @body_attr.
        :param ignore_case: ignore letter case or not; if True, "aaa" == "AAA"
        :return:
        """
        if attr_name in body:
            msg = str(body[attr_name])
            if ignore_case:
                msg = msg.lower()
                expect_value = str(expect_value).lower()
            error_msg = ("[FAIL] Wrong body message, expect: [%s], actual: [%s]"
                         % (expect_value, msg))
            assert msg == expect_value, error_msg
        else:
            error_msg = "[FAIL] Invalid body atttribute: %s" % attr_name
            raise ValueError(error_msg)

    @staticmethod
    def assert_body_attr_contains(body, attr_name, exxpect_text, ignore_case=False):
        # type: (object, object, object, object) -> object
        """
        Verify body[body_attr] contains @expect_text
        :param body: response body in dict
        :param attr_name: attribute name to verify
        :param exxpect_text: expect text contained by value of @body_attr.
        :param ignore_case: ignore letter case or not; if True, "aaa" == "AAA"
        :return:
        """
        if attr_name in body:
            attr_value = str(body[attr_name])
            if ignore_case:
                attr_value = attr_value.lower()
                expect_text = str(exxpect_text).lower()
            error_msg = ("[FAIL] failed to find text [%s] in attribute value [%s]"
                         % (exxpect_text, attr_value))
            assert expect_text in attr_value, error_msg
        else:
            error_msg = "[FAIL] Invalid body attribute: %s" % attr_name
            raise ValueError(error_msg)

    @staticmethod
    def assert_text_contain(body, expect_text, ignore_case=False):
        # type: (object, object, object) -> object
        """
        Verify response body contains @expect_text
        :param body:
        :param expect_text:
        :param ignore_case:
        :return:
        """
        expect_text = str(expect_text)
        if ignore_case:
            expect_text = expect_text.lower()

        text = json.dumps(body, ensure_ascii=False).lower()
        error_msg = ("[FAIL] Failed to find expect text [%s] in response body [%s]."
                     % (expect_text, text))
        assert expect_text in text, error_msg


@staticmethod
def assert_code(code, expect_code):
    # type: (object, object) -> object
    """
    Verify response status code.
    :param code:
    :param expect_code:
    :return:
    """
    error_msg = "[FAIL] Wrong status code, expect: [%s], actual: [%s]" % (expect_code, code)
    assert code == expect_code, error_msg
