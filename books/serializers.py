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


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category',
                  'description', 'isbn', 'status']
        extra_kwargs = {
            'title': {'required': False},
            'author': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'isbn': {'required': False},
            'status': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update the instance fields with the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.status = validated_data.get('status', instance.status)

        # Save the updated instance
        instance.save()

        return instance
