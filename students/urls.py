from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_view, name="create"),
    path('create_stud', views.create_student, name="create_student"),
    
]  
    