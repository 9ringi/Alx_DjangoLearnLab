from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, like
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

User = get_user_model()
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
 # views.py in posts app

@login_required
def feed(request):
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})
class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        request.user.following.add(user_to_follow)
        return Response({'status': 'followed'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK) 
    
def like_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target=post,
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id
            )
            return JsonResponse({"message": "Post liked"}, status=201)
        return JsonResponse({"message": "Post already liked"}, status=200)
    return JsonResponse({"message": "Unauthorized"}, status=403)

def unlike_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return JsonResponse({"message": "Post unliked"}, status=200)
        return JsonResponse({"message": "You haven't liked this post"}, status=400)
    return JsonResponse({"message": "Unauthorized"}, status=403)