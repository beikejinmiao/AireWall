"""
URL configuration for AireWall project.

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
from django.urls import include
from aireadmin.views import login as login_view


admin.site.site_header = "极智安AireWall Admin"
admin.site.site_title = "极智安AireWall Admin Portal"
admin.site.index_title = "Welcome to JZA AireWall Portal"

urlpatterns = [
    re_path(r'^$', login_view.index),
    path('admin/', admin.site.urls),
    path('index/', login_view.index),
    path('login/', login_view.login),
    path('document/', login_view.document),
    path('logout/', login_view.logout),
    path('captcha/', include('captcha.urls')),
]

