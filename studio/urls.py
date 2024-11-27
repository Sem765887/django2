from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.indexacc, name='profile'),
    path('account/filter/', views.indexacc_filter, name='profile_filter'),
    path('signup/', views.signup, name='signup'),
]