from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsLibrarian
# Create your views here.


@api_view(["POST"])
@permission_classes([IsLibrarian])
def add_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsLibrarian])
def get_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

    except Book.DoesNotExist:
        return Response("No Books found in library", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)

        return Response(serializer.data)

    except Book.DoesNotExist:
        return Response("Book not found in library", status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
@permission_classes([IsLibrarian])
def update_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsLibrarian])
def remove_book(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
