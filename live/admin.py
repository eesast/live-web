# -*- coding:utf-8 -*-
from django.contrib import admin
from live import models
from django.contrib.sessions.models import Session


class GuestAdmin(admin.ModelAdmin):
    list_display = ('name','authid','img')

class MsgAdmin(admin.ModelAdmin):
    list_display = ('name','content','send_time','id')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key',)

class GivenAdmin(admin.ModelAdmin):
    list_display = ('authid',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','content','img','id')

admin.site.register(models.Guest,GuestAdmin)
admin.site.register(models.Msg,MsgAdmin)
admin.site.register(Session,SessionAdmin)
admin.site.register(models.Comment,CommentAdmin)
# Register your models here.
