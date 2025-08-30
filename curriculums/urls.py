from django.urls import path
from . import views

app_name = 'curriculums'

urlpatterns = [
    path('my/', views.my_curriculum, name = 'my'),
    path('panel/', views.curriculums_editor, name = 'editor')
]
