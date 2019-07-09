# coding=utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SYSTEM_CODE = 'liukaiprj'
SYSTEM_NAME = '刘凯项目'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^42(67g79vw(e$*&m6s)q-1=+ecsn2xx3lh@b$u%p79(!sb03e'


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.bizlog',
    'apps.pypinyin',
    'apps.common',
    'apps.data',
    'apps.swagger',
    'apps.upload_resumable',
    'apps.user',
    'apps.weixinmp',
    'apps.practice',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'apps.bizlog.record.LogMiddleware',
)

ROOT_URLCONF = SYSTEM_CODE + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = SYSTEM_CODE + '.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'  # 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )

# 用户模型，根据情况进行修改
AUTH_USER_MODEL = 'user.Account'

# 本地认证结合CAS认证
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django_cas_ng.backends.CASBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SUIT_CONFIG = {
    'ADMIN_NAME': u'刘凯prj',
    'HEADER_DATE_FORMAT': 'Y年 F j日 l',
    'HEADER_TIME_FORMAT': 'H:i',
    'LIST_PER_PAGE': 50,
    'MENU': (
        {'app': 'common', 'label': u'通用',},
        {'app': 'bizlog', 'label': u'日志',},
    )
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'django.log'),
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'django_command': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'command.log'),
            'formatter': 'standard',
        },
        'django.db.backends_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'db.log'),
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
        },
        'applications': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django_command': {
            'handlers': ['django_command', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        # 'django.db.backends': {
        #     'handlers': ['django.db.backends_handler', 'console'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },

    }
}

LOG_CENTER = {
    'log': os.path.join(BASE_DIR + '/log/', 'django.log'),
    'system_code': SYSTEM_CODE,
    'system_name': SYSTEM_NAME,
    'domain': 'http://127.0.0.1:8000',
    'table': 'common_oper_log',
    'rotate_search': 1,
    'include': ('^/api/', '^/test/api/'),
    'exclude': ('^/api/$', '^/api/docs/$', ),
    'long_request': {
        'threshold': 1000 * 2,
        'report_include': ('*', ),
        'report_exclude': ('^/api/common/upload/image', ),
    },
    'head_record_length': -1,
    'request_record_length': -1,
    'response_record_length': -1,
}

# 会话过期时间1天，默认值2周过期（1209600）
SESSION_COOKIE_AGE = 1209600

# 密码加密密钥
PASSWORD_CRYPT_KEY = "58560e24317140589770c1af3bb2905c"
DEFAULT_PASSWORD = "123456"

DATA_STORAGE_USE_S3 = False
FILE_STORAGE_DIR_NAME = 'media'

# 文件类型
FILE_TYPE_PDF = ["pdf", [".pdf"]]
FILE_TYPE_MP4 = ["mp4", [".mp4", ".avi", ".mov", ".wmv", ".mkv", ".ogg", ".mpeg", ".webm", ".3gp", ".mpg"]]
FILE_TYPE_FLV = ["flv", [".flv"]]
FILE_TYPE_SWF = ["swf", [".swf"]]
FILE_TYPE_IMG = ["img", [".jpg", ".jpeg", ".gif", ".png", ".bmp"]]
FILE_TYPE_DOC = ["doc", [".doc", ".docx"]]
FILE_TYPE_PPT = ["ppt", [".ppt", ".pptx"]]
FILE_TYPE_XLS = ["xls", [".xls", ".xlsx"]]
FILE_TYPE_ZIP = ["zip", [".zip", ".rar"]]
FILE_TYPE_UNKNOWN = ["unknown", []]
SUPPORTED_FILE_TYPE = [FILE_TYPE_PDF, FILE_TYPE_MP4, FILE_TYPE_FLV, FILE_TYPE_SWF, FILE_TYPE_IMG, FILE_TYPE_DOC,
                       FILE_TYPE_PPT, FILE_TYPE_XLS, FILE_TYPE_ZIP]
NEED_PROCESS_TO_PREVIEW_FILE_TYPE = [FILE_TYPE_PDF[0], FILE_TYPE_MP4[0], FILE_TYPE_FLV[0], FILE_TYPE_SWF[0],
                                     FILE_TYPE_DOC[0], FILE_TYPE_PPT[0], FILE_TYPE_XLS[0]]
FILE_EXT_ZIP = '.zip'
FILE_EXT_RAR = '.rar'
