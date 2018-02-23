from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url(r'^$', views.index), # Dashboard (Travels)
    url(r'^add/$', views.add_plan),
    url(r'^add_new_trip/$', views.add_new_trip),
    url(r'^destination/([0-9]{1,})/$', views.destination),
    url(r'^join/([0-9]{1,})/$', views.join),
] 
