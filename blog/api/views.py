from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    )
from .serializers import PostSerializer
from blog.models import Blogpost
class PostCreate(ListCreateAPIView):
    queryset=Blogpost.objects.all()
    serializer_class=PostSerializer

class PostDeleteAPIView(DestroyAPIView):
    queryset=Blogpost.objects.all()
    serializer_class=PostSerializer
    lookup_field='post_id'

class PostListAPIView(ListAPIView):
    queryset=Blogpost.objects.all()
    serializer_class=PostSerializer

class PostUpdateAPIView(UpdateAPIView):
    queryset=Blogpost.objects.all()
    serializer_class=PostSerializer
    lookup_field='post_id'