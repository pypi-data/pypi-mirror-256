# from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path
from django.views.generic import TemplateView

from . import views
# this does not work from here:
# from django.conf.urls import handler404
# handler404 = views.error_404


# our admin/base_site.html override template also affects the title
admin.site.site_title = 'REAL Django Admin'   # DEFAULT: Django site admin
admin.site.site_header = 'Real Django Admin'  # DEFAULT: Django Administration
admin.site.index_title = 'Site Admin Home'    # DEFAULT: Site Administration


# this is supposed to be opinionated and NOT require defining more stuff in
# settings, particularly for just getting simple sites up an running quickly
ADMIN_URL = 'adm/'
LOGIN_URL = 'ac/li/'
LOGOUT_URL = 'ac/lo/'
# ADMIN_URL = settings.ADMIN_URL
# LOGIN_URL = settings.LOGIN_URL
# LOGOUT_URL = settings.LOGOUT_URL


urlpatterns = [
    path(ADMIN_URL, admin.site.urls),

    path("robots.txt", views.robots_txt, name="robots_txt"),

    path(LOGIN_URL, auth_views.LoginView.as_view(
        template_name='accounts/login.dtl'), name='login'),
    
    path(LOGOUT_URL, auth_views.LogoutView.as_view(
        template_name='accounts/logout.dtl'), name='logout'),

    # in lieu of defining LOGIN_REDIRECT_URL in settings
    path('accounts/profile/', lambda request: redirect('login', permanent=True)),

    # put this in another OPTIONAL package?
    # this is for when you do NOT care about having a home page
    path('', lambda request: redirect('home/', permanent=True)),
    path('home/', TemplateView.as_view(template_name='home.dtl'), name='home'),
]
