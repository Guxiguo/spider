"""
URL configuration for mewe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from django.urls import re_path as url
from mainapp import views
urlpatterns = [
    url('^$', views.mewe_web, name='index'),  # 主页
    path('mewe/', views.mewe_web, name='mewe'),  # Mewe
    path('line/', views.line_web, name='line'),  # Line
    path('mewe_port/', views.mewe_port, name='mewe_port'),  # mewe_port
    path('mewe_data_port/', views.mewe_data_port, name='mewe_data_port'),  # mewe_port
    path('line_port/', views.line_port, name='line_port'),  # line_port
    path('line_data_port/', views.line_data_port, name='line_data_port'),  # mewe_port
]
