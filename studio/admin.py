from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Request)
admin.site.register(Category)
admin.site.register(UserProfile)