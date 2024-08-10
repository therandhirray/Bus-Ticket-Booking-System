from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/',home),
    path('about/',about),
    path('aboutus/',aboutus),
    path('help/',help),

    path('contact/',contact),
    path('',home),
    path('myprofile/',myprofile),
    path('findbus/',findbus),
    path('booking/<int:id>',booking),
    path('booked/<int:id>',booked),
    #My Tickets
    path('seebookings/',seebookings),

    path('cancellings/',cancellings),
    path('detail/<int:id>',detail),
    path('cancel/<int:id>',cancel),
    path('signup/',signup),
    path('signin/',signin),
    path('success/',success),
    path('signout/',signout),
]