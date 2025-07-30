from django.shortcuts import render

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

# Keep your existing BookList view if you want both options
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Add the new ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer