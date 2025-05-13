from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from accounting.models import Budget, Expense

def is_project_manager(user):
    return user.groups.filter(name='project_manager').exists()


@login_required
def ubuntu_dashboard(request):
    budgets = Budget.objects.all()
    expenses = Expense.objects.all()
    total_budget = sum([budget.allocated_amount for budget in budgets])
    total_expenses = sum([expense.amount for expense in expenses])
    remaining_budget = total_budget - total_expenses

    context = {
        'budgets': budgets,
        'expenses': expenses,
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
    }
    return render(request, 'ubuntu_project/ubuntu_dashboard.html', context)

