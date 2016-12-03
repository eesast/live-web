# -*- coding:utf-8 -*-
"""live_thu_ee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from live import views
from django.conf.urls.static import static
from . import settings

app_name="live"
urlpatterns = [
#    url(r'^imgtest/',views.imgtest),
    url(r'^admin/', admin.site.urls),
    url(r'^msg$', views.datapost),
    url(r'^$', views.index, name='index'),
    url(r'^poll$', views.poll, name='poll'),#获取新的弹幕、评论，各一次一条，JS端用
    url(r'^login$', views.login, name='login'),#登录url 杨怿飞用
	url(r'^logout$', views.logout, name='logout'),
    url(r'^datapost$', views.datapost, name='datapost'),#微信端弹幕，杨怿飞用
    url(r'^danmusubmit$', views.danmusubmit, name='danmusubmit'),#用户弹幕的表单交到这里
    url(r'^commentsubmit$', views.commentsubmit, name='commentsubmit'),#用户评论的表单交到这里
    url(r'^wechatpost$', views.wechatpost, name='wechatpost'),#用更改的趣现场插件获取弹幕
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
