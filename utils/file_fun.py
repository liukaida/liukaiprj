# -*- coding: utf-8 -*-
import hashlib
import os
import datetime
import uuid
import logging

# from object_storage import ObjectStorage
from django.conf import settings

from apps.upload_resumable.storage.object_storage import ObjectStorage
from const_def import *

logger = logging.getLogger(__name__)

OBJECT_STORAGE_OBJ = None


def get_object_storage_obj():
    global OBJECT_STORAGE_OBJ
    if OBJECT_STORAGE_OBJ is None:
        OBJECT_STORAGE_OBJ = ObjectStorage()
    return OBJECT_STORAGE_OBJ


def remove_obj_storage_file(obj_path):
    get_object_storage_obj().delete(obj_path)


def clean_overdue_files(dir_path=settings.TEMP_DIR):
    try:
        now = datetime.datetime.now()
        due_date = now - datetime.timedelta(hours=settings.TMP_FILE_EXPIRED_HOURS)
        files_in_dir = os.listdir(dir_path)
        for file_path in files_in_dir:
            abs_file_path = os.path.join(dir_path, file_path)
            if os.path.isfile(abs_file_path):
                mtimestamp = os.path.getmtime(abs_file_path)
                mtime = datetime.datetime.fromtimestamp(mtimestamp)
                if mtime < due_date:
                    os.remove(abs_file_path)
    except Exception as ex:
        logging.exception("Clean files in %s with exception:%s" % (dir_path, ex))


def gen_path(prefix='', suffix='.xlsx', dir_path=settings.TEMP_DIR):
    # clean_overdue_files()
    random_num = uuid.uuid4().hex
    file_name = "%s%s%s" % (prefix, random_num, suffix)
    if len(dir_path) > 0:
        file_path = os.path.join(dir_path, file_name)
        return file_path
    else:
        return file_name


def gen_s3_file_path(suffix, abs=True):
    if abs:
        return gen_path(suffix=suffix, dir_path=settings.AWS_STORAGE_BUCKET_NAME)
    else:
        return gen_path(suffix=suffix, dir_path='')


def get_image_url(path, abs=False):
    if not path:
        url = ""
        return url
    if settings.DATA_STORAGE_USE_S3:
        path = "/" + settings.AWS_STORAGE_BUCKET_NAME + "/" + path
        url = 'http://' + settings.AWS_S3_HOST + ":" + str(settings.AWS_S3_PORT) + path
    else:
        path = "/" + settings.FILE_STORAGE_DIR_NAME + "/" + path
        url = path
    return url


def get_file_type(file_name, type_list=settings.SUPPORTED_FILE_TYPE):
    ext = ""
    if len(file_name) < 2:
        return None, ext
    ext = os.path.splitext(file_name)[-1].lower()
    for file_type in settings.SUPPORTED_FILE_TYPE:
        if ext in file_type[1]:
            return file_type[0], ext
    return None, ext


def get_new_file_name_with_suffix(file_name, suffix, ext=""):
    src_ext = os.path.splitext(file_name)[-1]
    if not ext:
        ext = src_ext
    dst_file_name = file_name[:-len(src_ext)] + suffix + ext
    return dst_file_name


def get_file_md5(filepath):
    if not os.path.isfile(filepath):
        return
    f = file(filepath, 'rb')
    md5 = get_fileobj_md5(f)
    f.close()
    return md5


def get_fileobj_md5(fileobj):
    myhash = hashlib.md5()
    while True:
        b = fileobj.read(8096)
        if not b:
            break
        myhash.update(b)
    return myhash.hexdigest()
