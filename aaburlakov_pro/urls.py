from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as mediaserve

from aaburlakov_pro import settings

urlpatterns = [
    path('', include('apps.personal_site.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += [
        re_path(
            f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
            mediaserve,
            {'document_root': settings.MEDIA_ROOT},
        ),
        re_path(
            f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
            mediaserve,
            {'document_root': settings.STATIC_ROOT},
        ),
    ]
