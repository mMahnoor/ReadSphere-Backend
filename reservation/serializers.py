from rest_framework import serializers
from reservation.models import Reservation
from book.models import Book
from book.serializers import BookSerializer 
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ReservationSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "member",
            "book",
            "book_id", 
            "reservation_date",
            "priority",
        ]
        read_only_fields = ["reservation_date", "priority"]

class FulfillCancelSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "member",
            "book",
            "book_id", 
            "reservation_date",
            "priority",
        ]
        read_only_fields = fields

