from django.urls import include, path

urlpatterns = [
    path('users/', include("bp_app.api.users.urls")),
]