from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/new/', views.budget_create, name='budget_create'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/new/', views.expense_create, name='expense_create'),
    path('import/', views.importExcel, name='pushExcel')
]
