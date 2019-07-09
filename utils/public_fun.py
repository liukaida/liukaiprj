#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import urllib2
import urllib
import base64
import hmac
import hashlib
import datetime
import logging

import collections

import math
import requests
import os
from django.conf import settings
from const_err import *

logger = logging.getLogger(__name__)


def gen_signature(key):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    h = hmac.new(key=key, msg=timestamp, digestmod=hashlib.sha256)
    signature = base64.encodestring(h.digest()).strip()
    return timestamp, signature


# 请求第三方网站数据
def send_http_request(url, method="POST", form_data_dict=None):
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)

    # build a request
    data = urllib.urlencode(form_data_dict) if form_data_dict else None
    request = urllib2.Request(url, data=data)

    # add any other information you want
    request.add_header("Content-Type", 'application/x-www-form-urlencoded')
    # overload the get method function with a small anonymous function...
    request.get_method = lambda: method

    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        # connection = e
        raise Exception(u"无法连接到网站")

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
        return data
    else:
        # handle the error case. connection.read() will still contain data
        # if any was returned, but it probably won't be of any use
        raise Exception(u"请求网站返回值不是200")


# 下载文件
def download_file(url, local_dir=settings.TEMP_DIR):
    local_filename = url.split('/')[-1]
    local_path = os.path.join(local_dir, local_filename)
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    if r.status_code != 200:
            # or r.headers.get('Content-Type') != 'binary/octet-stream':
        logger.error("download file error: %s" % url)
        return ""
    with open(local_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    if os.path.exists(local_path):
        return local_path
    else:
        logger.error("download file error: %s" % url)
        return ""


def string_is_null(s):
    if s is None or len(s.strip())==0:
        return True
    else:
        return False


def xor_crypt_string(data, key=settings.PASSWORD_CRYPT_KEY, encode=False, decode=False):
    from itertools import izip, cycle
    import base64
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored

# 输入参数
# rows: 每页最大行数
# page: 请求第几页从1开始计数
# sidx: 排序的列名
# sord: 升序或降序（asc:升序）

# 输出参数
# total: 总页数
# page: 当前第几页
# records: 总记录数（行数）
# items: 请求数据元素列表


def paging(item_list, rows, page, sidx="", sord="asc"):
    # 计算记录数量和页数
    ret_items = []
    records = len(item_list)
    total = records/rows
    if records % rows > 0:
        total += 1
    if page > total:
        page = total

    # 排序
    if sidx:
        reverse = False
        if sord != "asc":
            reverse = True
        if item_list and sidx in item_list[0].keys():
            item_list.sort(key=lambda x: x[sidx], reverse=reverse)

    # compute start and end index
    start = (page-1)*rows
    end = start + rows
    if records > 0 and (start < 0 or end < start):
        logger.error("error start=%d, end=%d" % (start, end))
    else:
        ret_items = item_list[start:end]

    ret_val = dict(
        total=str(total),
        page=str(page),
        records=str(records),
        items=ret_items,
    )
    return ret_val


def paging_with_request(request, dictResp, work_id=None):
    rows = request.POST.get("rows", "")
    page = request.POST.get("page", "")
    sidx = request.POST.get("sidx", "")
    sord = request.POST.get("sord", "")
    if not rows or not page or dictResp["c"] != SUCCESS[0]:
        return dictResp
    item_list = dictResp["d"]
    if work_id:
        rows = len(item_list)
    dictResp["d"] = paging(item_list, int(rows), int(page), sidx, sord)
    return dictResp


def get_pre_and_next(id, dictResp, id_name="id"):
    if not id or dictResp["c"] != SUCCESS[0]:
        return dictResp
    id = int(id)

    rep_data = dictResp["d"]
    if isinstance(rep_data, list):
        item_list = rep_data
    else:
        item_list = rep_data.get("items")

    ret_items = []
    current_idx = -1
    for i in xrange(len(item_list)):
        if item_list[i][id_name] == id:
            current_idx = i
            break
    if current_idx == 0 and current_idx < len(item_list):
        ret_items = item_list[:current_idx+2]
    elif current_idx > 0 and current_idx == len(item_list)-1:
        ret_items = item_list[current_idx-1:]
    elif current_idx > 0 and current_idx < len(item_list):
        ret_items = item_list[current_idx-1:current_idx+2]

    dictResp["d"] = ret_items
    return dictResp


def convert_list_to_dict(src_list, key_name):
    ret_dict = {}
    for item in src_list:
        key = item.pop(key_name)
        if key not in ret_dict.keys():
            ret_dict[key] = []
        ret_dict[key].append(item)
    return ret_dict


# datetime 格式转换
def str_p_datetime(datetime_str, str_format='%Y-%m-%d %H:%M:%S'):
    if not datetime_str:
        return None
    try:
        date_time = datetime.datetime.strptime(datetime_str, str_format)
        return date_time
    except Exception as ex:
        logger.exception(ex.message)
        raise Exception(u"日期时间格式[%s]转换失败" % unicode(str_format, encoding='utf-8'))


def datetime_f_str(date_time, str_format='%Y-%m-%d %H:%M:%S'):
    if isinstance(date_time, datetime.datetime):
        datetime_str = date_time.strftime(str_format)
        return datetime_str
    else:
        raise Exception(u"datetime_to_str fail")


def datetime_f_str_noexcept(date_time, str_format='%Y-%m-%d %H:%M:%S'):
    if isinstance(date_time, datetime.datetime):
        datetime_str = date_time.strftime(str_format)
        return datetime_str
    else:
        return ''


def get_pages(cnt, page, size):
    """
         分页，这种方式比Paginator更高效一些
        :param:总行数， 当前页码  ，每页行数
        :return: 总页数，本次开始行数，本次结束行数
    """
    page = int(page)
    size = int(size)
    num_pages = math.ceil(float(cnt) / size)  # 总页数
    # if page > num_pages:
    #     raise BusinessException(WRONG_PAGE)
    cur_start = (page - 1) * size
    cur_end = page * size
    return num_pages, cur_start, cur_end


def paging_by_lastid(raw_list, rows):
    rows = int(rows)
    total = len(raw_list)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    paged_list = raw_list[:rows]

    result = collections.OrderedDict()
    result['max_page'] = int(max_page)
    result['total'] = int(total)
    result['page'] = 0
    result['data_list'] = list()
    return paged_list, result


def paging_by_page(raw_list, rows, page):
    page = int(page)
    rows = int(rows)
    total = len(raw_list)
    max_page = total / rows
    if total % rows != 0:
        max_page += 1

    if total >= (page - 1) * rows:
        start = (page - 1) * rows
        end = start + rows
        paged_list = raw_list[start:end]
    else:
        paged_list = []

    result = collections.OrderedDict()
    result['total'] = int(max_page)
    result['records'] = int(total)
    result['page'] = int(page)
    result['items'] = list()
    return paged_list, result


def get_lastid_index(file_list, last_id):
    index = 0
    last_id = int(last_id)
    for each_file in file_list:
        index += 1
        if each_file['id'] == last_id:
            return index

    return 0


def gen_rnd_filename(file_name):
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s_%s_%s' % (file_name, filename_prefix, str(random.randrange(1000, 10000)))


def load_clazz(path, **kwargs):
    import importlib
    sp = path.rfind('.')
    module_name = path[:sp]
    clazz_name = path[sp+1:]
    module = importlib.import_module(module_name)
    clazz = getattr(module, clazz_name)
    return clazz(kwargs)


def get_timestr(dt, dt_format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(dt_format)


slash_replace_str = ("/", "%2F")  # 替换url中的/
question_replace_str = ("?", "%3F")  # 替换url中的?
equal_replace_str = ("=", "%3D")  # 替换url中的=
and_replace_str = ("&", "%26")  # 替换url中的&
url_replace_list = (slash_replace_str, question_replace_str, equal_replace_str, and_replace_str)


def convert_from_url_path(s):
    # print s
    for url_replace in url_replace_list:
        s = s.replace(url_replace[0], url_replace[1])
    # print s
    # if s.isalnum():
    #     return s
    # else:
    #     return None
    return s


def convert_to_url_path(s):
    for url_replace in url_replace_list:
        s = s.replace(url_replace[1], url_replace[0])
    return s
