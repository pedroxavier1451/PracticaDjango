from django.contrib import admin
from django.urls import path
from django.urls import include, re_path
from appCreditoBanco.View import views
from appEnfermedadesCardiacas.View import views2

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API para predicción de crédito en una institución financiera",
      default_version='v1',
      description="Es el API para predicción de crédito en una institución financiera",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="remigiohurtado@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    re_path(r'^nuevasolicitud/$',views.Clasificacion.determinarAprobacion, name='nuevasolicitud'),
    re_path(r'^predecir/',views.Clasificacion.predecir),
    re_path(r'^predecirIOJson/',views.Clasificacion.predecirIOJson),
    re_path(r'^nuevopaciente/$',views2.determinarEnfermedad, name='nuevopaciente'),
    re_path(r'^predecir2/',views2.predecir2, name='predecir2'),
    re_path(r'^predecirNB/',views2.predecirNB, name='predecirNB'),
]
