# -*- coding=utf-8 -*-

import logging
import json
import uuid

import datetime

from apps.practice.models import Question, UserAnswer
from utils.const_def import FALSE_INT, TRUE_INT
from utils.const_err import FAIL
from utils.public_fun import datetime_f_str
from utils.utils_except import BusinessException
from const import *

logger = logging.getLogger(__name__)


def api_common_test(request, testparam1):
    logger.info(testparam1)
    if testparam1.lower() != 'ok':
        raise BusinessException(FAIL)
    result = testparam1
    return result


def api_practice_create_quest(request, quest_type):
    if not quest_type:
        raise BusinessException(ERR_QUEST_TYPE)

    # 检查是否已经生成题目
    old_quest = Question.objects.filter(quest_type=quest_type, del_flag=FALSE_INT)
    if old_quest:
        raise BusinessException(ERR_QUEST_HASQUEST)

    if int(quest_type) == QUEST_TYPE_ADD100[0]:
        # 100以内加
        answer_type = ANSWER_TYPE_FILLSPACE[0]

        for x in range(0, 100):
            for y in range(0, 100):
                z = x + y
                if z <= 100:
                    answer_detail = list()
                    answer_detail.append(z)
                    answer_detail_jsonstr = json.dumps(answer_detail)

                    quest = Question()
                    quest.quest_type = quest_type
                    quest.answer_type = answer_type
                    quest.quest_title = '%s + %s' % (x, y)
                    quest.title_appendattr = ''
                    quest.quest_detail = ''
                    quest.answer_detail = answer_detail_jsonstr
                    quest.weight = 1
                    quest.save()
    elif int(quest_type) == QUEST_TYPE_SUB100[0]:
        # 100以内减
        answer_type = ANSWER_TYPE_FILLSPACE[0]

        for x in range(0, 100):
            for y in range(0, 100):
                z = x - y
                if z >= 0:
                    answer_detail = list()
                    answer_detail.append(z)
                    answer_detail_jsonstr = json.dumps(answer_detail)

                    quest = Question()
                    quest.quest_type = quest_type
                    quest.answer_type = answer_type
                    quest.quest_title = '%s - %s' % (x, y)
                    quest.title_appendattr = ''
                    quest.quest_detail = ''
                    quest.answer_detail = answer_detail_jsonstr
                    quest.weight = 1
                    quest.save()
    elif int(quest_type) == QUEST_TYPE_MUL10[0]:
        # 10以内乘
        answer_type = ANSWER_TYPE_FILLSPACE[0]

        for x in range(1, 10):
            for y in range(1, 10):
                z = x * y
                if z >= 0:
                    answer_detail = list()
                    answer_detail.append(z)
                    answer_detail_jsonstr = json.dumps(answer_detail)

                    quest = Question()
                    quest.quest_type = quest_type
                    quest.answer_type = answer_type
                    quest.quest_title = '%s X %s' % (x, y)
                    quest.title_appendattr = ''
                    quest.quest_detail = ''
                    quest.answer_detail = answer_detail_jsonstr
                    quest.weight = 1
                    quest.save()
    elif int(quest_type) == QUEST_TYPE_ADD10[0]:
        # 10以内加
        answer_type = ANSWER_TYPE_FILLSPACE[0]

        for x in range(1, 10):
            for y in range(1, 10):
                z = x + y
                if z >= 0:
                    answer_detail = list()
                    answer_detail.append(z)
                    answer_detail_jsonstr = json.dumps(answer_detail)

                    quest = Question()
                    quest.quest_type = quest_type
                    quest.answer_type = answer_type
                    quest.quest_title = '%s + %s' % (x, y)
                    quest.title_appendattr = ''
                    quest.quest_detail = ''
                    quest.answer_detail = answer_detail_jsonstr
                    quest.weight = 1
                    quest.save()
    elif int(quest_type) == QUEST_TYPE_SUB10[0]:
        # 10以内减
        answer_type = ANSWER_TYPE_FILLSPACE[0]

        for x in range(1, 10):
            for y in range(1, 10):
                z = x - y
                if z >= 0:
                    answer_detail = list()
                    answer_detail.append(z)
                    answer_detail_jsonstr = json.dumps(answer_detail)

                    quest = Question()
                    quest.quest_type = quest_type
                    quest.answer_type = answer_type
                    quest.quest_title = '%s - %s' % (x, y)
                    quest.title_appendattr = ''
                    quest.quest_detail = ''
                    quest.answer_detail = answer_detail_jsonstr
                    quest.weight = 1
                    quest.save()
    else:
        raise BusinessException(ERR_QUEST_TYPE)
    return 'ok'


