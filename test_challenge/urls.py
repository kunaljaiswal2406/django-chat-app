"""test_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from tastypie.api import NamespacedApi

from account.api import AccountResource
from chat.api import ChatResource

v1_api = NamespacedApi(api_name="v1", urlconf_namespace="namespace")
v1_api.register(AccountResource())
v1_api.register(ChatResource())


urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^api/", include(v1_api.urls)),
]
