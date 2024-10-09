from django.urls import path
from books.views import add_book, get_books, get_book, update_book, remove_book

urlpatterns = [
    path('add/', add_book, name='add_book'),
    path('', get_books, name="get_books"),
    path('<int:id>/', get_book, name='add_book'),
    path('<int:id>/update', update_book, name='add_book'),
    path('<int:id>/remove', remove_book, name='add_book')
]
