from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic import View,TemplateView
from django.http.response import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
# Create your views here.



class BaseView(View):
    def get(self,request):
        return  render(request,'base.html')

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['host_error_count'] = 5
        return  context

# class IndexView(View):
#     def get(self,request):
#         return render(request,'index.html',{'host_error_count':10})

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self,request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username,password=password)
        if user:
        # if username == 'admin' and password == '123456':
            login(request,user)
            res = {'status':0,'msg':'登陆成功'}
        else:
            res = {'status':1,'msg':'登陆失败,重新验证'}
        return JsonResponse(res)

class LogOutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))