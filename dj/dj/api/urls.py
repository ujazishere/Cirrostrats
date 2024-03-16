from rest_framework.routers import DefaultRouter
from django.urls import path, include
from dj_app.api.urls import flighter_router

router = DefaultRouter()
router.registry.extend(flighter_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]
