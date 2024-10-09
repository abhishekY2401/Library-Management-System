from django.db import models
from users.models import User
from datetime import timezone

# Create your models here.


class Book(models.Model):
    '''
    This Book Model describes a brief information about books
    '''

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'available'
        BORROWED = 'BORROWED', 'borrowed'

    title = models.CharField(max_length=128, null=False)
    author = models.CharField(max_length=100, null=False)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.AVAILABLE)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Book title={self.title} category={self.category}"


class BookRecord(models.Model):
    '''
    This Model keeps a record of books status
    '''
    class Status(models.TextChoices):
        BORROWED = 'BORROWED', 'borrowed'
        RETURNED = 'RETURNED', 'returned'

    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    member = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.BORROWED)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def mark_as_returned(self):
        self.status = self.Status.RETURNED
        self.returned_at = timezone.now()
        self.save()

    def __str__(self):
        return f"BookRecord: {self.book.title} - {self.member.email} - {self.status}"
