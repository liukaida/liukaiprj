# -*- coding=utf-8 -*-

import logging

from django.contrib import auth

import services
from utils.check_auth import validate
from utils.check_param import InvalidHttpParaException, getp
from utils.const_err import SUCCESS, ERR_LOGIN_FAIL
from utils.net_helper import response_parameter_error, response_exception, response200
from utils.utils_log import log_request, log_response
from django.contrib.auth import logout

logger = logging.getLogger(__name__)


@validate("POST", auth=False)
def api_login(request):
    log_request(request)
    try:
        username = getp(request.POST.get("username"), u"用户名", nullable=True)
        password = getp(request.POST.get("password"), u"密码", nullable=True)
        confirm_code = getp(request.GET.get('confirm_code'), nullable=True, para_intro='用户确认码')
    except InvalidHttpParaException as ex:
        logger.exception(ex)
        return response_parameter_error(ex)
    try:
        if confirm_code:
            # 如果传了confirm_code则直接用确认码进行登陆
            if services.api_confirmcode_login(request, confirm_code):
                return response200({"c": SUCCESS[0], "m": SUCCESS[1]})
            else:
                return response200({"c": ERR_LOGIN_FAIL[0], "m": ERR_LOGIN_FAIL[1]})

        if services.login(request, username=username, password=password):
            result = {"c": SUCCESS[0], "m": SUCCESS[1]}
            log_response(request, result)
            response = response200(result)
            return response
        else:
            result = {"c": ERR_LOGIN_FAIL[0], "m": ERR_LOGIN_FAIL[1]}
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, result)
    return response200(result)


@validate("POST")
def api_logout(request):
    log_request(request)
    try:
        logout(request)
        response = response200(dict(c=SUCCESS[0], m=SUCCESS[1]))
        response.delete_cookie('account')
        return response
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex)
    # log_response(request, {})
    # return response200(dict(c=SUCCESS[0], m=SUCCESS[1]))


@validate("POST")
def api_add_account(request):
    log_request(request)
    try:
        username = getp(request.POST.get("username"), u"用户名", nullable=False)
        name = getp(request.POST.get("name"), u"姓名", nullable=False)
        sex = getp(request.POST.get("sex"), u"性别", nullable=False)
        activity_mask = getp(request.POST.get("activity_mask"), u"创建活动的掩码", nullable=True)
        area_id = getp(request.POST.get("area_id"), u"区域的id", nullable=True)
    except InvalidHttpParaException as ex:
        logger.exception(ex)
        return response_parameter_error(ex)
    try:
        result = services.add_account(request.user, username, name, sex, activity_mask, area_id)
    except Exception as ex:
        logger.exception(ex)
        return response_exception(ex, ex.message)
    log_response(request, result)
    return response200(result)
