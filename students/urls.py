from django.urls import path
from . import views

urlpatterns = [
    # Main listing
    path('', views.home, name='home'),
    
    # Create operations
    path('create/', views.create_view, name="create"),
    path('create_stud', views.create_student, name="create_student"),
    
    # Update operations
    path('update/<int:id>/', views.update_view, name="update_view"),
    path('update_stud/<int:id>/', views.update_student, name="update_student"),
    
    # Delete operations
    path('delete/<int:id>/', views.delete_view, name="delete_view"),
    path('delete_confirm/<int:id>/', views.delete_student, name="delete_student"),  # Legacy endpoint
]  
    