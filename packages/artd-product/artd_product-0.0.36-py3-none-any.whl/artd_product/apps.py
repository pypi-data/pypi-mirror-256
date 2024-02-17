from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArtdProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("ArtD Product")
    name = "artd_product"
