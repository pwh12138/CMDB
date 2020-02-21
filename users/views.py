from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView, TemplateView
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.hashers import make_password
from users.models import *
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# class UserListView(LoginRequiredMixin,View):
#     def get(self,request):
#         userlist = User.objects.all()
#         return render(request,'user_list.html',{'userlist':userlist})

# 分页范围  防止越界的一个处理算法
def my_page(page_obj, paginator, page_nums=3):
    current_index = page_obj.number
    # 显示总页数
    # page_nums = 5
    # 限制显示范围 设置起始值
    start = current_index - page_nums // 2
    end = current_index + (page_nums // 2 + 1)
    # 如果小于第一页 就从第一页开始取
    if start <= 1:
        start = 1
    # 如果大约总页数  就取到最大页数
    if end >= paginator.num_pages:
        end = paginator.num_pages + 1
    # 如果取出页数后发现没有达到所需显示总页数（page_nums）
    current_pages_num = end - start
    # 当前end已经取到了最后
    if (end == paginator.num_pages + 1):
        # 所需显示总页数不够,就向前取
        start = start - (page_nums - current_pages_num)
    else:
        # 否则就向后取
        end = end + (page_nums - current_pages_num)
    # 如果小于第一页 就从第一页开始取
    if start <= 1:
        start = 1
    # 如果大约总页数  就取到最大页数
    if end >= paginator.num_pages:
        end = paginator.num_pages + 1
    return range(start, end)


class UserListView(LoginRequiredMixin,ListView):
    template_name = 'user_list.html'
    model = User
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_range'] = self.page_range(context['page_obj'],context['paginator'])
        return context

    def page_range(self, page_obj, paginator):
        current_num = page_obj.number
        start = current_num - 2
        end = current_num + 3
        if start < 1:
            start = 1
            end = end + 5 - (end - start)

        if end > paginator.num_pages:
            end = paginator.num_pages + 1
            start = start - (5 - (end - start))
        return range(start, end)

class UserStatusView(LoginRequiredMixin,View):
    def get(self,request):
        # print(request.GET)
        user = User.objects.get(id=request.GET.get('id'))
        user_status = int(user.is_active)
        # print(user_status)
        try:
            if user_status == 1:
                User.objects.filter(id=request.GET.get('id')).update(is_active=0)
            else:
                User.objects.filter(id=request.GET.get('id')).update(is_active=1)
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'mag':'状态修改失败'})
        return  JsonResponse({'status':0,'msg':'状态修改成功'})

# 批量添加用户
def faker_data():
    from faker import Faker
    for i in range(10):
        faker = Faker(locale='zh_CN')
        user = User()
        user.username = Faker().first_name()
        user.password = make_password(123456)
        user.email = faker.email()
        user.save()
        profile = Profile()
        profile.name_cn = faker.name()
        profile.wechat = faker.phone_number()
        profile.phone = faker.phone_number()
        profile.profile = user
        profile.save()

class UseraddView(LoginRequiredMixin,TemplateView):
    template_name = 'user_add.html'
    def post(self,request):
        # print(request.POST)
        try:
            data = request.POST
            user = User()
            user.username = data.get('username')
            user.password = make_password(data.get('password'))
            user.email = data.get('email')
            user.save()
            profile = Profile()
            profile.name_cn = data.get('name_cn')
            profile.wechat = data.get('wechat')
            profile.phone = data.get('phone')
            profile.profile = user
            profile.save()
        except Exception as e:
            print(e)
            return  JsonResponse({'status':1,'msg':'添加失败'})
        return JsonResponse({'status':0,'msg':'添加成功'})

class UserUpdateView(LoginRequiredMixin,TemplateView):
    template_name = 'user_update.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_obj'] = User.objects.get(id=self.request.GET.get('id'))
        return context
    def post(self,request):
        # print(request.POST)
        try:
            data = request.POST
            user = User.objects.get(id=request.POST.get('id'))
            user.username = data.get('username')
            user.password = make_password(data.get('password'))
            user.email = data.get('email')
            user.save()
            # 一对一关系 找到需要修改的profile信息
            profile = user.profile
            profile.name_cn = data.get('name_cn')
            profile.wechat = data.get('wechat')
            profile.phone = data.get('phone')
            profile.profile = user
            profile.save()
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'msg':'用户信息更新失败'})
        return  JsonResponse({'status':0,'msg':'用户信息更新成功'})


class UserDeleteView(LoginRequiredMixin,View):
    def get(self,request):
        # print(request.GET)
        user = User.objects.get(id=request.GET.get('id'))
        # print(user_status)
        try:
            user.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'mag':'用户删除失败'})
        return  JsonResponse({'status':0,'msg':'用户删除成功'})


# 用户组

class GroupListView(LoginRequiredMixin,ListView):
    template_name = 'group_list.html'
    model = Group
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_range'] = self.page_range(context['page_obj'], context['paginator'])
        return context

    def page_range(self,page_obj,paginator):
        return  my_page(page_obj,paginator,5)



class GroupaddView(LoginRequiredMixin,ListView):
    template_name = 'group_add.html'
    model = User
    def post(self,request):
        # print(request.POST)

        try:
            group = Group()
            group.name = request.POST.get('name')
            group.save()

            for i in request.POST.getlist('group_user'):
                group.user_set.add(User.objects.get(id=i))
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'msg':'添加用户组失败'})
        return JsonResponse({'status':0,'msg':'添加用户组成功'})




class GroupUpdateView(LoginRequiredMixin,ListView):
    template_name = 'group_update.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['group_obj'] = Group.objects.get(id=self.request.GET.get('id'))
        return context

    def post(self,request):
        # print(request.POST)
        try:
            data = request.POST
            group = Group.objects.get(id=data.get('id'))
            group.name = data.get('name')
            group.save()

            group.user_set.clear()
            for i in data.getlist('group_user'):
                group.user_set.add(User.objects.get(id=i))
        except Exception as e:
            print(e)
            return  JsonResponse({'status':1,'msg':'用户组更新失败'})
        return  JsonResponse({'status':0,'msg':'用户组更新成功'})






class GroupDeleteView(LoginRequiredMixin,View):


    def get(self,request):
        # print(request.GET)
        group = Group.objects.get(name=request.GET.get('groupname'))

        try:
            group.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'status':1,'mag':'用户组删除失败'})
        return  JsonResponse({'status':0,'msg':'用户组删除成功'})


# 权限管理

class PermListView(LoginRequiredMixin,ListView):
    template_name = 'perm_list.html'
    model = Permission

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(name__regex='[A-Za-z]')
        return  queryset


