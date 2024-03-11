from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'expenses/index.html')

@login_required(login_url='/authentication/login')
def add_expense(request):
    return render(request, 'expenses/add_expense.html')

@login_required(login_url='/authentication/login')
def add_income(request):
    return render(request,'expenses/income.html')

def is_user_authenticated(user):
    """
    Custom test to check if the user is authenticated.
    """
    return user.is_authenticated

protected_after_logout = user_passes_test(lambda u: not u.is_authenticated, login_url='/authentication/login')
