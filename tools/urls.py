from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from .views import HomeView, OpenAIView
router = routers.DefaultRouter()

router.register(r'', HomeView, 'heartbeat')
router.register(r'ai', OpenAIView, 'ai')

urlpatterns = [
    path("", include(router.urls)),
]