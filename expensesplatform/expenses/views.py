from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Expense, Category
from django.contrib import messages

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'expenses/index.html', context)

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
        
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        
        return render(request, 'expenses/add_expense.html', context)

        #Expense.objects.create(amount=amount, date=date, category=category, description=description)
    
@login_required(login_url='/authentication/login')
def add_income(request):
    return render(request,'expenses/income.html')

def is_user_authenticated(user):
    """
    Custom test to check if the user is authenticated.
    """
    return user.is_authenticated

protected_after_logout = user_passes_test(lambda u: not u.is_authenticated, login_url='/authentication/login')
