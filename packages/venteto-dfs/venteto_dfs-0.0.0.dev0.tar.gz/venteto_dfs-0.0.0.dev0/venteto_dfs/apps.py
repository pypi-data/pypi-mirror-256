from django.apps import AppConfig
# from django.contrib.auth.apps import AuthConfig


class VentetoSimpleDjangoFoundationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = "venteto_simple_django_foundation"
    name = "venteto_dfs"
    # verbose_name = "(PAB) Users"
    # verbose_name = "Auth Users (Custom)"

"""
class ContribAuthRenamed(AuthConfig):
    verbose_name = "(PAC) Authentication and Authorization (Contrib)"
"""
