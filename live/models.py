#coding:utf-8
from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Guest(models.Model):
    name = models.CharField(max_length=50, default='Anonymous')
    img = models.CharField(max_length=200, default='', blank=True, null=True)
    authid = models.CharField(max_length=4, null=False)
    ip = models.CharField(max_length=15,null=True)
    addr = models.CharField(max_length=100, default='火星')
    forbid = models.IntegerField(default=0)
    islogin = models.IntegerField(default=0)
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Msg(models.Model):
    name = models.CharField(max_length=20, default='Anonymous')
    img=models.CharField(max_length=300, null=True, blank=True)
    content = models.CharField(max_length=300)
    send_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=20, default='Anonymous')
    img=models.CharField(max_length=300, null=True, blank=True)
    content = models.CharField(max_length=300)
    send_time = models.DateTimeField(auto_now=True)
    dianzan = models.IntegerField(default=0)
    biandi = models.IntegerField(default=0)
    def __str__(self):
        return self.name+"发表了"+self.content




# Create your models here.