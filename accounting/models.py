from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Budget(models.Model):
    project = models.CharField(max_length=100)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.project} Budget"

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    incurred_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_incurred = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"

class data(models.Model):
        Budget_Line = models.CharField(max_length =100)
        SDA = models.CharField(max_length =100)
        description = models.CharField(max_length =100)
        Cost_Category = models.CharField(max_length =100)
        Budget = models.CharField(max_length =100)
        Actual = models.CharField(max_length =100)
        Varience = models.CharField(max_length =100)
        Budget = models.CharField(max_length =100)
        Actual = models.CharField(max_length =100)
        Varience = models.CharField(max_length =100)