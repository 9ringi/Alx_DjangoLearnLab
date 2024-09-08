"""
To authenticate requests, users must obtain a token from /api-token-auth/.
Include the token in the Authorization header as "Token <your_token_here>".
Permissions:
- Only authenticated users can access the API.
- Only authors can modify their own books.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthorOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly] 
