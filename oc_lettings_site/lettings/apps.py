from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LettingsConfig(AppConfig):
    name = 'oc_lettings_site.lettings'
    verbose_name = _("Lettings")
