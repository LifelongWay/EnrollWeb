from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static
app_name = 'courses'

urlpatterns = [
        # path('dashboard', views.sections_view, name = 'dashboard'), # for stud-s and teachers
        path('panel/', views.courses_and_sections_view, name = 'panel'), # management panel - should be secured
        path('panel/add/<str:type>/', views.courses_and_sections_view, name = 'add'),
        path('panel/add/<str:course_name>/<int:course_id>/', views.courses_and_sections_view, name = 'add-section'),
        path('panel/delete/<str:type>/<int:pk>', views.courses_and_sections_delete_view, name = 'delete'),
        path('panel/edit/<str:type>/<int:pk>', views.courses_and_sections_edit_view, name = 'edit'),
        # paths for Students and Teachers 
        path('my_sections/dashboard/', views.my_sections_view, name = 'my-sections')
    ]