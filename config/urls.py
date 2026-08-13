from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from pets.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("politica-de-datos/", TemplateView.as_view(
        template_name="legal/politica_datos.html",
        extra_context={"admin_email": settings.ADMIN_NOTIFICATION_EMAIL},
    ), name="politica_datos"),
    path("cuenta/", include("accounts.urls")),
    path("", include("pets.urls")),
    path("ordenes/", include("orders.urls")),
    path("panel/", include("backoffice.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

