from django.urls import path
from api.verdict.views import *

urlpatterns = [
    path('get_verdict/', get_verdict, name='get_verdict'),
    path('get_verdicts/', get_verdicts, name='get_verdicts'),
    path('filter_verdicts/', filter_verdicts, name='filter_verdicts'),
    path('get_crime_verdicts/', get_crime_verdicts, name='get_crime_verdicts'),
    path('like_verdict/', like_verdict, name='like_verdict'),
    path('unlike_verdict/', unlike_verdict, name='unlike_verdict'),
    path('collect_verdict/', collect_verdict, name='collect_verdict'),
]