from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.swagger import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
]
