from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("lettings/", include("oc_lettings_site.lettings.urls", namespace="lettings")),
    path("profiles/", include("oc_lettings_site.profiles.urls", namespace="profiles")),
    path("admin/", admin.site.urls),
    path('sentry-debug/', trigger_error),
]
