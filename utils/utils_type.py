# -*- coding=utf-8 -*-

import types

from utils.const_def import *


def is_string(data):
    return isinstance(data, basestring)


def not_null_string(data, default=''):
    """
        将None和数值型转化为String
    """
    if isinstance(data, types.NoneType):
        return default
    elif isinstance(data, types.IntType) or isinstance(data, types.FloatType):
        return str(data)
    else:
        return data


def datetime2str(datetime_para, format=DEFAULT_FORMAT_DATETIME):
    """
        时间转字符串
    """
    if not datetime_para:
        return ''
    return datetime_para.strftime(format)


def bool2str(bool_para):
    """
        布尔值转字符串
    """
    return '1' if bool_para else '0'


def str2bool(str_para):
    """
        字符串转布尔值
    """
    return False if str_para == '0' else True


def smart_unicode(raw):
    if not isinstance(raw, unicode) and not isinstance(raw, str):
        return str(raw).decode('utf8')
    elif isinstance(raw, str):
        return raw.decode('utf8')
    elif isinstance(raw, unicode):
        return raw
    else:
        return None


def float2str(data, decimal):
    """
        将传入的浮点数字，转换为指定小数位的浮点字符串，由于round函数有时会显示有问题
        :type data: 浮点数字(字符串或float类型)
        :type decimal: 小数位数
    """
    formatstr = "%%.%df" % decimal
    return formatstr % data


def is_mobile(login_name):
    if len(login_name) != 11 or not login_name.isdigit():
        return False
    else:
        return True
