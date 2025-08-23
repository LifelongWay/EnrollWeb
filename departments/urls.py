from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('panel/', views.departments_view, name = 'panel'),
    path('panel/add', views.departments_add_view, name = 'add'),
    path('panel/edit/<int:dept_id>/', views.departments_edit_view, name = 'edit'),
    path('panel/delete/<int:dept_id>', views.departments_delete_view, name = 'delete'),
]
