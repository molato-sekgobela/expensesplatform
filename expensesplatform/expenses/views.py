from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Expense, Category
from  userpreferences.models import UserPreference
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    

@login_required(login_url='/authentication/login') 
def index(request):
    categories = Category.objects.all()
    expense = Expense.objects.filter(owner=request.user)
    preferences = UserPreference.objects.get(user=request.user)
    paginator = Paginator(expense, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'expenses': expense,
        'preferences': preferences,
        'page_obj': page_obj,
    }
    
    return render(request, 'expenses/index.html' , context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')
    
@login_required(login_url='/authentication/login')
def add_income(request):
    return render(request,'expenses/income.html')

def is_user_authenticated(user):
    """
    Custom test to check if the user is authenticated.
    """
    return user.is_authenticated

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', context)

        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')

protected_after_logout = user_passes_test(lambda u: not u.is_authenticated, login_url='/authentication/login')
