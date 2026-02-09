from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} ({self.roll_no})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Present")

    def __str__(self):
        return f"{self.student.user.username} - {self.timestamp}"