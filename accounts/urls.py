from django.urls import path
from .views import (
    signup,
    user_login,
    user_logout,
    phone_login,
    verify_otp,
    forgot_password,
    verify_reset_otp,
    reset_password,
)

urlpatterns = [

    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('phone-login/', phone_login, name='phone_login'),
    path('verify-otp/', verify_otp, name='verify_otp'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-reset-otp/', verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', reset_password, name='reset_password'),
    

]