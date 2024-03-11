from .views import RegistrationView, LoginView, reset_password, set_new_password, UsernameValidationView, EmailValidationView, VerificationView, LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', reset_password.as_view(), name='reset-password'),
    path('set-new-password/', set_new_password.as_view(), name='set-new-password'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uid>/<token>', VerificationView.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]