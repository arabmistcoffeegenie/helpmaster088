from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

STATUS_CHOICES = [
    ('processing', 'Processing'),
    ('completed', 'Completed'),
]

class Assignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Assignment")
    degree = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    # Uploaded brief file (Saved to AWS S3)
    brief = models.FileField(
        storage=S3Boto3Storage(),
        upload_to="assignments/",
        blank=True, null=True
    )

    payment_status = models.CharField(max_length=50, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    # Status field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    # Completed assignment file (Saved to AWS S3)
    completed_file = models.FileField(
        storage=S3Boto3Storage(),
        upload_to="assignments/completed/",
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.title} ({self.student.username})"


# Custom managers for proxy models remain the same.
class PremiumAssignmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(student__profile__premium_member=True)


class NonPremiumAssignmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(student__profile__premium_member=False)


class PremiumAssignment(Assignment):
    objects = PremiumAssignmentManager()

    class Meta:
        proxy = True
        verbose_name = "Premium Assignment"
        verbose_name_plural = "Premium Assignments"


class NonPremiumAssignment(Assignment):
    objects = NonPremiumAssignmentManager()

    class Meta:
        proxy = True
        verbose_name = "Non-Premium Assignment"
        verbose_name_plural = "Non-Premium Assignments"
