# -*- coding=utf-8 -*-

import logging

from utils.const_err import FAIL
from utils.utils_except import BusinessException

logger = logging.getLogger(__name__)


def api_common_test(request, testparam1):
    logger.info(testparam1)
    if testparam1.lower() != 'ok':
        raise BusinessException(FAIL)
    result = testparam1
    return result

