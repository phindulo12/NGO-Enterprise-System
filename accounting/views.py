from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm

def is_accountant(user):
    return user.groups.filter(name='accountant').exists()

@login_required
@user_passes_test(is_accountant)
def accountant_dashboard(request):
    return render(request, 'accounting/dashboard.html')

# @login_required
# @user_passes_test(is_accountant)
def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'accounting/budget_list.html', {'budgets': budgets})

# @login_required
# @user_passes_test(is_accountant)
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'accounting/budget_form.html', {'form': form})

# @login_required
# @user_passes_test(is_accountant)
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'accounting/expense_list.html', {'expenses': expenses})

# @login_required
# @user_passes_test(is_accountant)
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.incurred_by = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'accounting/expense_form.html', {'form': form})
