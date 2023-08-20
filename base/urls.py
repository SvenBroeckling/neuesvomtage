# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView

from base import views

app_name = "base"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "xhr_load_feed/<feed_id>/",
        views.XhrFeedOlderNewsView.as_view(),
        name="xhr_feed_older_news",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="base/contact.html"),
        name="contact",
    ),
]
