from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet, basename='car')

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('api/', include(router.urls)),
    path('api/check-availability/', views.check_availability, name='check-availability'),
    path('api/rentals/register/', views.register_rental, name='register-rental'),
    path('api/bookings/<int:rental_id>/approve/', views.approve_booking, name='approve-booking'),
    path('api/bookings/<int:rental_id>/reject/', views.reject_booking, name='reject-booking'),
]
