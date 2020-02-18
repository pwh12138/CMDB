from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    profile = models.OneToOneField(User)
    name_cn = models.CharField(max_length=20,verbose_name='中文名称')
    wechat = models.CharField(max_length=50,verbose_name='微信号')
    phone = models.CharField(max_length=15,verbose_name='电话号码')
