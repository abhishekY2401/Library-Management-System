from rest_framework import serializers
from books.models import Book, BookRecord


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category',
                  'description', 'isbn', 'status']


class BookRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecord
        fields = ['book', 'member', 'action_type', 'issue_date', 'return_date']