def api_practice_list_quest(request, quest_type, num):
    result = dict()
    quest_list = list()
    # 获取列表
    if not quest_type:
        raise BusinessException(ERR_QUEST_TYPE)

    quest_type = quest_type.strip(',').split(',')

    # 检查是否已经生成题目
    old_quest = Question.objects.filter(quest_type__in=quest_type, del_flag=FALSE_INT)
    if not old_quest:
        raise BusinessException(ERR_QUEST_HASQUEST)

    quests = Question.objects.filter(quest_type__in=quest_type, del_flag=FALSE_INT).order_by('?')[:num]
    sn = 0
    for each_quest in quests:
        quest_dict = {
            'sn': sn,
            'quest_title': each_quest.quest_title,
            'answer_type': each_quest.answer_type,
            'title_appendattr': each_quest.title_appendattr,
            'quest_detail': each_quest.quest_detail,
            'answer_detail': each_quest.answer_detail,
            'answer_detail_json': json.loads(each_quest.answer_detail) if each_quest.answer_detail else '',
            'weight': each_quest.weight,
        }
        quest_list.append(quest_dict)
        sn += 1

    result['quest_type'] = quest_type
    result['quest_type_name'] = get_quest_name_by_type(quest_type)
    result['quest_list'] = quest_list
    result['quest_num'] = len(quest_list)
    return result


def get_quest_name_by_type(quest_type):
    name_list = []
    # quest_type = int(quest_type)
    for each_type in QUEST_TYPE_LIST:
        if str(each_type[0]) in quest_type:
            name_list.append(each_type[1])
    return u'、'.join(name_list)


def get_quest_list_page_param(request, quest_type, num):
    # result = list()
    # params = {
    #     'id': 1,
    #     'name': 2,
    #     'testlist': [5, 6, 7],
    # }
    if not quest_type:
        raise BusinessException(ERR_QUEST_TYPE)

    quest_list = api_practice_list_quest(request, quest_type, num)
    params = {
        'quest_type_name': quest_list['quest_type_name'],
        'quest_maxnum': quest_list['quest_num'],
        'rand_uniq_id': get_rand_id(uniq=True),
        'quest_type': quest_type,
        'quest_list': quest_list['quest_list'],
    }

    return params


def get_rand_id(uniq=True):
    random_num = uuid.uuid4().hex
    if not uniq:
        return random_num

    # 防止重复
    while True:
        rep_useranswer = UserAnswer.objects.filter(question_uuid=random_num, del_flag=FALSE_INT)
        if not rep_useranswer:
            break
        random_num = uuid.uuid4().hex
    return random_num


def api_practice_answer_commit(user, user_name, question_uuid, question_count_total, question_count_err, useranswer_detail, duration, quest_type):
    # 检查有没有相同的题目答案，如果有则是重复提交，不用再提交了。直接return
    old_answer = UserAnswer.objects.filter(question_uuid=question_uuid, del_flag=FALSE_INT,
                                           user_name=user_name, question_count_total=question_count_total,
                                           question_count_err=question_count_err, useranswer_detail=useranswer_detail,
                                           quest_type=quest_type)
    if old_answer:
        return 'ok'

    # 先将旧的uuid失效
    UserAnswer.objects.filter(question_uuid=question_uuid, del_flag=FALSE_INT).update(del_flag=TRUE_INT)

    useranswer = UserAnswer()
    useranswer.user_name = user_name
    useranswer.question_uuid = question_uuid
    useranswer.question_count_total = question_count_total
    useranswer.question_count_err = question_count_err
    useranswer.useranswer_detail = useranswer_detail
    useranswer.duration = duration
    useranswer.quest_type = quest_type
    useranswer.save()
    return 'ok'


def get_practice_list_answer_his(request, user_name, days):
    param = dict()
    days = int(days)
    now = datetime.datetime.now()
    starttime = now - datetime.timedelta(days=days)
    quizs = UserAnswer.objects.filter(del_flag=FALSE_INT, create_time__gte=starttime)
    if user_name:
        quizs = quizs.filter(user_name=user_name)
    quizs = quizs.order_by('-create_time')

    quiz_list = list()
    for each_quiz in quizs:
        quiz_dict = dict()
        quiz_dict['create_time'] = datetime_f_str(each_quiz.create_time)
        quiz_dict['user_name'] = each_quiz.user_name
        quiz_dict['question_uuid'] = each_quiz.question_uuid
        quiz_dict['question_count_total'] = each_quiz.question_count_total
        quiz_dict['question_count_err'] = each_quiz.question_count_err
        quiz_dict['duration'] = each_quiz.duration
        quiz_dict['quest_type'] = get_quest_type_name(each_quiz.quest_type)
        quiz_dict['err_answer_detail'] = get_useranswer_detail_str(each_quiz.useranswer_detail)
        quiz_list.append(quiz_dict)
    param['quiz_list'] = quiz_list
    return param


def get_quest_type_name(quest_type):
    """
    将逗号分隔questid转换为逗号分隔的名称
    :param quest_type:
    :return:
    """
    quest_type_list = quest_type.split(',')
    print quest_type_list

    quest_type_name_list = list()
    for each_quest_type in QUEST_TYPE_LIST:
        if str(each_quest_type[0]) in quest_type_list:
            quest_type_name_list.append(each_quest_type[1])
    print quest_type_name_list
    return ','.join(quest_type_name_list)


def get_useranswer_detail_str(useranswer_detail):
    """
    将useranswer_detail转换为可显示的字符串，供前端阅读
    :param useranswer_detail:
    :return:
    """
    result = ""
    useranswer_detail = json.loads(useranswer_detail)
    for each_answer in useranswer_detail:
        result = result + u"序号：%s 题：%s 答：%s 正：%s <br \>" % (each_answer['sn'], each_answer['question'],
                                                            each_answer['myanswer'], each_answer['answer'])
    return result
