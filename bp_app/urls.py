from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('api/', include("bp_app.api.urls")),
]
