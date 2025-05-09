from django.contrib.auth.models import AbstractUser


from django.db import models


class CustomUser(AbstractUser):

    ROLE_CHOICES = [

        ('admin' , 'Admin'),
        ('project_manager' , 'Project Manager'),
        ('accountant' , 'Accountant'),
        ('staff' , 'staff'),
        ('reporter', 'Reporter'),
    ]

    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='staff')
    

    def __str__(self):
        return f"{self.username} ({self.role})"