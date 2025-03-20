from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    FICTION = 'Fiction'
    NONFICTION = 'NonFiction'
    SCIENCE = 'Science'
    HISTORY = 'History'
    BIOGRAPHY = 'Biography'

    CATEGORY_CHOICES = [
        (FICTION, 'Fiction'),
        (NONFICTION, 'NonFiction'),
        (SCIENCE, 'Science'),
        (HISTORY, 'History'),
        (HISTORY, 'Biography')
    ]

    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=15, unique=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(auto_now_add=True)
    current_book = models.ManyToManyField(Book, related_name='borrow', blank=True)

    def __str__(self):
        return self.name.get_full_name()
    

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.member} - {self.book}"
    