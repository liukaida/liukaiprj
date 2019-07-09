# -*- coding=utf-8 -*-

from django.conf.urls import url

from views import *

urlpatterns = [
    # url(r'^api/common/upload/image', api_upload_image),  # 图片上传
    url(r'^api/common/test$', api_common_test),  # 测试方法
    url(r'^page/common/test$', page_common_test),  # 测试方法
    url(r'^wechat', wechat, name='wechat')
]
