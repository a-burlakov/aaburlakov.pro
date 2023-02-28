from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from aaburlakov_pro import settings
from personal_site.views import *


urlpatterns = [
    path("", include("personal_site.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
