# -*- coding: utf-8 -*-
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from api import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'feeds', views.FeedViewSet)
router.register(r'entries', views.EntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('doc/', TemplateView.as_view(
        template_name='api/swagger-ui.html'
    ), name='swagger-ui'),
    path('openapi-schema', get_schema_view(
        title="Neuesvomtage API",
        description="API for all the news",
        version="1.0.0"
    ), name='openapi-schema'),

]
