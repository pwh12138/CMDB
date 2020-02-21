from django.conf.urls import url
from users.views import *

urlpatterns = [
        url(r'^list/', UserListView.as_view(),name='user_list'),
        url(r'^add/', UseraddView.as_view(),name='user_add'),
        url(r'^update/',UserUpdateView.as_view(),name='user_update'),
        url(r'^userstatus/', UserStatusView.as_view(),name='userstatus'),
        url(r'^userdelete/', UserDeleteView.as_view(),name='userdelete'),

        url(r'^group/list/', GroupListView.as_view(),name='group_list'),
        url(r'^group/add/', GroupaddView.as_view(), name='group_add'),
        url(r'^group/update/', GroupUpdateView.as_view(), name='group_update'),
        url(r'^group/userdelete/', GroupDeleteView.as_view(),name='group_delete'),


        url(r'^perm/list', PermListView.as_view(),name='perm_list'),
]