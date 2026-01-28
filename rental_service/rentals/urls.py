from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rentals', views.RentalViewSet, basename='rental')

urlpatterns = [
    path('', views.home, name='home'),
    path('my-bookings/', views.my_bookings, name='my-bookings'),
    path('api/', include(router.urls)),
]
