from django.urls import path
from api.verdict.views import *

urlpatterns = [
    path('get_verdict_content/', get_verdict_content, name='get_verdict_content'),

]