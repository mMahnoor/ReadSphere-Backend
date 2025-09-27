from rest_framework import serializers
from book.models import Book
from users.models import CustomUser
from borrow.models import BorrowRecord
from book.serializers import BookSerializer

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'email']


class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all()
    )
    book_detail = BookSerializer(source="book", read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "book",   
            "book_detail",    
            "member",
            "borrow_date",
            "return_date",
            "status",
        ]
        read_only_fields = ["borrow_date", "return_date", "status", "member"]

class ReturnBorrowSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ["id", "book", "member", "borrow_date", "return_date", "status"]
        read_only_fields = fields