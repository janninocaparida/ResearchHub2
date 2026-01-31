from django.db import models

class Students(models.Model):
    s_id = models.IntegerField()
    s_name = models.CharField(max_length=64)
    s_dept = models.CharField(max_length=64)