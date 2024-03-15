from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Source, UserIncome
from  userpreferences.models import UserPreference
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
import json



def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
@login_required(login_url='/authentication/login') 
def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    preferences = UserPreference.objects.get(user=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'source': source,
        'incomes': income,
        'preferences': preferences,
        'page_obj': page_obj,
    }
    
    return render(request, 'income/index.html' , context)

@login_required(login_url='/authentication/login')
def add_income(request):
    
    sources = Source.objects.all()

    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date, source=source, description=description)
        messages.success(request, 'Income saved successfully')
        return redirect('income')

def is_user_authenticated(user):
    """
    Custom test to check if the user is authenticated.
    """
    return user.is_authenticated

def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Source of income removed')
    return redirect('income')

def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'source': source,
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()
        messages.success(request, 'Source Of Income updated successfully')
        return redirect('income')
protected_after_logout = user_passes_test(lambda u: not u.is_authenticated, login_url='/authentication/login')
