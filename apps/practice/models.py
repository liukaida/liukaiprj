# -*- coding=utf-8 -*-
from django.conf import settings
from django.db import models


class Question(models.Model):
    # 0：100以内加
    # 1：100以内减
    quest_type = models.PositiveSmallIntegerField(u'题目类型', blank=False, null=False)
    answer_type = models.PositiveSmallIntegerField(u'答案种类', choices=((1, u"单选"), (2, u"多选"), (3, u"填空")), blank=False, null=False)
    quest_title = models.TextField(u'题目', blank=True, null=True)
    title_appendattr = models.CharField(u'题目附加属性', blank=True, null=True, max_length=30)  # 预留
    quest_detail = models.TextField(u'题目详情JSON', blank=True, null=True)  # 题目选项
    answer_detail = models.TextField(u'答案详情JSON', blank=True, null=True)  # 答案
    weight = models.IntegerField(u'权重', default=1, blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'question_define'
        verbose_name_plural = u'题目定义表'
        verbose_name = u'题目定义表'
        # ordering = ['-create_time']

    def __unicode__(self):
        return 'q(%s: %s)' % (self.id, self.quest_title)


class UserAnswer(models.Model):
    user_name = models.CharField(u'用户名称', blank=True, null=True, max_length=30)
    question_uuid = models.CharField(u'当次题目唯一标识', blank=True, null=True, max_length=30)
    question_count_total = models.IntegerField(u'题目总数', default=0, blank=True, null=True)
    question_count_err = models.IntegerField(u'错题总数', default=0, blank=True, null=True)
    useranswer_detail = models.TextField(u'用户答案详情JSON', blank=True, null=True)
    duration = models.CharField(u'时长', blank=True, null=True, max_length=30)
    quest_type = models.CharField(u'题目类型', blank=False, null=False, max_length=50)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    class Meta:
        db_table = 'question_user_answer'
        verbose_name_plural = u'用户答案'
        verbose_name = u'用户答案'
        # ordering = ['-create_time']

    def __unicode__(self):
        return 'q(%s: %s)' % (self.id, self.user_name)
