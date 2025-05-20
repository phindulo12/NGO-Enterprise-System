from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import data, Budget, Expense
from .forms import BudgetForm, ExpenseForm
from tablib import Dataset
from .resources import DataResource
from .data_cleaning import Data_Cleaner


def importExcel(request):
    if request.method == 'POST':
        if 'data' not in request.FILES:
            messages.error(request, "No file uploaded.")
            return render(request, 'accounting/AddData.html')

        data_resource = DataResource()
        dataset = Dataset()
        new_data = request.FILES['data']

        # Save uploaded file temporarily
        with open('temp_uploaded_file.xlsx', 'wb+') as temp:
            for chunk in new_data.chunks():
                temp.write(chunk)

        # Clean the uploaded file
        cleaned_path = Data_Cleaner('temp_uploaded_file.xlsx')

        # Read cleaned file and load it into tablib
        with open(cleaned_path, 'rb') as f:
            imported_Data = dataset.load(f.read(), format='xlsx')

        for i in imported_Data:
            value = data(
                i[0], i[1], i[2], i[3], i[4], 
                i[5], i[6], i[7], i[8], i[9],
            )
            value.save()  # Fixed

    return render(request, 'accounting/AddData.html')





def is_accountant(user):
    return user.groups.filter(name='accountant').exists()

@login_required
@user_passes_test(is_accountant)
def accountant_dashboard(request):
    return render(request, 'accounting/dashboards.html')

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
