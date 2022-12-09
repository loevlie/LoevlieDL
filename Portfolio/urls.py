from django.urls import re_path,path, include, re_path
from . import views
# from django.conf.urls import url

app_name = 'Portfolio'

urlpatterns = [
    path('success/',views.successView,name='success'),
    path('', views.PostList.as_view(), name='home'),
    #path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('add_post/',views.AddPostView,name='add_post'),
    re_path(r'^logout/$',views.user_logout,name='logout'),
    #path('<slug:slug>/', views.post_detail, name='post_detail'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    #re_path(r'^Blog/$', views.blog, name='Blog'),
]