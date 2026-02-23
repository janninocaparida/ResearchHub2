from django.db import models


class Students(models.Model):
    """Model representing a Student in the ResearchHub system"""
    
    s_id = models.IntegerField(
        unique=True,
        help_text="Unique student identifier"
    )
    s_name = models.CharField(
        max_length=64,
        help_text="Full name of the student"
    )
    s_dept = models.CharField(
        max_length=64,
        help_text="Department of the student"
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Students"
    
    def __str__(self):
        return f"{self.s_name} (ID: {self.s_id})"