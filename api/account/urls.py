from django.urls import path
from api.account.views import *

urlpatterns = [
    path('picture_list/', picture_list, name='picture_list'),
]