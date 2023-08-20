# -*- coding: utf-8 -*-
from django.urls import path

from quiz import views

app_name = "quiz"

urlpatterns = [
    path(r"", views.IndexView.as_view(), name="index"),
]
