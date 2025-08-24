# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.following.filter(pk=target.pk).exists():
            return Response(
                {"detail": f"You are already following {target.username}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(target)
        return Response(
            {"detail": f"You are now following {target.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not request.user.following.filter(pk=target.pk).exists():
            return Response(
                {"detail": f"You are not following {target.username}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(target)
        return Response(
            {"detail": f"You unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )
