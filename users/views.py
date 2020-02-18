from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic import View,TemplateView
from django.http.response import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.

class UserListView(LoginRequiredMixin,View):
    def get(self,request):
        userlist = User.objects.all()
        return render(request,'user_list.html',{'userlist':userlist})




class UserStatusView(View):
    def get(self,request):
        # print(request.GET)
        user = User.objects.get(id=request.GET.get('id'))
        user_status = int(user.is_active)
        print(user_status)
        try:
            if user_status == 1:
                User.objects.filter(id=request.GET.get('id')).update(is_active=0)
            else:
                User.objects.filter(id=request.GET.get('id')).update(is_active=1)
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'mag':'状态修改失败'})
        return  JsonResponse({'status':0,'msg':'状态修改成功'})