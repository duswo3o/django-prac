from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        # 쓰기 요청을 할 때 articles는 읽기 전용이라고 명시
        read_only_fields = ("articles",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("articles")
        return ret


class ArticleSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    # comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
