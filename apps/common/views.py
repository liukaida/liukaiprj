# -*- coding=utf-8 -*-

import logging

from django.contrib import auth
from django.shortcuts import render_to_response

import services
from utils.check_auth import validate
from utils.check_param import InvalidHttpParaException, getp
from utils.const_err import SUCCESS
from utils.net_helper import response_parameter_error, response_exception, response200
from utils.utils_log import log_request, log_response

logger = logging.getLogger(__name__)


@validate('GET', auth=False)
def api_common_test(request):
    """
    功能说明: 测试函数
    """
    log_request(request)
    try:
        testparam1 = getp(request.GET.get('testparam1'), nullable=False, para_intro='测试参数1')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        result = services.api_common_test(request, testparam1)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, result)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


def page_common_root(request):
    """
    功能说明: 首页
    """
    return render_to_response('html/index.html')