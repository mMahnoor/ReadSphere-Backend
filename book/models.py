from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    published_year = models.DateField(blank=True, null=True, help_text="Enter a four digit number i.e 2002")
    available_copies = models.IntegerField(default=1)
    availability_status = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.first_name} on {self.book.title}"