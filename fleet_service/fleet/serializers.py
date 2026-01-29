from rest_framework import serializers
from .models import Car, RentalRecord


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Car"""
    
    class Meta:
        model = Car
        fields = '__all__'


class CarListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка автомобилей"""
    full_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = [
            'car_id', 'brand', 'model', 'year', 'color', 'car_type',
            'fuel_type', 'fuel_level', 'battery_level', 'location',
            'hourly_rate', 'daily_rate', 'is_available', 'is_under_maintenance',
            'image_url', 'full_image_url'
        ]
    
    def get_full_image_url(self, obj):
        """Возвращает полный URL картинки с доменом"""
        request = self.context.get('request')
        if request and obj.image_url:
            return request.build_absolute_uri(obj.image_url)
        return obj.image_url


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
