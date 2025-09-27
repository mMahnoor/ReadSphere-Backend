from rest_framework import serializers
from .models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


# class BookSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=Author.objects.all()
#     )
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     # author_detail = AuthorSerializer(source="author", read_only=True)
#     # category_detail = CategorySerializer(source="category", read_only=True)

#     class Meta:
#         model = Book
#         fields = [
#             'id',
#             'title',
#             'isbn',
#             'availability_status',
#             'available_copies',
#             'author',
#             'category'
#         ]
#     def to_representation(self, instance):
#         """
#         On GET request, show nested serializers.
#         """
#         representation = super().to_representation(instance)
#         representation['author'] = AuthorSerializer(instance.author).data
#         representation['category'] = CategorySerializer(instance.category).data
#         return representation

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

