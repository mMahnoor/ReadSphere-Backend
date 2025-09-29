from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated

from book.models import Book, Category, Author, Review
from book.serializers import BookSerializer, CategorySerializer, AuthorSerializer, ReviewSerializer
from book.paginations import DefaultPagination
from book.filters import BookFilter
from api.permissions import IsAdminOrReadOnly, IsReviewAuthorOrReadOnly, IsLibrarian, IsAdmin

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  
        return [IsLibrarian() | IsAdmin()]

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  
        return [IsLibrarian() | IsAdmin()]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category', 'author').all()
    serializer_class = BookSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  
        return [IsLibrarian() | IsAdmin()]
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
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsReviewAuthorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs.get('book_pk'))

    def get_serializer_context(self):
        return {'book_id': self.kwargs.get('book_pk')}
