from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

urlpatterns = [
    # Original path for BookList view
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include all router-generated URLs
    path('', include(router.urls)),
]