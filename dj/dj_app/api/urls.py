from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..views import FlightViewSet


flighter_router = DefaultRouter()
flighter_router.register(r'flights', FlightViewSet)
