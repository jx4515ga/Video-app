from django.urls import path 
from . import views 
# Paths to navegate throught the app 
urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list', views.video_list, name='video_list'),
]