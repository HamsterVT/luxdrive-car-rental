from rest_framework import serializers
from .models import Car, RentalRecord


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Car"""
    
    class Meta:
        model = Car
        fields = '__all__'


class CarListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка автомобилей"""
    
    class Meta:
        model = Car
        fields = [
            'car_id', 'brand', 'model', 'year', 'color', 'car_type',
            'fuel_type', 'fuel_level', 'battery_level', 'location',
            'hourly_rate', 'daily_rate', 'is_available', 'is_under_maintenance',
            'image_url'
        ]


class AvailabilityCheckSerializer(serializers.Serializer):
    """Сериализатор для проверки доступности"""
    
    car_id = serializers.CharField(max_length=20)
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    pickup_location = serializers.CharField(max_length=100)


class RentalRecordSerializer(serializers.ModelSerializer):
    """Сериализатор для записи бронирования"""
    
    class Meta:
        model = RentalRecord
        fields = '__all__'
