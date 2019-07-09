# -*- coding=utf-8 -*-

from django.conf.urls import url

from apps.swagger.views import api_index, api_docs

urlpatterns = [
    # url(r'^api/common/test$', api_common_test),
    url(r'^api/$', api_index),
    url(r'^api/docs/$', api_docs),
]

# swagger
# urlpatterns += patterns('apps.swagger.views',
#                         url(r'^api/$', 'api_index'),
#                         url(r'^api/docs/$', 'api_docs'),
#                         )
