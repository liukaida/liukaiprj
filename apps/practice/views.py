# -*- coding=utf-8 -*-

import logging
import uuid

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response

import services
from apps.practice.pinyinservice import get_pinyin_excel
from utils.check_auth import validate
from utils.check_param import InvalidHttpParaException, getp
from utils.const_err import SUCCESS
from utils.net_helper import response_parameter_error, response_exception, response200
from utils.utils_log import log_request, log_response

logger = logging.getLogger(__name__)


@validate('GET', auth=False)
def api_practice_pinyin(request):
    """
    功能说明: 下载拼音练习EXCEL
    """
    log_request(request)
    try:
        has_hanzi = getp(request.GET.get('has_hanzi'), nullable=True, para_intro='仅显示汉字拼音，不要格式')  # 勾上为on，不勾不会传这个参数
        words = getp(request.GET.get('words'), nullable=False, para_intro='中文单词列表')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        excel_filename=r'temp/%s.xls' % uuid.uuid1()
        result = get_pinyin_excel(words, excel_filename, has_hanzi)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, result)

    file = open(excel_filename, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="quiz.xls"'
    return response


@validate('GET', auth=False)
def api_practice_create_quest(request):
    """
    功能说明: 创建题目
    """
    log_request(request)
    try:
        quest_type = getp(request.GET.get('quest_type'), nullable=False, para_intro='生成题目类型')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        result = services.api_practice_create_quest(request, quest_type)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, result)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('GET', auth=False)
def api_practice_list_quest(request):
    """
    功能说明: 题目列表
    """
    log_request(request)
    try:
        quest_type = getp(request.GET.get('quest_type'), nullable=False, para_intro='生成题目类型')
        num = getp(request.GET.get('num'), nullable=False, para_intro='题目数量')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        result = services.api_practice_list_quest(request, quest_type, num)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, result)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


@validate('POST', auth=False)
def api_practice_answer_commit(request):
    """
    功能说明: 提交答题结果
    """
    log_request(request)
    try:
        user_name = getp(request.POST.get('user_name'), nullable=False, para_intro='用户姓名')
        question_uuid = getp(request.POST.get('question_uuid'), nullable=False, para_intro='当次题目唯一标识')
        question_count_total = getp(request.POST.get('question_count_total'), nullable=False, para_intro='题目总数')
        question_count_err = getp(request.POST.get('question_count_err'), nullable=False, para_intro='错题总数')
        useranswer_detail = getp(request.POST.get('useranswer_detail'), nullable=False, para_intro='用户答案详情JSON')
        duration = getp(request.POST.get('duration'), nullable=False, para_intro='时长')
        quest_type = getp(request.POST.get('quest_type'), nullable=False, para_intro='题目类型')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        result = services.api_practice_answer_commit(request.user, user_name, question_uuid, question_count_total, question_count_err,
                                                     useranswer_detail, duration, quest_type)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, result)
    return response200({'c': SUCCESS[0], 'm': SUCCESS[1], 'd': result})


def page_practice_home(request):
    """
    功能说明: 练习题首页
    """
    return render_to_response('html/practice/home.html')


def page_practice_pinyin(request):
    """
    功能说明: 练习题首页
    """
    return render_to_response('html/practice/pinyin.html')


def page_practice_list_quest(request):
    """
    功能说明: 题目列表页面
    """
    log_request(request)
    try:
        quest_type = getp(request.GET.get('quest_type'), nullable=False, para_intro='生成题目类型')   # 多种类型以逗号隔开
        num = getp(request.GET.get('num'), nullable=False, para_intro='题目数量')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        params = services.get_quest_list_page_param(request, quest_type, num)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, params)
    return render_to_response('html/practice/index.html', params)


def page_practice_list_answer_his(request):
    """
    功能说明: 查看历史答题记录页面
    """
    log_request(request)
    try:
        user_name = getp(request.GET.get('username'), nullable=True, para_intro='用户姓名', default='')
        days = getp(request.GET.get('days'), nullable=False, para_intro='最近天数', default='7')

    except InvalidHttpParaException as ihpe:
        logger.exception(ihpe)
        return response_parameter_error(ihpe)

    try:
        params = services.get_practice_list_answer_his(request, user_name, days)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)
    log_response(request, params)
    return render_to_response('html/practice/answer_his.html', params)
