from django.urls import path
from api.verdict.views import *

urlpatterns = [
    path('get_verdict_content/', get_verdict_content, name='get_verdict_content'),
    path('get_verdict_contents/', get_verdict_contents, name='get_verdict_contents'),
    path('like_verdict/', like_verdict, name='like_verdict'),
    path('unlike_verdict/', unlike_verdict, name='unlike_verdict'),
]