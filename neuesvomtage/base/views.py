#!/usr/bin/env python
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView

from base.models import Feed, TopWord


class IndexView(TemplateView):
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        feeds = Feed.objects.all()

        q = self.request.GET.get("q", None)
        if q is not None:
            feeds = feeds.filter(entry__title__icontains=q)

        feeds = feeds.feeds_with_entries().order_by("-category__sort", "-sort")

        context = super().get_context_data(**kwargs)
        context.update(
            {
                "q": q,
                "feed_list": feeds,
                "top_words": TopWord.objects.all(),
            }
        )
        return context


class XhrFeedOlderNewsView(TemplateView):
    template_name = "base/xhr_feed_older_news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed"] = Feed.objects.get(id=kwargs["feed_id"])
        context["q"] = self.request.GET.get("q", None)
        return context
