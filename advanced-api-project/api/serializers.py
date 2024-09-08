# AuthorSerializer uses a nested BookSerializer to serialize related books dynamically.
# This makes it easier to handle the relationship between authors and their books.

from django.utils import timezone
from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    # Custom validation to ensure the publication year is not in the future
    def validate_publication_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested BookSerializer

    class Meta:
        model = Author
        fields = ['name', 'books']