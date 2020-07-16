"""accessCode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from code import views

urlpatterns = [
    # path('admin/', admin.site.urls),  # 博客后台登录页
    url(r'^$', views.index, name='index'),  # 首页
    path('sim', views.sim_content, name='sim-content'),  # 短信详情页
    path('sim_update/', views.sim_update),  # 短信详情页

]