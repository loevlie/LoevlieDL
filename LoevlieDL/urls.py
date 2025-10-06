"""LoevlieDL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from django.conf.urls import url
from Portfolio import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wedding/', include('wedding.urls')),  # Wedding website URLs
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    re_path(r'^logout/$',views.user_logout,name='logout'),
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^$',views.index,name='index'),
    re_path(r'^timeline/$',views.timeline,name='timeline'),
    re_path(r'^about_me/$',views.about_me,name='about_me'),
    re_path(r'^contact/$',views.contact,name='contact'),
    re_path(r'^portfolio/$',views.portfolio,name='portfolio'),
    re_path(r'^publications/$',views.publications,name='publications'),
    #re_path(r'^Blog/$',views.blog,name='Blog'),
    re_path(r'^Blog/$', views.blog.as_view(), name='Blog'),
    path('add_post/',views.AddPostView,name='add_post'),
    path('', include('Portfolio.urls')), # new
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('edit/<slug:slug>/', views.UpdatePostView, name='update_post'),
] + static(settings.STATIC_URL,document_root=settings.STATIC_DIR) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
