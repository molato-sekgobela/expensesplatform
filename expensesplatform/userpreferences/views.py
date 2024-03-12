from django.shortcuts import render
import os
import json
from .models import UserPreference
from django.conf import settings
from django.contrib import messages

# Create your views here.
def preferences(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preference = None
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if exists:
        user_preference = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':

        return render(request, 'userpreferences/index.html',{'currency_data': currency_data,'user_preference': user_preference})
    else:
        currency = request.POST['currency']
        if exists:
            user_preference = UserPreference.objects.get(user=request.user)
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=request.POST['currency'])
        messages.success(request, 'Changes saved')
        return render(request, 'userpreferences/index.html',{'currency_data': currency_data,'user_preference': user_preference})

def profile(request):
    return render(request,'userpreferences/profile.html')
