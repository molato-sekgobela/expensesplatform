from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse
from .utils import token_generator
from django.http import HttpResponse

# Create your views here.


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):

        post_data = request.POST
        username = post_data['username']
        email = post_data['email']
        password = post_data['password']

        context = {
            'fieldValues': request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': token_generator.make_token(user)})
                email_subject = 'Activate your account'
                email_body = 'Hi ' + user.username + ' Please use this link to verify your account\n http://' + domain + link
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@techwithmolato.co.za",
                    [email],
                    
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/register.html')
            else:
                messages.error(request, 'Email is already in use')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')
    
class VerificationView(View):
    def get(self, request, uid, token):
        #User.objects.filter(id=uid).update(is_active=True)
        #messages.success(request, 'Account activated successfully')
        #return render(request, 'authentication/activate.html')
        try:
            id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass
      
        return redirect('login')
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry Email is in use.'}, status=409)
        

        return JsonResponse({'email_valid': True})
    
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry Username is in use.'}, status=409)
        

        return JsonResponse({'username_valid': True})
        
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                    return redirect('expenses')
                messages.error(request, 'Account is not active, please check your email for the activation link')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill all fields') 
        return render(request, 'authentication/login.html')
    
class reset_password(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')
    
class set_new_password(View):
    def get(self, request):
        return render(request, 'authentication/set_new_password.html')
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')