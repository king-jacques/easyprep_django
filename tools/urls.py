from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from .views import HomeView, OpenAIView, homepage_view, APIV1View
from django.views.generic import TemplateView


router = routers.DefaultRouter()

router.register(r'', HomeView, 'heartbeat')
router.register(r'ai', OpenAIView, 'ai')
router.register(r'api/v1', APIV1View, 'api-v1')

urlpatterns = [
    # path('', homepage_view, name='home'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path("", include(router.urls)),
]