# -*- coding=utf-8 -*-

from django.conf.urls import url

from views import *

urlpatterns = [
    # url(r'^api/common/upload/image', api_upload_image),  # 图片上传
    url(r'^api/practice/create/quest$', api_practice_create_quest),  # 生成100以内加减
    url(r'^api/practice/list/quest$', api_practice_list_quest),  # 生成题目列表
    url(r'^api/practice/answer/commit$', api_practice_answer_commit),  # 提交答题结果

    url(r'^page/practice/home$', page_practice_home),  # 生成题目列表
    url(r'^page/practice/list/quest$', page_practice_list_quest),  # 生成题目列表
    url(r'^page/practice/list/answer/his$', page_practice_list_answer_his),  # 查看历史答题记录

    # url(r'^page/practice/list/questtype$', page_practice_list_questtype),  # 生成题目列表
    url(r'^page/practice/pinyin$', page_practice_pinyin),  # 生成拼音练习的页面
    url(r'^api/practice/pinyin$', api_practice_pinyin),  # 生成拼音练习EXCEL
]
