#!/usr/bin/env python
from datetime import datetime

import feedparser
from django.db import models, DataError
from django.db.models import Count
from django.utils.translation import gettext as _


class Category(models.Model):
    name = models.CharField(max_length=40)
    sort = models.IntegerField(default=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-sort",)


class FeedQuerySet(models.QuerySet):
    def feeds_with_entries(self):
        return self.annotate(num_entries=Count("entry")).filter(num_entries__gte=1)


class Feed(models.Model):
    objects = FeedQuerySet.as_manager()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(null=True, blank=True)
    last_update_status = models.IntegerField(blank=True, null=True)

    title = models.CharField(max_length=30, db_index=True)
    url = models.URLField(max_length=250, db_index=True)
    site_url = models.URLField(max_length=250, blank=True, null=True)
    favicon = models.ImageField(upload_to="favicons", blank=True, null=True)

    supports_lsr = models.BooleanField(default=False)
    has_adblock_block = models.BooleanField(default=False)
    has_paywall = models.BooleanField(default=False)

    sort = models.IntegerField(default=1000)
    include_in_quiz = models.BooleanField(default=False)

    class Meta:
        ordering = ("-sort",)

    def __str__(self):
        return self.title

    def update(self):
        self.entry_set.update(is_new=False)
        try:
            d = feedparser.parse(self.url)
            print(d.status, self.url)
            # if d.href != self.url and d.status in [301, 308]:  # autocorrect permanent redirects
            #     self.url = d.href
        except:
            self.last_update_status = 0
            self.save()
            print("skipped: ", self)
            return
        else:
            self.last_update_at = datetime.now()
            self.last_update_status = d.status
            self.save()

        for e in d.entries:
            try:
                lnk = e.link
            except AttributeError:
                try:
                    lnk = e.links[0].href
                except AttributeError:
                    lnk = ""

            try:
                ca = datetime(*e.updated_parsed[:-2])
            except (AttributeError, TypeError):
                ca = datetime.now()

            count = self.entry_set.filter(title=e.title, url=lnk).count()

            if not count:
                try:
                    self.entry_set.create(
                        title=e.title, is_new=True, created_at=ca, url=lnk
                    )
                except DataError:
                    pass


class Entry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    fetched_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=400)
    created_at = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=250)
    abstract = models.TextField(blank=True, null=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = _("entries")

    def __str__(self):
        return self.title


class TopWordQuerySet(models.QuerySet):
    def top_10(self):
        return self.order_by("-count")[:10]

    def rest(self):
        return self.order_by("-count")[10:30]


class TopWordLemma(models.Model):
    lemma = models.CharField(max_length=400)

    def __str__(self):
        return self.lemma

    def words_string(self):
        return ", ".join([w.word for w in self.topwordlemmaword_set.all()])


class TopWordLemmaWord(models.Model):
    lemma = models.ForeignKey(TopWordLemma, on_delete=models.CASCADE)
    word = models.CharField(max_length=400)

    def __str__(self):
        return self.word


class TopWord(models.Model):
    objects = TopWordQuerySet.as_manager()

    word = models.CharField(max_length=400)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ("-count",)

    def __str__(self):
        return f"{self.word} ({self.count})"
