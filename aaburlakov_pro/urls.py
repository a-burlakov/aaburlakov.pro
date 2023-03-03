from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.views.static import serve

from aaburlakov_pro import settings

urlpatterns = [
    path("", include("apps.personal_site.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [
        url(
            f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
        url(
            f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
            serve,
            {"document_root": settings.STATIC_ROOT},
        ),
    ]
