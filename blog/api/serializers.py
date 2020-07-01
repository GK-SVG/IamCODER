from rest_framework.serializers import ModelSerializer
from blog.models import Blogpost

class PostSerializer(ModelSerializer):
    class Meta:
        model=Blogpost
        fields=[
            'post_id',
            'writter',
            'title',
            'contant',
        ]