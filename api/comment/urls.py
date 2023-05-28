from django.urls import path
from api.comment.views import *

urlpatterns = [
    path('add_comment/', add_comment, name='add_comment'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('get_comments/', get_comments, name='get_comments'),
    path('edit_comment/', edit_comment, name='edit_comment'),
    path('add_reply/', add_reply, name='add_reply'),
    path('delete_reply/', delete_reply, name='delete_reply'),
    path('edit_reply/', edit_reply, name='edit_reply'),
    path('add_like/', add_like, name='add_like'),
    path('delete_like/', delete_like, name='delete_like')
]