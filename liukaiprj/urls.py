"""liukaiprj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('apps.swagger.urls')),
    url(r'^robottest/', include('apps.weixinmp.urls')),
    url(r'', include('apps.common.urls')),
    url(r'', include('apps.data.urls')),
    url(r'', include('apps.upload_resumable.urls')),
    url(r'', include('apps.user.urls')),
    url(r'', include('apps.practice.urls')),
    url(r'', include('apps.wechatmp.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #     {'document_root': os.path.join(settings.BASE_DIR, settings.FILE_STORAGE_DIR_NAME), }),
]


# html page
# urlpatterns += patterns('templates.html',
# url(r'^html/login$', 'html_login'),
# url(r'^html/locallogin$', 'html_locallogin'),
# url(r'^html/logout$', 'html_logout'),

# )

# page's favicon
# urlpatterns += patterns('', (r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),)

urlpatterns += staticfiles_urlpatterns()   # static

# urlpatterns += patterns('',
#     url(r'^media/(?P<path>.*)$',
#         'django.views.static.serve',
#         {'document_root': os.path.join(settings.BASE_DIR, settings.FILE_STORAGE_DIR_NAME), }),
#                         )
