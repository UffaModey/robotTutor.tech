from django.contrib import admin
from django.urls import path, include
from robottutor import views

##added section

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('robottutor.urls')),
    path("<slug:passcodeguiapplink>/", include('robottutor.urls')),
    path("run/", include('robottutor.urls')),
]
