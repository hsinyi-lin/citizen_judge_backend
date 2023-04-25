from django.urls import path
from api.auth.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('send_code/', send_code, name='send_code'),
]