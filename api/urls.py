from rest_framework_nested import routers
from django.urls import path, include
from book.views import BookViewSet, CategoryViewSet, AuthorViewSet, ReviewViewSet
from borrow.views import BorrowViewSet
from reservation.views import ReservationViewSet
from users.views import GroupViewSet, UserGroupViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='books')
router.register('borrows', BorrowViewSet, basename='borrows')
router.register('reservations', ReservationViewSet, basename='reservations')

# Nested routes
book_router = routers.NestedDefaultRouter(
    router, 'books', lookup='book')
book_router.register('reviews', ReviewViewSet, basename='book-review')

# Groups router
user_router = routers.DefaultRouter()
user_router.register('user-groups', UserGroupViewSet, basename='user-groups')
user_router.register('groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(book_router.urls)),
    path('', include(user_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]