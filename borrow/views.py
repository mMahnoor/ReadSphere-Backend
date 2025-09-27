from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from borrow.models import BorrowRecord
from borrow.serializers import BorrowSerializer, ReturnBorrowSerializer
from book.models import Book
from django.utils import timezone

class BorrowViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = BorrowRecord.objects.all()
    serializer_class = BorrowSerializer
    def get_queryset(self):
        qs = BorrowRecord.objects.filter(member=self.request.user)
        qs = qs.filter(status="borrowed")
        return qs
    
    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow_book(self, request):
        book_id = request.data.get("book")
        print("book_id is: ", request.data)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if not book.availability_status:
            return Response({"error": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST)

        # Create borrow record
        borrow = BorrowRecord.objects.create(book=book, member=request.user)
        book.available_copies = book.available_copies-1
        if book.available_copies == 0:
            book.availability_status = False
        book.save()
        serializer = BorrowSerializer(instance=borrow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='return', serializer_class=ReturnBorrowSerializer)
    def return_book(self, request, pk=None):
        try:
            borrow = BorrowRecord.objects.get(id=pk, member=request.user, status="borrowed")
        except BorrowRecord.DoesNotExist:
            return Response({"error": "Borrow record not found or already returned"}, status=status.HTTP_404_NOT_FOUND)

        borrow.status = "returned"
        borrow.return_date = timezone.now()
        borrow.save()
        
        borrow.book.availability_status = True
        borrow.book.available_copies = borrow.book.available_copies+1
        borrow.book.save()

        serializer = self.get_serializer(borrow)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        records = BorrowRecord.objects.filter(member=request.user).order_by('-borrow_date')
        serializer = BorrowSerializer(records, many=True)
        return Response(serializer.data)

   
