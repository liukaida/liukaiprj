# -*- coding=utf-8 -*-

import json
import re
import types

from django.conf import settings

from utils.utils_type import smart_unicode


class InvalidHttpParaException(Exception):
    def __init__(self, description):
        super(InvalidHttpParaException, self).__init__(description)


_para_check_map = {
    'INT': u'必须是整数',
    'INT_NONNEGATIVE': u'必须是非负整数',
    'INT_POSITIVE': u'必须是正整数',
    'INT_IN_RANGE': u'超出了允许范围',
    'SEQ': u'必须是逗号分隔的序列',
    'SEQ_INT': u'必须是逗号分隔的整型序列',
    'CHOICES': u'超出了允许范围',
    'MAX_LENGTH': u'字符长度超出了范围',
    'IMAGE': u'图片类型不支持或图片大小超出限制',
    'VOICE': u'语音类型不支持或语音大小超出限制',
    'VIDEO': u'视频类型不支持或视频大小超出限制',
    'FILE': u'附件类型不支持或附件大小超出限制',
    'JSON': u'不是合法的json格式字符串',
    'USER_TUPLES': u'不是合法的用户类型格式'
}


def getp(para, para_intro, nullable=False, default=None, check=None, **valid_check_para):
    """
        统一请求入参检查方法
        注意：默认不允许请求入参为空 nullable=False
    """
    if None is para or '' == para:
        if not nullable:
            raise InvalidHttpParaException(u'请求参数 %s 不能为空' % para_intro)
        else:
            return default

    if check:
        err_desc = _para_check_map[check.__name__]
        # 校验函数只有一个
        if type(check) == types.FunctionType:
            if not check(para, **valid_check_para):
                raise InvalidHttpParaException(u'%s%s' % (para_intro, err_desc))
        # 校验函数有多个（元组或者列表）
        elif type(check) == types.TupleType or type(check) == types.ListType:
            for each_check in check:
                if callable(each_check) and not each_check(para, **valid_check_para):
                    raise InvalidHttpParaException(u'%s%s' % (para_intro, err_desc))
    return para


def SEQ(para, **valid_check_para):
    return re.match(r'^\w+(,\w+)*(,)?$', para)


def SEQ_INT(para, **valid_check_para):
    return re.match(r'^\d+(,\d+)*(,)?$', para)


def USER_TUPLES(para, **valid_check_para):
    return re.match(r'^\d+,\d+,\d+(;\d+,\d+,\d+)*(;)?$', para)


def JSON(para, **valid_check_para):
    try:
        json.loads(para)
    except ValueError as e:
        return False
    return True


def IMAGE(para, **valid_check_para):
    """
        检查传入参数是否是图像文件
    """
    if '*' in settings.UPLOAD_IMAGE_EXTENSION:
        ext_ok = True
    else:
        ext = para.name[para.name.rfind('.') + 1:]
        if ext.lower() not in settings.UPLOAD_IMAGE_EXTENSION:
            ext_ok = False
        else:
            ext_ok = True
    if para.size > settings.UPLOAD_IMAGE_SIZE:
        size_ok = False
    else:
        size_ok = True
    return ext_ok and size_ok


def VOICE(para, **valid_check_para):
    """
        检查传入参数是否是语音文件
    """
    if '*' in settings.UPLOAD_VOICE_EXTENSION:
        ext_ok = True
    else:
        ext = para.name[para.name.rfind('.') + 1:]
        if ext.lower() not in settings.UPLOAD_VOICE_EXTENSION:
            ext_ok = False
        else:
            ext_ok = True
    if para.size > settings.UPLOAD_VOICE_SIZE:
        size_ok = False
    else:
        size_ok = True
    return ext_ok and size_ok


def VIDEO(para, **valid_check_para):
    """
        检查传入参数是否是视频文件
    """
    if '*' in settings.UPLOAD_VIDEO_EXTENSION:
        ext_ok = True
    else:
        ext = para.name[para.name.rfind('.') + 1:]
        if ext.lower() not in settings.UPLOAD_VIDEO_EXTENSION:
            ext_ok = False
        else:
            ext_ok = True
    if para.size > settings.UPLOAD_VIDEO_SIZE:
        size_ok = False
    else:
        size_ok = True
    return ext_ok and size_ok


def FILE(para, **valid_check_para):
    """
        检查传入参数是否是文件
    """
    if '*' in settings.UPLOAD_FILE_EXTENSION:
        ext_ok = True
    else:
        ext = para.name[para.name.rfind('.') + 1:]
        if ext.lower() not in settings.UPLOAD_FILE_EXTENSION:
            ext_ok = False
        else:
            ext_ok = True
    if para.size > settings.UPLOAD_FILE_SIZE:
        size_ok = False
    else:
        size_ok = True
    return ext_ok and size_ok


def INT(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是整型
    """
    try:
        int(para)
    except ValueError:
        return False
    else:
        return True


def INT_NONNEGATIVE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是非负整数
    """
    try:
        int_value = int(para)
    except ValueError:
        return False
    else:
        return int_value >= 0


def INT_POSITIVE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是正整数
    """
    try:
        int_value = int(para)
    except ValueError:
        return False
    else:
        return int_value > 0


def INT_IN_RANGE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是在某一范围的整型
    """
    try:
        int_value = int(para)
    except ValueError:
        return False
    else:
        return True if int_value in range(valid_check_para.get('min'), valid_check_para.get('max')+1) else False


def CHOICES(para, **valid_check_para):
    """
        检查传入参数，是否是给定枚举内的一种
    """
    return True if para in valid_check_para.get('choices') else False


def MAX_LENGTH(para, **valid_check_para):
    return len(smart_unicode(para)) <= valid_check_para.get('length')


if __name__ == '__main__':
    pass
