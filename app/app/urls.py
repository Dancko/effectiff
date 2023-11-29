from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tasks.urls")),
    path("users/", include("users.urls")),
    path("projects/", include("projects.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("verification/", include("verify_email.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("account/", include("allauth.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
