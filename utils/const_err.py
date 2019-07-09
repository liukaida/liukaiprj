# -*- coding=utf-8 -*-

from django.conf import settings


def code(err_code):
    """
        转换为全局唯一错误码
    """
    return int(settings.SYSTEM_CODE) * 10000 + err_code


# -------------------------------- 通用错误码 （一般不要修改）---------------------------------------
FAIL = [-1, u'失败']
SUCCESS = [0, u'完成']
RATE_LIMIT = [10, u'操作太频繁，请稍后再试']
REQUEST_PARAM_ERROR = [1002, u'请求参数错误']

ERR_LOGIN_FAIL = [40003, u'用户名或密码错误']
AUTH_NEED_LOGIN = [40004, u'用户未登录或登录已过期']  # 同用户中心保持一致
AUTH_USER_TYPE_CRUSH = [40000, u'用户角色冲突，请重新登录']
ERR_USER_AUTH = [40005, u'用户权限不够']
ERR_USER_EXISTS = [40006, u'用户已经存在']
ERR_USER_NOT_EXIST = [40012, u'用户不存在']