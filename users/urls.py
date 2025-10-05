from rest_framework.routers import DefaultRouter
from users.views import PaymentViewSet, RegisterView, UserViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls + [
    path('register/', RegisterView.as_view(), name='register'),
]
