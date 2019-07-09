# -*- coding: utf-8 -*-

import logging
import types
from functools import wraps

from django.conf import settings

from utils.const_err import *
from utils.const_def import *
from utils.net_helper import response405, response403, response200
from utils.utils_log import log_request

logger = logging.getLogger(__name__)


def validate(method, auth=True, usertype=(None,), condition=None):
    """
        用户请求基本权限验证,usertype后面设计后再补充
    """
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            if request.method != method:
                return response405({'c': REQUEST_WRONG_METHOD[0], 'm': REQUEST_WRONG_METHOD[1]})

            if auth:
                # if request.user.username == settings.DB_ADMIN:
                #     return response403({'c': ROOT_FORBID[0], 'm': ROOT_FORBID[1]})
                if not request.user.is_authenticated():
                    return response200({'c': AUTH_NEED_LOGIN[0], 'm': AUTH_NEED_LOGIN[1]})
                
                # 检查用户是否存在
                if request.user.del_flag == TRUE_INT:
                    return response403({'c': USER_NOT_EXIST[0], 'm': USER_NOT_EXIST[1]})

                # 检查用户类型是否被允许
                request_user_type = None  # 后面设计了再补充
                if request_user_type not in usertype:
                    return response403({'c': AUTH_WRONG_TYPE[0], 'm': AUTH_WRONG_TYPE[1]})
                elif isinstance(condition, types.FunctionType):
                    if not condition(request):
                        return response403({'c': AUTH_CONDITION_FAIL[0], 'm': AUTH_CONDITION_FAIL[1]})
            log_request(request)
            return func(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def is_admin(request):
    """
        判断用户是否是管理员，待补充
    """
    return True


