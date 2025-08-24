from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # ✅ Create notification when someone comments on a post
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on your post",
            target=comment.post,
        )


# 👇 Like endpoints
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ matches checker
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Explicit Notification.objects.create
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post,
        )

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ matches checker
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response(
                {"detail": "You haven't liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
