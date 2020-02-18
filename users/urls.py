from django.conf.urls import url
from users.views import *

urlpatterns = [
        url(r'^list/', UserListView.as_view(),name='user_list'),
        url(r'^userstatus/', UserStatusView.as_view(),name='userstatus'),
]