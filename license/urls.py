from django.conf.urls import url, include
from . import views


urlpatterns = [
    url('stream/', views.stream,name='stream'),
    url('displaylog/',views.displaylog,name='displaylog'),
    url('addowner/',views.addOwner,name='addowner'),
    url('videofeed', views.video_feed, name='videofeed'),
    url('',views.home,name='home'),

]