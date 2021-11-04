from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from carwashapp import views

urlpatterns = [
    path('',include('carwashapp.urls')),
    path('admin/', admin.site.urls),
]

