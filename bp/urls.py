from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("bp_app.urls")),
    path("healthy-check/", views.HealthyCheck.as_view(), name="healthyCheck")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)