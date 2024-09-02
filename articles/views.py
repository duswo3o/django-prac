from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from .models import Article, Comment
from .serializers import (
    ArticleSerializer,
    CommentSerializer,
    ArticleDetailSerializer)

from rest_framework.views import APIView


# Create your views here.
# @api_view(["GET", "POST"])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         # json_data = serializer.data
#         return Response(serializer.data)
#
#     else:
#         # data = request.data
#         # print(data)
#         # title = data.get("title")
#         # content = data.get("content")
#         # article = Article.objects.create(title=title, content=content)
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True): # raise_exception옵션으로 false인 경우의 return을 대신함
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=400)


class ArticleListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Articles"],
        description="Article 목록 조회를 위한 API"
    )
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # json_data = serializer.data
        return Response(serializer.data)

    @extend_schema(
        tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer
    )
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # raise_exception옵션으로 false인 경우의 return을 대신함
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "DELETE", "PUT"])
# def article_detail(request, pk):
#     if request.method == "GET":
#         # pk에 해당하는 article 조회
#         # article = Article.objects.get(pk=pk)
#         article = get_object_or_404(Article, pk=pk)
#         # serialization
#         serializer = ArticleSerializer(article)
#         # return
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#
#     else:
#         article = get_object_or_404(Article, pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleDetailAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        # serialization
        serializer = ArticleDetailSerializer(article)
        # return
        return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class CommentListAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, article_pk):
        # comments = Comment.objects.all(article_pk=article_pk)
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self,request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    def get_object(self, request, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def check_sql(request):
    from django.db import connection

    # comments = Comment.objects.all().select_related("articles")
    # for comment in comments:
    #     print(comment.articles.title)

    articles = Article.objects.all().prefetch_related("comments")
    for article in articles:
        comments = article.comments.all()
        for comment in comments:
            print(comment.content)

    print("-"*30)
    print(connection.queries)

    return Response()
