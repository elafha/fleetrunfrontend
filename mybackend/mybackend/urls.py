"""
URL configuration for mybackend project.

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
from django.urls import path, include
from mybackendapp.views import *
from rest_framework import routers

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used

urlpatterns = [
    path('admin/', admin.site.urls),
]
#     path('api/v1/home', Home.as_view(), name='home'),
#     path('api/v1/login', Login.as_view(), name='login')
#     # path('', include('login.urls')),
#     # path('login/v1', views.login, name='login')
# ]
