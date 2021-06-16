# coding=utf-8
import requests
import time

from Log import log_request
from Log import log_response

import logging
logger = logging.getLogger(__name__)


class HttpMethod:
    TIMEOUT = 5

    def __init__(self):
        pass

    @staticmethod
    def login(self, username, password):
        pass

    @staticmethod
    def get_response_dict(response, start_time):
        """
        Format response body to a dict structure.
        :param response:
        :param start_time:
        :return:
        """
        # response time , unit is ms
        time_consuming = response.elapsed.microseconds / 1000000
        # response time , unit is second
        time_total = response.elapsed.total_seconds()

        response_dict = dict()
        response_dict["code"] = response.status_code

        try:
            response_dict["header"] = response.headers
        except Exception as e:
            logger.debug("Invaild or empty header %s", str(e))
            response_dict["header"] = ""

        try:
            response_dict["body"] = response.json()
        except Exception as e:
            logger.debug("Invaild or empty body %s", str(e))
            response_dict["body"] = ""

        try:
            response_dict["cookies"] = response.cookies
        except Exception:
            response_dict["cookies"] = None

        response_dict["text"] = response.text
        response_dict["time_consuming"] = time_consuming
        response_dict["time_total"] = time_total
        response_dict["start_time"] = start_time
        response_dict["end_time"] = time.time()

        return response_dict

    @staticmethod
    def get_request(url,
                    headers=None,
                    params=None,
                    json_data=None,
                    data=None,
                    cookies=None,
                    timeout=TIMEOUT):
        """
        get request
        :param url:
        :param headers:
        :param params:
        :param json_data:
        :param data:
        :param cookies:
        :param timeout:
            timeout in seconds
        :return:
            response dict, including:
            response{
                "code":
                "header":
                "body":
                "text":
                "time_consuming": cost time, unit is
                "time_total":
            }
        """
        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            start_time = time.time()
            response = requests.get(url,
                                    headers=headers,
                                    params=params,
                                    json=json_data,
                                    data=data,
                                    cookies=cookies,
                                    timeout=timeout)
            log_request("GET", url, json_data, headers, data)
        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        response_dict = HttpMethod.get_response_dict(response, start_time)
        log_response(response_dict)

        return response_dict

    @staticmethod
    def post_request(url,
                     headers=None,
                     params=None,
                     json_data=None,
                     data=None,
                     cookies=None,
                     allow_redirects=False,
                     files=None,
                     timeout=TIMEOUT):
        """
        post request
        :param url:
        :param headers:
        :param params:
        :param json_data:
        :param data:
        :param cookies:
        :param allow_redirects: 默认禁止重定向
        :param files:
        :param timeout:
        :return:
        """
        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            start_time = time.time()
            response = requests.post(url,
                                     headers=headers,
                                     params=params,
                                     json=json_data,
                                     data=data,
                                     cookies=cookies,
                                     allow_redirects=allow_redirects,
                                     files=files,
                                     timeout=timeout)
            log_request("POST", url, json_data, headers, data)
        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        response_dict = HttpMethod.get_response_dict(response, start_time)
        log_response(response_dict)

        return response_dict

    @staticmethod
    def put_request(url,
                    headers=None,
                    json_data=None,
                    data=None,
                    timeout=TIMEOUT):
        """
        Put request.
        :param url:
        :param headers:
        :param json_data:
        :param data:
        :param timeout:
        :return:
        """

        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            start_time = time.time()
            response = requests.put(url,
                                    headers=headers,
                                    json=json_data,
                                    data=data,
                                    timeout=timeout)
            log_request("PUT", url, json_data, headers, data)
        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        response_dict = HttpMethod.get_response_dict(response, start_time)
        log_response(response_dict)

        return response_dict

    @staticmethod
    def delete_request(url,
                       headers=None,
                       json_data=None,
                       data=None,
                       timeout=TIMEOUT):
        """
        Put request.
        :param url:
        :param headers:
        :param json_data:
        :param data:
        :param timeout:
        :return:
        """

        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            start_time = time.time()
            response = requests.delete(url,
                                       headers=headers,
                                       json=json_data,
                                       data=data,
                                       timeout=timeout)
            log_request("DELETE", url, json_data, headers, data)
        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        response_dict = HttpMethod.get_response_dict(response, start_time)
        log_response(response_dict)

        return response_dict

    @staticmethod
    def download_request(url,
                         path,
                         headers=None,
                         params=None,
                         json_data=None,
                         data=None,
                         timeout=TIMEOUT):
        """
        Put request.
        :param params:
        :param path:
        :param url:
        :param headers:
        :param json_data:
        :param data:
        :param timeout:
        :return:
        """

        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            response = requests.get(url,
                                    headers=headers,
                                    params=params,
                                    json=json_data,
                                    data=data,
                                    timeout=timeout)
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            log_request("DOWNLOAD", url, json_data, headers, data)

        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        return path

    @staticmethod
    def download_by_post(url,
                         path,
                         headers=None,
                         params=None,
                         json_data=None,
                         data=None,
                         timeout=TIMEOUT):
        """
        Put request.
        :param params:
        :param path:
        :param url:
        :param headers:
        :param json_data:
        :param data:
        :param timeout:
        :return:
        """

        if not str(url).startswith("http://"):
            url = "%s%s" % ("http://", url)

        try:
            log_request("POST DOWNLOAD", url, json_data, headers, data)
            response = requests.post(url,
                                     headers=headers,
                                     params=params,
                                     json=json_data,
                                     data=data,
                                     timeout=timeout)
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)

        except requests.RequestException:
            logger.debug(f"RequestException url: {url}")
            raise
        except Exception as e:
            logger.error(str(e))
            raise Exception

        return path
