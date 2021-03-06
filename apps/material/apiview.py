#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:13
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters

from .models import MaterialCategory, MaterialTag, MaterialBanner, PostBaseInfo, MaterialCommentInfo
from .serializers import CategorySerializer, SingleLevelCategorySerializer, TagSerializer, MaterialBannerSerializer, \
    MaterialPostBaseInfoSerializer, CommentDetailInfoSerializer, CreateCommentSerializer
from .filters import CategoryFilter, MaterialBannerFilter, PostBaseInfoFilter, CommentFilter
from base.utils import CustomeLimitOffsetPagination, CustomePageNumberPagination


class CategoryListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        分类列表页
    """
    queryset = MaterialCategory.objects.all()
    # 分页设置
    pagination_class = CustomePageNumberPagination
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'category_type', 'desc')
    ordering_fields = ('category_level', 'is_tab')
    ordering = ('id',)


class SingleLevelCategoryListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        单级分类列表页
    """
    queryset = MaterialCategory.objects.all()
    # 分页设置
    pagination_class = CustomePageNumberPagination
    serializer_class = SingleLevelCategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'category_type', 'desc')
    ordering_fields = ('category_level', 'is_tab')
    ordering = ('id',)


class TagListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        标签列表页
    """
    queryset = MaterialTag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name', 'subname')
    ordering_fields = ('name', 'subname')


class MaterialBannerListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        Banner列表页
    """
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = MaterialBannerFilter
    queryset = MaterialBanner.objects.all().order_by("-index")
    serializer_class = MaterialBannerSerializer


class PostBaseInfoListViewset(viewsets.ReadOnlyModelViewSet):
    """
    List:
        时间轴列表页
    """
    queryset = PostBaseInfo.objects.all()
    # 分页设置
    pagination_class = CustomeLimitOffsetPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PostBaseInfoFilter
    search_fields = ('title', 'subtitle', 'abstract', 'desc')
    ordering_fields = ('id', 'click_num', 'like_num', 'comment_num', 'add_time')
    serializer_class = MaterialPostBaseInfoSerializer


class CommentDetailListViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    List:
        评论列表页
    """
    queryset = MaterialCommentInfo.objects.all()
    # 分页设置
    pagination_class = CustomeLimitOffsetPagination
    
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CommentFilter
    ordering_fields = ('add_time',)
    ordering = ('-add_time',)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentDetailInfoSerializer
        elif self.action == "create":
            return CreateCommentSerializer
        return CommentDetailInfoSerializer


