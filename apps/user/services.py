# -*- coding=utf-8 -*-

import logging
import re

from django.conf import settings
from django.contrib import auth
from django.db import transaction

from apps.user.models import Account
from utils.const_def import FLAG_NO
from utils.const_err import FAIL, ERR_USER_AUTH, SUCCESS, ERR_USER_EXISTS
from utils.utils_except import BusinessException

logger = logging.getLogger(__name__)


def login(request, username="", password=""):
    username = username.strip()
    password = password.strip()
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return True
    return False


@transaction.atomic
def add_account(user, username, name, sex, activity_mask, area_id, password=settings.DEFAULT_PASSWORD):
    if not user.is_admin:
        return dict(c=ERR_USER_AUTH[0], m=ERR_USER_AUTH[1])
    account = Account.objects.filter(del_flag=FLAG_NO, username=username).first()
    if not account:
        account = Account.objects.create_user(username, password=password)
        account.name = name if name else ""
        if sex:  account.sex = sex
        if re.match('[gl]', username, re.I):
            account.code = username
        elif len(username) == 11 and username.isdigit():
            account.mobile = username
        if activity_mask:
            activity_mask = int(activity_mask)
            account.activity_mask = activity_mask
        account.save()
        return dict(c=SUCCESS[0], m=SUCCESS[1], d=[account.id])
    else:
        return dict(c=ERR_USER_EXISTS[0], m=ERR_USER_EXISTS[1])


def api_confirmcode_login(request, confirm_code):
    # 用户登陆，此处为模拟登陆的样例，还需要另外开发。
    if confirm_code == '21321239827981293821':
        account_id = 1
        account = Account.objects.filter(id=account_id)
        account.backend = settings.AUTHENTICATION_BACKENDS[0]
        auth.login(request, request.user)

    return True
