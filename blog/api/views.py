from rest_framework.generics import ListAPIView
from .serializers import PostSerializer
from blog.models import Blogpost
class PostListAPIView(ListAPIView):
    queryset=Blogpost.objects.all()
    serializer_class=PostSerializer