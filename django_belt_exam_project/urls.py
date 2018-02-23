from django.conf.urls import url, include 
from django.contrib import admin 
 
urlpatterns = [ 
    url(r'^', include('apps.users_app.urls')),
    url(r'^travels/', include('apps.travel_buddy_app.urls')),
    url(r'^$', include('apps.travel_buddy_app.urls'))
] 
