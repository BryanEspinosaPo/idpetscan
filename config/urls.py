"""
URLs principales del proyecto. Cada app tiene su propio urls.py,
aquí solo los conectamos con un prefijo.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Landing page pública (home)
    path("", TemplateView.as_view(template_name="home.html"), name="home"),

    # Cada app maneja sus propias rutas
    path("cuenta/", include("accounts.urls")),
    path("", include("pets.urls")),      # incluye /mis-mascotas/ y /p/<codigo>/
    path("ordenes/", include("orders.urls")),
]

# Solo en desarrollo: sirve las imágenes subidas (fotos, QR) directamente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
