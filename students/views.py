from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Students
from .forms import StudentsForm


def home(request):
    """Display all students in a list view with search functionality"""
    students = Students.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            s_name__icontains=search_query
        ) | students.filter(
            s_dept__icontains=search_query
        )
    
    context = {
        'students': students,
        'search_query': search_query
    }
    return render(request, "home.html", context)


def create_view(request):
    """Display the create student form"""
    if request.method == "POST":
        form = StudentsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student created successfully!")
                return redirect("home")
            except IntegrityError:
                form.add_error('s_id', 'A student with this ID already exists.')
                return render(request, "create.html", {"form": form})
        else:
            return render(request, "create.html", {"form": form})
    else:
        form = StudentsForm()
    
    return render(request, "create.html", {"form": form})


def update_view(request, id):
    """Display the update student form"""
    student = get_object_or_404(Students, pk=id)
    
    if request.method == "POST":
        form = StudentsForm(request.POST, instance=student)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student updated successfully!")
                return redirect("home")
            except IntegrityError:
                form.add_error('s_id', 'A student with this ID already exists.')
                return render(request, "update.html", {"form": form, "student": student})
        else:
            return render(request, "update.html", {"form": form, "student": student})
    else:
        form = StudentsForm(instance=student)
    
    return render(request, "update.html", {"form": form, "student": student})


def delete_view(request, id):
    """Display delete confirmation page"""
    student = get_object_or_404(Students, pk=id)
    
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect("home")
    
    return render(request, "confirm_delete.html", {"student": student})


# Legacy functions for backward compatibility (can be removed later)
def create_student(request):
    """Backward compatibility wrapper"""
    return create_view(request)


def update_student(request, id):
    """Backward compatibility wrapper"""
    return update_view(request, id)


def delete_student(request, id):
    """Backward compatibility direct delete without confirmation"""
    student = get_object_or_404(Students, pk=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect("home")
