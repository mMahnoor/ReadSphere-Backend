from rest_framework import serializers
from .models import Book, Author, Category, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    author_detail = AuthorSerializer(source="author", read_only=True)
    category_detail = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "availability_status",
            "available_copies",
            "author", 
            "author_detail",     
            "category",    
            "category_detail", 
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    book = serializers.SerializerMethodField(method_name='get_book')

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'ratings', 'comment', 'created_at']
        read_only_fields = ['user', 'book', 'created_at']

    def get_user(self, obj):
        return MemberSerializer(obj.user).data
    
    def get_book(self, obj):
        return BookSerializer(obj.book).data

    def create(self, validated_data):
        book_id = self.context['book_id']
        # print("book-review: ", book_id)
        return Review.objects.create(book_id=book_id, **validated_data)