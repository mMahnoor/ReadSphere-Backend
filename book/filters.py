from book.models import Book
from django_filters.rest_framework import FilterSet

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'category__name': ['exact', 'icontains'],
            'author__name': ['exact', 'icontains'],
            'availability_status': ['exact'],
            'isbn': ['exact', 'icontains'],
            'title': ['icontains'],
        }