from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

User = get_user_model()


class FollowUserView(generics.GenericAPIView):
    """
    Allows an authenticated user to follow another user.
    """
    queryset = User.objects.all()  # <-- CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # <-- permissions.IsAuthenticated

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(target)  # via related_name on followers
        return Response(
            {"detail": f"You are now following {target.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows an authenticated user to unfollow another user.
    """
    queryset = User.objects.all()  # <-- CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # <-- permissions.IsAuthenticated

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(target)
        return Response(
            {"detail": f"You unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )
