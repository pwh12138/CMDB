from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    profile = models.OneToOneField(User)
    name_cn = models.CharField(max_length=20,verbose_name='中文名称')
    wechat = models.CharField(max_length=50,verbose_name='微信号')
    phone = models.CharField(max_length=15,verbose_name='电话号码')

    class Meta:
        default_permissions = []
        permissions = (
            ('add_user','添加用户'),
            ('show_user','查看用户'),
            ('update_user','更新用户'),
            ('delete_user','删除用户'),
        )
