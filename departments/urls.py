from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('panel/', views.departments_view, name = 'panel'),
    path('panel/add', views.departments_add_view, name = 'add')
]
