from django.urls import path, include
from rest_framework import routers
from api_Product import views

router=routers.DefaultRouter()
router.register(r'routes', views.ProductViewSet)

urlpatterns = [
    path('',include(router.urls)),
]