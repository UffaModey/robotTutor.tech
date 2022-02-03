from django.urls import path
from django.contrib import admin
from .views import home
from .views import run
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = "robottutor"


urlpatterns = [
    path("", home, name='home'),
    path("<slug:passcodeguiapplink>/", home, name='home'),
    path("admin/", admin.site.urls),
    path("run/", run, name='run'),
]
urlpatterns += staticfiles_urlpatterns()