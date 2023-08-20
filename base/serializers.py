from base.models import Feed, Entry, Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['feed', 'fetched_at', 'title', 'url', 'is_new']


class FeedSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = ['category', 'last_update_at', 'title', 'url', 'site_url',
                  'favicon', 'entries']

    def get_entries(self, obj):
        serializer = EntrySerializer(
            Entry.objects.filter(feed=obj).order_by('-created_at')[:7],
            many=True)
        return serializer.data
