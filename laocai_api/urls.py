from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'roads', views.RoadViewSet, basename='roads')
router.register(r'assets', views.AssetViewSet, basename='assets')
router.register(r'projects', views.ProjectViewSet, basename='projects')
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include(router.urls)),
        path('auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
        path('import/roads', views.ImportRoadsView.as_view(), name='import_roads'),
        path('reports/summary', views.SummaryView.as_view(), name='reports_summary'),
        path('health', views.health),
    ])),
]
