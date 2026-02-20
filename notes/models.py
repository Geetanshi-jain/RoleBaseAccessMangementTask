from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField()
    is_work = models.BooleanField(default=False)

    deletion_request = models.BooleanField(default=False)
    manager_request = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'),
                 ('approved', 'Approved'),
                 ('rejected', 'Rejected')),
        default='pending'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.notes
