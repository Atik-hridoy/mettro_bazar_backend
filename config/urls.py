from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.orders.urls')),
    path('api/', include('apps.payments.urls')),
    path('api/', include('apps.delivery.urls')),
    path('api/', include('apps.reviews.urls')),

    # OpenAPI Documentation Schema & Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
