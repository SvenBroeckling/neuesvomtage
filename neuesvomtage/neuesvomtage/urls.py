from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from base import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('base/', include('base.urls')),
    path('quiz/', include('quiz.urls')),

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.DEBUG_TOOLBAR:
        urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
