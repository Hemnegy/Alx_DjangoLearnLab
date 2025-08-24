from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):  # <-- "viewsets.ModelViewSet"
    queryset = Post.objects.all().order_by("-created_at")  # <-- "Post.objects.all()"
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):  # <-- "viewsets.ModelViewSet"
    queryset = Comment.objects.all().order_by("-created_at")  # <-- "Comment.objects.all()"
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.GenericAPIView):
    """
    Returns posts from users that the authenticated user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all the users the current user is following
        following_users = request.user.following.all()  # <-- "following.all()"

        # Get posts authored by those users
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")  
        # <-- "Post.objects.filter(author__in=following_users).order_by"

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
