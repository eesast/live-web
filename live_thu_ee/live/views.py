 #coding:utf-8
from django.shortcuts import render,  get_object_or_404
from .models import Guest, Msg, Comment
import json,time
from datetime import datetime
from datetime import timedelta
from random import choice
import urllib.request as req
import hashlib
import string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .gl import danmucount, commentcount

def imgtest(reqeust):
    return render(reqeust, 'imgtest.html')

#以下是从微信端函数
@csrf_exempt
def login(request):#从微信端登录
    print('loginhere')
    if request.method=='POST':
        req = json.loads(request.body.decode('utf-8'))
        id=req['msg']
        if len(id)!=4:
            return HttpResponse('wrong')
        try:
            guest=Guest.objects.get(authid=id)#检查authid是否有微信绑定
            guest.islogin=1
            guest.name=req['name']
            guest.img=req['img']
            guest.save()
            return HttpResponse('0')
        except Guest.DoesNotExist:
            return HttpResponse('no such authid')
    else:
        return HttpResponse("没有用POST!")

def encodeHTML(str):
    return str.replace("&", "&amp;") \
    .replace("<", "&lt;") \
    .replace(">", "&gt;") \
    .replace("\"", "&quot;") \
    .replace("'", "&#39;");


@csrf_exempt
def datapost(request):#从微信端发消息，始终都有头像信息
    print('dataposthere')
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        content = req['msg']
        name=req['name']
        img=req['img']
        msg=Msg(content=encodeHTML(content), img=img, name=name)
        msg.save()
        string='I got %s'%(content)
        return HttpResponse(string)
    else:
        return HttpResponse("没有用POST!")

@csrf_exempt
def wechatpost(request):#直接从趣现场获得弹幕
    if request.method=='POST':
        content=request.POST['content']
        name=request.POST['user_name']
        img=request.POST['user_info[contact_info][wx_headimg_url]']
        msg=Msg(content=content, img=img, name=name)
        msg.save()
    return HttpResponse('0')


#以下是网页端函数
@csrf_exempt
def danmusubmit(request):
    if request.method == 'POST':
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            return HttpResponse('server error')
        if guest.forbid==1:
            return HttpResponseRedirect('https://live.thu.ee')
        msg=Msg(content= encodeHTML(request.POST['msg']),name=guest.name, img=guest.img)
        msg.save()
        return HttpResponse('0')
    else:
        return HttpResponseRedirect('https://live.thu.ee')

@csrf_exempt
def commentsubmit(request):
    if request.method == 'POST':
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            return HttpResponse('server error')
        if guest.forbid==1:
            return HttpResponseRedirect('https://live.thu.ee')
        comment=Comment(content=encodeHTML(request.POST['msg']),name=guest.name, img=guest.img)
        comment.save()
    else:
        return HttpResponseRedirect('https://live.thu.ee')



