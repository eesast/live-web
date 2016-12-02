 #coding:utf-8
from django.shortcuts import render,  get_object_or_404
from .models import Guest, Msg, Comment
import json, time
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
        print(id)
        try:
            givenid=Givenid.objects.get(authid=id)#检查authid是否已经分配过
        except Givenid.DoesNotExist:
            string="%s这个authid还没有分配！"%(id)
            return HttpResponse(string)
        try:
            guest=Guest.objects.get(authid=id)#检查authid是否有微信绑定
            string="%s这个authid分配过，但是已经有人绑定了！"%(id)
            return HttpResponse(string)
        except Guest.DoesNotExist:
            guest=Guest(name=req['name'], img=req['img'], authid=id)#建立新的Guest
            guest.save()
            string="%s与%s绑定成功！"%(req['name'],id)
            return HttpResponse(string)
    else:
        return HttpResponse("没有用POST!")



@csrf_exempt
def datapost(request):#从微信端发消息，始终都有头像信息
    print('dataposthere')
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        content = req['msg']
        name=req['name']
        img=req['img']
        msg=Msg(content=content, img=img, name=name)
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

def encodeHTML(str):
    return str.replace("&", "&amp;") \
    .replace("<", "&lt;") \
    .replace(">", "&gt;") \
    .replace("\"", "&quot;") \
    .replace("'", "&#39;");

#以下是网页端函数
@csrf_exempt
def danmusubmit(request):
    if request.method == 'POST':
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            return HttpResponse('server error')
        msg=Msg(content= encodeHTML(request.POST['msg']),name=guest.name, img='static/image/anonymous.png')
        return HttpResponse('0')
    else:
        HttpResponseRedirect(reverse('live:index'))

@csrf_exempt
def commentsubmit(request):
    if request.method == 'POST':
        try:
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:
            return HttpResponse('server error')
        comment=Comment(content=encodeHTML(request.POST['msg']),name=guest.name, img=guest.img)
        comment.save()
    else:
        HttpResponseRedirect(reverse('live:index'))



def poll(request):
#danmu & comment
    danmu_list=[]
    com_list=[]
    dict={}
    danmus=Msg.objects.all().order_by("id")
    comments=Comment.objects.all().order_by("id")
    if 'danmucount' in request.session and 'commentcount' in request.session:
        danmucount=request.session['danmucount']
        commentcount=request.session['commentcount']
        danmus.filter(id__gte=danmucount)
        comments.filter(id__gte=commentcount)
        for danmu in danmus:
            dict2={}
            dict2['danmu_name']=danmu.name
            dict2['danmu_img']=danmu.img
            dict2['danmu_content']=danmu.content
            dict2['danmu_time']=str(danmu.send_time)
            danmu_list.append(dict2)
        for comment in comments:
            dict2={}
            dict2['comment_name']=comment.name
            dict2['comment_img']=comment.img
            dict2['comment_content']=comment.content
            dict2['comment_time']=str(comment.send_time)
            comment_list.append(dict2)
    dict['danmu']=danmu_list
    dict['comment']=com_list
    if danmus.count()>0:
        request.session['danmucount']=danmus.last().id
    else:
        request.session['danmucount']=0
    if comments.count()>0:
        request.session['commentcount']=comments.last().id
    else:
        request.session['commentcount']=0
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

    resp=json.dumps(dict,ensure_ascii=False)
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

    else:
        try:#若Guest中有，则找到绑定的用户
            guest=Guest.objects.get(authid=request.session['authid'])
        except Guest.DoesNotExist:#若出错，则说明当前session尚未绑定，返回AnonymousUser
            guest=Guest.objects.get(authid='0000')
    request.session.save()
    print(request.session['authid'])
    msgs = Msg.objects.all()
    return render(request, 'index.html', {'msgs':msgs}, {'guest':guest})

def locating(ip):
    url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ip
    data = req.urlopen(url).read().decode('utf-8')
    dict = json.loads(data)
    return dict

def test(request):
    if "authid" not in request.session:#若首次登录，则分配给当前session  authid
       while(1):
            id= Genauthid()
            guest=Guest.objects.filter(authid=id)
            if len(guest)==0:
                request.session['authid']=id
                request.session.save() 
                guest=Guest(authid=id,ip=request.META['REMOTE_ADDR'])
                addr=locating(request.META['REMOTE_ADDR'])
                if len(addr["province".replace(" ","")])>0:
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
                    if len(addr["province".replace(" ","")])>0:
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
