from django.urls import path
from . import views
from django.urls import re_path
from .views import MyProtectedView


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]

urlpatterns += [
    path('protected/', MyProtectedView.as_view(), name='protected'),
]