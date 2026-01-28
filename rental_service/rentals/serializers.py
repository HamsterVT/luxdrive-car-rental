from rest_framework import serializers
from .models import Rental


class RentalSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Rental"""
    
    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'status', 'total_price', 'rejection_reason']


class RentalCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания аренды"""
    
    class Meta:
        model = Rental
        fields = [
            'car_id', 'user_email', 'user_name', 'user_phone',
            'start_datetime', 'end_datetime', 'pickup_location',
            'return_location', 'rental_type'
        ]
