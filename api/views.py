from rest_framework import viewsets, permissions

from base.models import Feed, Category, Entry
from base.serializers import FeedSerializer, CategorySerializer, EntrySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class EntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
