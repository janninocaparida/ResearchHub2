from django import forms
from .models import Students


class StudentsForm(forms.ModelForm):
    """Django form for creating and updating Student records with validation"""
    
    s_id = forms.IntegerField(
        label="Student ID",
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter unique student ID',
            'required': 'required'
        })
    )
    
    s_name = forms.CharField(
        label="Student Name",
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter full name',
            'required': 'required'
        })
    )
    
    s_dept = forms.CharField(
        label="Department",
        max_length=64,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter department name',
            'required': 'required'
        })
    )
    
    class Meta:
        model = Students
        fields = ['s_id', 's_name', 's_dept']
    
    def clean_s_id(self):
        """Validate Student ID is a positive integer"""
        s_id = self.cleaned_data.get('s_id')
        if s_id is not None and s_id <= 0:
            raise forms.ValidationError("Student ID must be a positive number.")
        return s_id
    
    def clean_s_name(self):
        """Validate Student Name is not empty"""
        s_name = self.cleaned_data.get('s_name')
        if s_name and len(s_name.strip()) == 0:
            raise forms.ValidationError("Student Name cannot be empty.")
        return s_name
    
    def clean_s_dept(self):
        """Validate Department is not empty"""
        s_dept = self.cleaned_data.get('s_dept')
        if s_dept and len(s_dept.strip()) == 0:
            raise forms.ValidationError("Department cannot be empty.")
        return s_dept
