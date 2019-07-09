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


def page_common_test(request):
    """
    功能说明: page页面
    """
    log_request(request)
    try:
        quest_type = getp(request.GET.get('quest_type'), nullable=True, para_intro='生成题目类型')
        num = getp(request.GET.get('num'), nullable=True, para_intro='题目数量')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        params = services.page_common_test(request, quest_type, num)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, params)
    return render_to_response('html/test.html', params)


from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from wechatpy import parse_message, create_reply
# from wechatpy.exceptions import InvalidSignatureException
# from wechatpy.utils import check_signature

WECHAT_TOKEN = '111111'


@csrf_exempt
def wechat(request):
    pass
    # if request.method == 'GET':
    #     signature = request.GET.get('signature', '')
    #     timestamp = request.GET.get('timestamp', '')
    #     nonce = request.GET.get('nonce', '')
    #     echo_str = request.GET.get('echostr', '')
    #     print 'weixin get connect ok'
    #     try:
    #         check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
    #     except InvalidSignatureException:
    #         echo_str = 'error'
    #     response = HttpResponse(echo_str, content_type="text/plain")
    #     return response
    # elif request.method == 'POST':
    #     print 'weixin post connect ok'
    #     msg = parse_message(request.body)
    #     if msg.type == 'text':
    #         reply = create_reply('这是条文字消息<a href="ok">aaa</a>', msg)
    #     elif msg.type == 'image':
    #         reply = create_reply('这是条图片消息', msg)
    #     elif msg.type == 'voice':
    #         reply = create_reply('这是条语音消息', msg)
    #     else:
    #         reply = create_reply('这是条其他类型消息', msg)
    #     response = HttpResponse(reply.render(), content_type="application/xml")
    #     return response
    # else:
    #     logger.info('--------------------------------')
