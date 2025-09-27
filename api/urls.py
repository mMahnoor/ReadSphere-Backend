from rest_framework import routers
from django.urls import path, include
from book.views import BookViewSet, CategoryViewSet, AuthorViewSet
from borrow.views import BorrowViewSet
from reservation.views import ReservationViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='books')
router.register('borrows', BorrowViewSet, basename='borrows')
router.register('reservations', ReservationViewSet, basename='reservations')
urlpatterns = [
    path('', include(router.urls)),
]