from django.contrib import admin
from django.urls import path

app_name = 'mail'
from .views import index, run_parse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('/parse', run_parse, name='run_parse')
]
