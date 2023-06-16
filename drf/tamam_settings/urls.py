from django.contrib import admin
from django.urls import path, include
from tamam_app.views import simple_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tamam_app.urls')),
    path('', simple_view),
]