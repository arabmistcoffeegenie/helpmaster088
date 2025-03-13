from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('completed', 'Completed'),
]

PAYMENT_STATUS_CHOICES = [
    ('unpaid', 'Unpaid'),
    ('pending', 'Pending'),
    ('paid', 'Paid'),
]

class Assignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Assignment")
    degree = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    # ✅ Student uploaded brief file (Stored in AWS S3)
    brief = models.FileField(
        upload_to="assignments/",
        blank=True, 
        null=True
    )

    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Status field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    # ✅ Admin uploaded completed file (Stored in AWS S3)
    completed_file = models.FileField(
        upload_to="assignments/completed/",
        blank=True, 
        null=True
    )

    def save(self, *args, **kwargs):
        """
        ✅ Ensures that completed_file gets stored in AWS S3.
        ✅ Works for both student-uploaded and admin-uploaded files.
        """
        if self.completed_file and not self.completed_file.name.startswith("assignments/completed/"):
            # ✅ Force correct path in AWS S3
            self.completed_file.name = f"assignments/completed/{self.completed_file.name}"

        if self.brief and not self.brief.name.startswith("assignments/"):
            # ✅ Force correct path in AWS S3
            self.brief.name = f"assignments/{self.brief.name}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.student.username})"
