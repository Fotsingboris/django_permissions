"""
URL configuration for django_permissions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns, set_language
from django.views import defaults as default_views
from django.conf import settings


urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('', include('core.urls')),
    path('i18n/setlang/', set_language, name='set_language'),
    
)

if not settings.DEBUG:
    handler404 = 'core.error_view.handler404'
    handler500 = 'core.error_view.handler500'
    handler403 = 'core.error_view.handler403'

# Error views for debugging in development
if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    