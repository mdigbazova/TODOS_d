from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from . import views
from . import filters


schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    re_path('^schema/', schema_view),
    re_path('^register/', views.RegisterUser.as_view(), name='register'),  # register functionality
    re_path('^todos_list/$', views.TodosList.as_view(), name='todos-list'),
    re_path('^todo/(?P<pk>\d+)/$', views.TodosDetail.as_view(), name='todos-detail'),
    re_path('^todo/(?P<pk>\d+)/url/$', views.TodoDetail.as_view(), name='todo-detail'),
    re_path('^users/$', views.UserList.as_view(), name='user-list'),
    re_path('^user/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-detail'),
    url(r'^search/$', views.FilterView.as_view(), name='searcher'),
    path('', views.api_root),
]


urlpatterns = format_suffix_patterns(urlpatterns)
