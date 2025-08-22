from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Meal Rater API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.django-rest-framework.org/topics/documenting-your-api/",
        contact=openapi.Contact(email="demo@api.com"),
        license=openapi.License(name="license"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)