from django.urls import path
from api.comment.views import *

urlpatterns = [
    path('add_comment/', add_comment, name='add_comment'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('get_comments/', get_comments, name='get_comments'),
    path('edit_comment/', edit_comment, name='edit_comment'),
]