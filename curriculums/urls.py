from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    path('curriculum/', views.curriculum_view, name = 'my'),
    path('curriculum/panel/', views.curriculum_panel, name = 'panel')
]
