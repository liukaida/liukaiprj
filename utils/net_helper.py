# -*- coding: utf-8 -*-

import os
import platform
import socket
import json
import logging
import urllib
import uuid
from urlparse import urlparse, urljoin, parse_qs
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.utils import http

from utils.const_def import *
from utils.const_err import *


logger = logging.getLogger(__name__)


def get_host_ip():
    """
        获取当前IP地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def response200(result):
    """
        OK
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response400(result):
    """
        bad request
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=400)


def response403(result):
    """
        Fobbidden
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=403)


def response405(result):
    """
        Method not allowed
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json', status=405)


def response_exception(exception, msg=''):
    from utils.utils_except import BusinessException
    if isinstance(exception, BusinessException):
        final_message = exception.msg
        if msg:
            final_message = u'%s, 原因: %s' % (msg, exception.msg)
        result = {'c': exception.code, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
    else:
        # final_message = u'请求失败' + exception.message
        final_message = exception.message
        if msg:
            final_message = msg
        result = {'c': -1, 'm': final_message}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


def response_parameter_error(exception):
    dict_resp = {"c": REQUEST_PARAM_ERROR[0], "m": exception.message}
    return response400(dict_resp)


def url_with_scheme_and_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return domain


def url_with_location(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def gen_url_with_fname(url, original_fname):
    """
        生成带有?fname=xxx格式的URL，使得nginx可以增加指定文件名的响应头
    """
    if not url or not original_fname:
        return ''
    (shortname, extension) = os.path.splitext(original_fname)
    return '%s?fname=%s' % (url, shortname)


def get_mac():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])


def get_mac_last4():
    return ''.join(get_mac().split(':'))[-4:]


def get_file_url(domain, filename):
    """
    将域名和文件名拼成URL
    :param domain: 域名
    :param filename: 文件
    :return: 拼好的URL
    """
    if not filename:
        return ''
    return urljoin(domain, filename)


def gen_file_reponse(file_path):
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/vnd.ms-excel')
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Encoding'] = 'utf-8'
    response['Content-Disposition'] = 'attachment;filename=%s' % os.path.basename(file_path)
    return response


def get_url_domain(url):
    proto, rest = urllib.splittype(url)
    res, rest = urllib.splithost(rest)
    return res


def get_cur_domain(request):
    """
    获取当前请求的域名
    :param request: view的request
    :return:
    """
    return request.META.get('HTTP_HOST', "")


def get_url_qs(url):
    """
    把get参数解决为字典
    如url="http://www.google.com/search?hl=en&q=urlparse&btnG=" 返回{'q': ['urlparse'], 'btnG': [''], 'hl': ['en']}
    :param url:
    :return:注意，返回结果中value为数组
    """
    parsed_tuple = urlparse(url)
    return parse_qs(parsed_tuple.query, True)
