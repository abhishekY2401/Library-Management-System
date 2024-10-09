from django.urls import path
from books.views import *

app_name = 'books'

urlpatterns = [
    ## template urls ##
    path('librarian-home/', librarian_home, name='librarian_home'),
    path('member-home/', member_home, name='member_home'),

    ## api urls ##
    path('api/books/add/', add_book, name='add_book'),
    path('api/books/', get_books, name="get_books"),
    path('api/books/<int:id>/', get_book, name='get_book'),
    path('api/books/<int:id>/update/', update_book, name='update_book'),
    path('api/books/<int:id>/remove/', remove_book, name='remove_book'),

    path('api/books/borrow', borrow_book, name='borrow_book'),
    path('api/books/return', return_book, name='return_book')
]
