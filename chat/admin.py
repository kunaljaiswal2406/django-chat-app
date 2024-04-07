from django.contrib import admin

# Register your models here.

from django.contrib import admin
from tastypie.models import ApiKey

admin.site.unregister(ApiKey)
