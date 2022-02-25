from rest_framework import serializers
from .models import User, Post


# rest_framework, 그리고 serializer 잘 설치됐나 확인하기 위해서 임시로 작성함. 추후 사용할 것임!
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'sign_up_date']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'writer_id', 'date', 'title', 'content']
