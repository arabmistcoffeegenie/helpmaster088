from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CVUpload(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s CV uploaded on {self.uploaded_at}"

class JobApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, default="Untitled")  # Default provided
    company = models.CharField(max_length=255, default="Unknown")       # Default provided
    application_date = models.DateField(default=timezone.now)           # Default provided
    status = models.CharField(max_length=50, default='Submitted')

    def __str__(self):
        return f"{self.student.username} - {self.job_title} at {self.company}"
