from django.urls import path
from . import views

urlpatterns = [
   path('user-preference/',views.preferences, name='user-preference'),
   path('user-profile', views.profile, name='user-profile')
]
