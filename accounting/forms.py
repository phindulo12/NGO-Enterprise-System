from django import forms
from .models import Budget, Expense

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['project', 'allocated_amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['budget', 'category', 'description', 'amount', 'date_incurred']
        widgets = {
            'date_incurred': forms.DateInput(attrs={'type': 'date'}),
        }
