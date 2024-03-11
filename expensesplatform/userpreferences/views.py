from django.shortcuts import render

# Create your views here.
def preferences(request):
    return render(request, 'userpreferences/index.html')

def profile(request):
    return render(request,'userpreferences/profile.html')
