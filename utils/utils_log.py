# -*- coding: utf-8 -*-

import json
import logging
from utils.const_err import *

logger = logging.getLogger(__name__)


def log_request(request):
    if settings.DEBUG:
        if hasattr(request, 'user'):
            user_account = getattr(request.user, 'username', '-')
        else:
            user_account = 'anonymous'
        logger.debug('%s %s' % (user_account, request.get_full_path()))


def log_response(request, data):
    if settings.DEBUG:
        logger.debug('request: %s, response json: %s' % (request.get_full_path(), data))

