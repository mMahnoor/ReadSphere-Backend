from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from book.models import Book, Category, Author
from book.serializers import BookSerializer, CategorySerializer, AuthorSerializer
from book.paginations import DefaultPagination
from book.filters import BookFilter

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category', 'author').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'isbn']
    ordering_fields = ['title', 'author', 'updated_at']

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if book.availability_status:  
            return Response(
                {'message': "Available books cannot be deleted. Mark as unavailable first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(book)
        return Response(status=status.HTTP_204_NO_CONTENT)
