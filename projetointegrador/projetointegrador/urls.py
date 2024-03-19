from django.contrib import admin
from django.urls import include, path
# Importe as views corretamente do aplicativo 'projeto'
from projeto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projeto.urls')),
]
