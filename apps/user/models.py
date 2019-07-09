# coding=utf-8
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from apps.upload_resumable.models import FileObj
from utils.public_fun import xor_crypt_string

__author__ = 'liukai'

"""
初始化用户
INSERT INTO "account"("password", "last_login", "username", "encoded_pwd", "name", "sex", "mobile", "email", "image_id", "is_admin", "create_time", "update_time", "del_flag") 
VALUES ('pbkdf2_sha256$20000$LSHwlFu5bemE$P6ed6cSvHT28jXWXNMj4rKXba7rJvsYKjdkdHYcGplA=', CURRENT_TIMESTAMP, 'liukai', '123456', '', '', '', '', NULL, '1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0);
"""

class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username or not password:
            raise ValueError('UserManager create user param error')
        user = self.model(username=username)
        user.encoded_pwd = xor_crypt_string(data=password, encode=True)
        user.set_password(password)
        if kwargs:
            if kwargs.get('mobile', ""):
                user.mobile = kwargs['mobile']
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        account = self.create_user(username, password)
        account.is_superuser = True
        account.is_admin = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser):
    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    username = models.CharField(max_length=40, unique=True, db_index=True, verbose_name=u"账号")
    encoded_pwd = models.CharField(max_length=128, verbose_name=u"加密密码")
    name = models.CharField(default="", max_length=30, db_index=True, blank=True, verbose_name=u'姓名')
    sex = models.CharField(default=u"未设置", max_length=30, choices=((u"未设置", u"未设置"), (u"男", u"男"),
                                                                      (u"女", u"女")), verbose_name=u'性别')
    mobile = models.CharField(default="", blank=True, max_length=30, verbose_name=u'手机号')
    email = models.CharField(default="", blank=True, max_length=30, verbose_name=u'邮箱')
    image = models.ForeignKey(FileObj, related_name=u"image_account", null=True, blank=True, verbose_name=u"用户头像",
                              on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False, verbose_name=u'是否后台管理员')  # 只有root可以登陆后台admin操作数据库
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    del_flag = models.IntegerField(default=0, choices=((1, u"是"), (0, u"否")), verbose_name=u'是否删除')

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        db_table = "account"
        verbose_name = u"个人表"
        verbose_name_plural = u"个人表"

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