def poll(request):
#danmu & comment
    danmu_list=[]
    comment_list=[]
    dict={}
    danmus=Msg.objects.all().order_by("id")
    dnum=danmus.count()
    if dnum>0:
        did=danmus.last().id
    else:
        did=0
    comments=Comment.objects.all().order_by("id")
    cnum=comments.count()
    if cnum>0:
        cid=comments.last().id
    else:
        cid=0
    if 'danmucount' in request.session and 'commentcount' in request.session:
        danmucount=request.session['danmucount']
        commentcount=request.session['commentcount']
        danmus=danmus.filter(id__gt=danmucount)
        comments=comments.filter(id__gt=commentcount)
        for danmu in danmus:
            dict2={}
            dict2['danmu_name']=danmu.name
            dict2['danmu_img']=danmu.img
            dict2['danmu_content']=danmu.content
            if datetime.now().year==danmu.send_time.year:
                dict2['danmu_time']=(danmu.send_time+timedelta(hours=8)).strftime("%m-%d %H:%M")
            else:
                dict2['danmu_time']=(danmu.send_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
            danmu_list.append(dict2)
        for comment in comments:
            dict2={}
            dict2['comment_name']=comment.name
            dict2['comment_img']=comment.img
            dict2['comment_content']=comment.content
            if datetime.now().year==danmu.send_time.year:
                dict2['comment_time']=(danmu.send_time+timedelta(hours=8)).strftime("%m-%d %H:%M")
            else:
                dict2['comment_time']=(danmu.send_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
            comment_list.append(dict2)
    dict['danmu']=danmu_list
    dict['comment']=comment_list
    request.session['danmucount']=did
    request.session['commentcount']=cid
    request.session.save()
#program index & status 0 normal, 1 video source error, 2 no source 
    try:
        f=open('/tmp/live_status.txt','r')
        temp=json.loads(f.read())
        dict['pnum']=temp.pnum
        dict['status']=temp.status
        f.close()
    except FileNotFoundError:
        dict['pnum']=-1
        dict['status']=0

#login_status
    if 'authid' in request.session:
        guest=Guest.objects.get(authid=request.session['authid'])
        dict['islogin']=guest.islogin
    else:
        dict['islogin']=0
    dict['danmucount']=danmus.count()
    dict['commentcount']=comments.count()
    g=Guest.objects.all()

    dict['totalamount']=g.count()
    try:
        guest=Guest.objects.get(authid=request.session['authid'])
    except Guest.DoesNotExist:
        return HttpResponse('Server Error')
    dict['forbid']=guest.forbid
    resp=json.dumps(dict,ensure_ascii=False)
    response=HttpResponse(resp)
    response['Access-Control-Allow-Origin']='*'
    response["Access-Control-Allow-Headers"] = "*"
    return response

def Genauthid(length=4,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])


def locating(ip):
    url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip
    data = req.urlopen(url).read().decode('utf-8')
    dict = json.loads(data)
    return dict

def logout(request):
    if "authid" in request.session:
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            return HttpResponse('not logged in yet.')
        del request.session['authid']
        guest.islogin=0
        return HttpResponseRedirect('https://live.thu.ee')
    else:
        return HttpResponse('not logged in yet.')

def index(request):
    if "authid" not in request.session:#若首次登录，则分配给当前session  authid
       while(1):
            id= Genauthid()
            guest=Guest.objects.filter(authid=id)
            if len(guest)==0:
                request.session['authid']=id
                request.session.save() 
                guest=Guest(authid=id,ip=request.META['REMOTE_ADDR'])
                addr=locating(request.META['REMOTE_ADDR'])
                if len(addr["province"].replace(" ",""))>0:
                    guest.addr=addr["province"]
                else:
                    guest.addr=addr["country"]
                guest.name=guest.addr+"网友 (" + str(int(hashlib.sha1(request.session.session_key.encode('utf-8')).hexdigest(), 16) % (10 ** 7)) + ")"
                guest.save()
                break
    else:
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            while(1):
                id= Genauthid()
                try:
                    guest=Guest.objects.get(authid=id)
                except Guest.DoesNotExist:
                    request.session['authid']=id
                    request.session.save()
                    guest=Guest(authid=id,ip=request.META['REMOTE_ADDR'])
                    addr=locating(request.META['REMOTE_ADDR'])
                    if len(addr["province"].replace(" ",""))>0:
                        guest.addr=addr["province"]
                    else:
                        guest.addr=addr["country"]
                    guest.save()
                    break
    if 'commentcount' not in request.session or 'danmucount' not in request.session:
        danmus=Msg.objects.all().order_by("id")
        comments=Comment.objects.all().order_by("id")
        if danmus.count()>0:
            request.session['danmucount']=danmus.last().id
        else:
            request.session['danmucount']=0
        if comments.count()>0:
            request.session['commentcount']=comments.last().id
        else:
            request.session['commentcount']=0
        request.session.save()

    return render(request, 'test.html', {'guest':guest})
