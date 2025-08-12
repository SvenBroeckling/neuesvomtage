import random

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from base.models import Entry, Feed


class IndexView(TemplateView):
    template_name = "quiz/index.html"

    def get_context_data(self, **kwargs):
        feeds = Feed.objects.filter(include_in_quiz=True)
        headline = Entry.objects.filter(feed__in=feeds).order_by("?")[0]
        answers = [headline.feed] + list(
            feeds.exclude(id=headline.feed.id).order_by("?")[:3]
        )
        random.shuffle(answers)

        context = super().get_context_data(**kwargs)
        context["headline"] = headline
        context["answers"] = answers
        return context

    def post(self, request, *args, **kwargs):
        answer = Feed.objects.get(id=request.POST.get("answer"))
        headline = Entry.objects.get(id=request.POST.get("headline"))

        if headline.feed.id == answer.id:
            messages.success(
                request,
                'Korrekt: <a href="%s">%s</a> ist %s'
                % (headline.url, headline.title, answer.title),
            )

            if request.session.get("streak", None) is not None:
                request.session["streak"] += 1
            else:
                request.session["streak"] = 1

        else:
            messages.error(
                request,
                'Falsch: <a href="%s">%s</a> ist %s'
                % (headline.url, headline.title, headline.feed.title),
            )
            if request.session.get("streak", None) is not None:
                del request.session["streak"]

        return HttpResponseRedirect(reverse("quiz:index"))
