from django.conf import settings


def set_admin_header(request):
    COLOR_GREEN_DARK = '#089c2f'
    COLOR_RED_DARK = '#961313'

    if settings.DNV == 'dev':
        ENV_NAME = "DEVELOPMENT"
        adm_bg = COLOR_GREEN_DARK
    elif settings.DNV == 'prod':
        ENV_NAME = "PRRODUCTION"
        adm_bg = COLOR_RED_DARK
    else:
        ENV_NAME = "✋ acceptable DNV values are dev or prod"
        adm_bg = 'black'

    return {
        "ADMIN_HEADER_FG": '#ffffff',
        "ADMIN_HEADER_BG": adm_bg,
        "ENV_NAME": ENV_NAME,
        
        # "PROJ_NAME": getattr(settings, "PROJ_NAME", None),
        "PROJ_NAME": getattr(settings, "PROJ_NAME", '✋ need to set PROJ_NAME in settings'),
    }
