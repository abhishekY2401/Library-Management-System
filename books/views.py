from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from books.models import Book, BookRecord
from users.models import User
from books.serializers import BookSerializer, BookRecordSerializer, BookUpdateSerializer
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from books.permissions import IsLibrarian
from datetime import datetime, timezone
from django.shortcuts import render
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
def get_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)

    except Book.DoesNotExist:
        return Response("No Books found in library", status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_book(request, id):
    try:
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book)

        return Response(serializer.data)

    except Book.DoesNotExist:
        return Response("Book not found in library", status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
@permission_classes([IsLibrarian])
def update_book(request, id):
    try:
        book = Book.objects.get(id=id)
        print("book:", book)

        # Get the fields from the request and update them if present
        if 'title' in request.data:
            book.title = request.data.get('title')
        if 'author' in request.data:
            book.author = request.data.get('author')
        if 'category' in request.data:
            book.category = request.data.get('category')
        if 'description' in request.data:
            book.description = request.data.get('description')
        if 'isbn' in request.data:
            book.isbn = request.data.get('isbn')
        if 'status' in request.data:
            book.status = request.data.get('status')

        # Save the updated book instance
        book.save()

        return Response("Book updated successfully", status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@permission_classes([IsLibrarian])
def remove_book(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
@permission_classes([IsLibrarian])
def view_all_members_records():
    try:
        records = BookRecord.objects.all()
        serializer = BookRecordSerializer(records, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Member related operations


@api_view(['POST'])
def borrow_book(request, id):
    # get the user id and book id for creating a book record of BORROWED status
    print(request)
    member_id = request.user
    book_id = id
    return_date = request.data.get('return_date')

    try:
        # now fetch the user and the book data by its corresponding id
        member = User.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)

        if member.role == User.Role.LIBRARIAN:
            return Response({"error": "Only members can borrow books"}, status=status.HTTP_400_BAD_REQUEST)

        if book.status == Book.Status.BORROWED:
            return Response({"error": "This book is currently not available."}, status=status.HTTP_400_BAD_REQUEST)

        # if available, then assign the book
        book_record = BookRecord.objects.create(
            book=book,
            member=member,
            action_type=BookRecord.Status.BORROWED,
            issue_date=datetime.now(timezone.utc),
            return_date=return_date
        )

        book.status = Book.Status.BORROWED
        book.save()

        return Response({"message": "Book borrowed successfully", "book_record": book_record}, status=status.HTTP_201_CREATED),

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def return_book(request, id):
    # get the user id and book id for creating a book record of BORROWED status
    member_id = request.user
    book_id = id

    try:
        # now fetch the user and the book data by its corresponding id
        member = User.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)

        if member.role == User.Role.LIBRARIAN:
            return Response({"error": "Only members can return books"}, status=status.HTTP_400_BAD_REQUEST)

        if book.status == Book.Status.AVAILABLE:
            return Response({"error": "This book is already returned."}, status=status.HTTP_400_BAD_REQUEST)

        # if borrowed, then return the book
        book_record = BookRecord.objects.create(
            book=book,
            member=member,
            action_type=BookRecord.Status.RETURNED,
            return_date=timezone.now()
        )

        book.status = Book.Status.AVAILABLE
        book.save()

        return Response({'message': 'Book returned successfully', 'book_record': BookRecordSerializer(book_record).data}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_past_records(request):

    # Get user_id from the request data
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:

        records = BookRecord.objects.filter(member=user_id)

        if not records.exists():
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookRecordSerializer(records, many=True)
        return Response(serializer.data)

    except Exception as error:
        return Response(f"Error while fetching all records: {str(error)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


### Template Views ###

# def add_book_in_library(request):
#     return render(request, 'add_book.html')
@permission_classes([IsLibrarian])
def librarian_home(request):
    try:
        books = Book.objects.all()
        book_serializer = BookSerializer(books, many=True)

        members = User.objects.filter(role=User.Role.MEMBER)
        member_serializer = UserSerializer(members, many=True)

        records = BookRecord.objects.all()
        record_serializer = BookRecordSerializer(records, many=True)

    except Book.DoesNotExist:
        return Response("No Books found in library", status=status.HTTP_404_NOT_FOUND)

    except User.DoesNotExist:
        return Response("No Members are added in library", status=status.HTTP_404_NOT_FOUND)

    except BookRecord.DoesNotExist:
        return Response("No Records found in library", status=status.HTTP_404_NOT_FOUND)

    return render(request, 'librarian.html', context={"books": book_serializer.data, "members": member_serializer.data, "records": record_serializer.data})


@permission_classes([IsAuthenticated])
def member_home(request):
    try:

        books = Book.objects.all()
        book_serializer = BookSerializer(books, many=True)

        # records = BookRecord.objects.filter(member=member_id)
        # record_serializer = BookRecordSerializer(records, many=True)

    except User.DoesNotExist:
        return Response("No User exists in the library", status=status.HTTP_404_NOT_FOUND)

    except BookRecord.DoesNotExist:
        return Response("Record not found in library", status=status.HTTP_404_NOT_FOUND)

    return render(request, 'member.html', context={
        'books': book_serializer.data,
        # "records": record_serializer.data
    })
