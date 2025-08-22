from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static
app_name = 'courses'

urlpatterns = [
    path('panel/', views.courses_and_sections_view, name = 'panel'), # management panel - should be secured
    path('panel/add/<str:type>/', views.courses_and_sections_view, name = 'add'),
    path('panel/delete/<str:type>/<int:pk>', views.courses_and_sections_delete_view, name = 'delete'),
    path('panel/edit/<str:type>/<int:pk>', views.courses_and_sections_edit_view, name = 'edit'),

    ]