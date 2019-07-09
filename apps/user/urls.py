# -*- coding=utf-8 -*-

from django.conf.urls import url

from views import *

urlpatterns = [
    # url(r'^api/common/upload/image', api_upload_image),  # 图片上传
    url("^api/login", api_login),  # 不用改
    url("^api/logout", api_logout),  # 不用改
    url("^api/add/account$", api_add_account),  # 不用改

]
