 #coding:utf-8
from django.shortcuts import render,  get_object_or_404
from .models import Guest, Msg, Givenid
from django.views.decorators.csrf import csrf_exempt
import json
from random import choice
import string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from email.header import Header
from live.gl import danmucount



#以下是从微信端函数
@csrf_exempt
def login(request):#从微信端登录
    if request.method=='POST':
        req = json.loads(request.body.decode('utf-8'))
        id=req['authid']
        try:
            givenid=Givenid.objects.get(authid=id)#检查authid是否已经分配过
        except Givenid.DoesNotExist:
            return HttpResponse("这个authid还没有分配！")
        try:
            guest=Guest.objects.get(authid=id)#检查authid是否有微信绑定
            return HttpResponse("这个authid分配过，但是已经有人绑定了！")
        except Guest.DoesNotExist:
            guest=Guest(nick_name=req['name'], avatarurl=req['img'], authid=id)#建立新的Guest
            guest.save()
    else:
        return HttpResponse("没有用POST!")

@csrf_exempt
def datapost(request):#从微信端发消息，始终都有头像信息
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        content = req['msg']
        name=req['name']
        img=req['img']
        msg=Msg(content=content, img=img, name=name)
        msg.save()
        return HttpResponse("I got you.")
    else:
        return HttpResponse("没有用POST!")

#以下是网页端函数
def danmusubmit(request):
    if request.method == 'POST':
        content=request.POST
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            guest=Guest.objects.get(authid=0000)
        msg=Msg(content= content,name=guest.nick_name, img=guest.avatarurl)
        msg.save()
    else:
        HttpResponseRedirect(reverse('live:index'))

def commentsubmit(request):
    if request.method == 'POST':
        content=request.POST
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            guest=Guest.objects.get(authid=0000)
        comment=Comment(content=guest.nick_name,name=guest.nick_name, img=guest.avatarurl)
        comment.save()
    else:
        HttpResponseRedirect(reverse('live:index'))



def danmu(request):#JS请求
    global danmucount, commentcount
    list=[]
    danmus=Msg.objects.all()
    danmus.order_by("id")
    comments=Comment.objects.all()
    comments.order_by("id")
    if danmus.count()!=0 and danmucount != danmus.count():
        danmu=danmus[danmucount]
        list.append(danmu.ToDict())
        danmucount+=1

    if commentcount != 0 and commentcount!=comments.count():
        comment=comments[commentcount]
        list.append(comment.ToDict())
        commentcount+=1
    resp=json.dumps(list,ensure_ascii=False)

    response=HttpResponse(resp)
    response['Access-Control-Allow-Origin']='*'
    response["Access-Control-Allow-Headers"] = "*"
    return response





def Genauthid(length=4,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])


def index(request):
    if "authid" not in request.session:#若首次登录，则分配给当前session  authid
       while(1):
            id= Genauthid()
            try:
                guest=Givenid.objects.get(authid=id)#检在Givenid库中查生成的随机id是否已经分配
            except Givenid.DoesNotExist:
                request.session['authid']=id
                g1=Givenid(authid=id)
                g1.save()
                request.session.save()
                break
       guest=Guest.objects.get(authid='0000')
    else:
        try:#若Guest中有，则找到绑定的用户
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:#若出错，则说明当前session尚未绑定，返回AnonymousUser
            guest=Guest.objects.get(authid='0000')


    msgs = Msg.objects.all()
    return render(request, 'live.html', {'msgs':msgs}, {'guest':guest})
