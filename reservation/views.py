from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from reservation.models import Reservation
from reservation.serializers import ReservationSerializer, FulfillCancelSerializer
from borrow.models import BorrowRecord

def updatePriorityQueue(self, reservation):
    self.reservation = reservation
    active_reservations = Reservation.objects.filter(book=reservation.book).order_by("reservation_date")
    for i, res in enumerate(active_reservations, start=1):
        res.priority = i
        res.save()

class ReservationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        # Reservations of the logged-in user
        return Reservation.objects.filter(member=self.request.user).order_by("-reservation_date")

    @action(detail=False, methods=["post"], url_path="make")
    def make_reservation(self, request):
        book_id = request.data.get("book_id")
        print(request.data)
        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Checking existing reservation for the same book
        existing = Reservation.objects.filter(member=request.user, book_id=book_id).first()
        if existing:
            return Response(
                {"error": "You already have an active reservation for this book."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="fulfill", serializer_class=FulfillCancelSerializer)
    def fulfill_reservation(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(id=pk)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found or already handled"}, status=status.HTTP_404_NOT_FOUND)

        # First in priority can borrow
        if reservation.priority != 1:
            return Response({"error": "Not first in queue"}, status=status.HTTP_400_BAD_REQUEST)

        if reservation.book.available_copies>0:
            reservation.book.available_copies = reservation.book.available_copies-1
            borrow = BorrowRecord.objects.create(book=reservation.book, member=reservation.member)
            reservation.delete()
            updatePriorityQueue(reservation)
        else:
            return Response(
                {
                    "error": "Book is currently not available for borrowing.",
                    "message": "Try again when the book is available."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if reservation.book.available_copies==0:
            reservation.book.availability_status = False
        reservation.book.save()

        return Response({"message": "Reservation fulfilled, borrow created", "borrow_id": borrow.id}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"], url_path="cancel", serializer_class=FulfillCancelSerializer)
    def cancel_reservation(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(id=pk, member=request.user)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

        reservation.delete()

        # Updating priorities after cancellation
        updatePriorityQueue(reservation)

        return Response({"message": "Reservation cancelled"}, status=status.HTTP_200_OK)
