# coding=utf-8
import logging
import json
import os
import sys

admin_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(admin_root)

logger = logging.getLogger(__name__)

INDENT = 4


def log_request(request_type, url, json_data=None, header=None, data=None, extra_msg=None):
    if json_data:
        formatted_data = json.dumps(json_data, indent=INDENT, ensure_ascii=False)
    else:
        formatted_data = "No json parameters."
    info_msg = f"[REQUEST] {request_type} url: {url}\n params: {formatted_data}"

    if data:
        formatted_raw_data = json.dumps(data, indent=INDENT, ensure_ascii=False)
        info_msg += f"\n {request_type} data: {formatted_raw_data}"

    if header:
        formatted_header = json.dumps(header, indent=INDENT, ensure_ascii=False)
        info_msg = f"{info_msg}\n header: {formatted_header}"

    if extra_msg:
        info_msg += f"\n {extra_msg}"

    logger.info(info_msg)


def log_response(response_dict):
    str_body = json.dumps(response_dict["body"], indent=INDENT, ensure_ascii=False)
    code = str(response_dict["code"])
    logger.info(f"[RESPONSE] code: {code}\n body: {str_body}")

    if "cookies" in response_dict and response_dict["cookies"]:
        logger.info("cookies:")
        for k, v in list(response_dict["cookies"].items()):
            logger.info(f"{k} - {v}")
