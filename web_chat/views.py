from django.shortcuts import render,HttpResponse
import json
import itertools
import Queue
from django.utils import timezone
import datetime
from user_center.models import UserProfile
from django.core.urlresolvers import resolve, reverse
from cmdb import models
MSG_DIC = {}
def dashboard(request):
    if request.method == 'GET':
        models.Server.objects.values('id','server_name','application')

        return render(request, 'user_center/chat_view.html', {})


def get_contact_list(request):
    user = request.user
    # friend_list_a = user.friends.select_related().values('id','alias','header_image')
    # friend_list_b = user.friends_set.select_related().values('id','alias','header_image')
    friend_list_a = user.friends.select_related()
    friend_list_b = user.friends_set.select_related()
    all_friend = itertools.chain(friend_list_a,friend_list_b)
    all_friend = set(all_friend)
    user_list = []
    for u in all_friend:
        user_dic = {
            'id':u.id,
            'alias':u.alias,
            'header_image':u.header_image
        }
        user_list.append(user_dic)
    return HttpResponse(json.dumps(list(user_list)))
def get_msg(requeset):
    if requeset.method == "GET":
        user = requeset.user
        msg_list = []

        if MSG_DIC.has_key(user.id):
            msg_queue = MSG_DIC[user.id]
            print  msg_queue.qsize()
            if msg_queue.qsize() != 0:
                for i in range(msg_queue.qsize()):
                    msg = msg_queue.get()
                    msg_list.append(msg)
            else:
                try:
                    msg = msg_queue.get(timeout=5)
                    msg_list.append(msg)
                except Queue.Empty:
                    print 'queue empty except !'
        else:
            MSG_DIC[user.id] = Queue.Queue()

        return HttpResponse(json.dumps(msg_list))

def send_msg(requeset):
    if requeset.method == 'POST':
        user = requeset.user
        data = requeset.POST.get("data",None)
        data = json.loads(data)
        to_user_id = int(data['to'])
        print 'from send_msg'
        print data

        if not MSG_DIC.has_key(to_user_id):
            MSG_DIC[to_user_id] = Queue.Queue()
        print MSG_DIC
        current_time = timezone.now()

        current_time = datetime.datetime.strftime(current_time,'%Y-%m-%d %H:%M:%S')
        msg_dic = {
            'from':user.id,
            'time_tag':current_time,
            'alias':user.alias,
            'msg':data['msg'],
            'header_image':user.header_image
        }
        MSG_DIC[to_user_id].put(json.dumps(msg_dic))

    return HttpResponse("send ok")


def test(request):
    print request.user.user_permissions
    url_resovle_obj = resolve(request.path_info)
    print 'url_name',url_resovle_obj.url_name
    print 'url_resovle_obj',url_resovle_obj
    current_url_namespace = url_resovle_obj.url_name
    return HttpResponse("send ok")
