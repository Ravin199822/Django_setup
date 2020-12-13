"""setup_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
   openapi.Info(
      title="AR Chat API",
      default_version='v1',
      description="Find APIs to Set Up",
      contact=openapi.Contact(email="contact@archat.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)
docs_urls = [
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

admin.site.site_header = "Set Up"
admin.site.site_title = "Set Up Admin Portal"
admin.site.index_title = "Welcome to Set Up Admin Portal"

app_urls = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('user.urls.v1')),
]


urlpatterns = app_urls

if settings.SYS_ENV != 'PROD':
    urlpatterns = docs_urls + app_urls