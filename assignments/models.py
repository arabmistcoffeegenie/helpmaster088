from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage  # ✅ Ensures AWS S3 storage is used

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

    # ✅ Uploaded brief file (Stored in AWS S3)
    brief = models.FileField(
        upload_to="assignments/",
        storage=default_storage,  # ✅ Ensures AWS S3 storage is used
        blank=True, null=True
    )

    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Status field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    # ✅ Completed assignment file (Stored in AWS S3)
    completed_file = models.FileField(
        upload_to="assignments/completed/",
        storage=default_storage,  # ✅ Ensures AWS S3 storage is used
        blank=True, null=True
    )

    def save(self, *args, **kwargs):
        """
        ✅ Ensures completed assignments uploaded via Admin Panel are stored in AWS S3.
        """
        if self.completed_file and not self.completed_file.name.startswith("assignments/completed/"):
            self.completed_file.name = f"assignments/completed/{self.completed_file.name}"
        
        if self.brief and not self.brief.name.startswith("assignments/"):
            self.brief.name = f"assignments/{self.brief.name}"

        super().save(*args, **kwargs)  # ✅ Ensures proper file saving in AWS S3

    def __str__(self):
        return f"{self.title} ({self.student.username})"

# ✅ Corrected Manager (Use Only If UserProfile Exists)
class PremiumAssignmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(student__is_staff=True)

class NonPremiumAssignmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(student__is_staff=False)

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
