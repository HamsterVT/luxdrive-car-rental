from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from .models import Car, RentalRecord
from .serializers import CarSerializer, CarListSerializer, AvailabilityCheckSerializer, RentalRecordSerializer
import requests


def home(request):
    """Главная страница Fleet Service"""
    cars = Car.objects.all()
    # Serialize cars to include rental_status
    serialized_cars = CarListSerializer(cars, many=True, context={'request': request}).data
    return render(request, 'fleet/home.html', {'cars': serialized_cars})


def admin_dashboard(request):
    """Админ-панель для управления заявками"""
    context = {
        'RENTAL_SERVICE_URL': settings.RENTAL_SERVICE_URL
    }
    return render(request, 'fleet/admin_dashboard.html', context)


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для просмотра автомобилей"""
    
    queryset = Car.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CarListSerializer
        return CarSerializer


@api_view(['POST'])
def check_availability(request):
    """Проверка доступности автомобиля"""
    
    serializer = AvailabilityCheckSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    car_id = serializer.validated_data['car_id']
    start_datetime = serializer.validated_data['start_datetime']
    end_datetime = serializer.validated_data['end_datetime']
    pickup_location = serializer.validated_data['pickup_location']
    
    # Проверка 1: Существует ли машина
    try:
        car = Car.objects.get(car_id=car_id)
    except Car.DoesNotExist:
        return Response({
            'available': False,
            'message': 'Car not found',
            'reason': f'Car with ID {car_id} does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Проверка 2: Машина на обслуживании
    if car.is_under_maintenance:
        return Response({
            'available': False,
            'message': 'Car is not available',
            'reason': 'Car is currently under maintenance'
        })
    
    # Проверка 3: Низкий уровень топлива
    if car.fuel_type == 'electric':
        if car.battery_level < 20:
            return Response({
                'available': False,
                'message': 'Car is not available',
                'reason': f'Low battery level ({car.battery_level}%). Car needs charging'
            })
    else:
        if car.fuel_level < 20:
            return Response({
                'available': False,
                'message': 'Car is not available',
                'reason': f'Low fuel level ({car.fuel_level}%). Car needs refueling'
            })
    
    # Проверка 4: Локация
    if car.location.lower() != pickup_location.lower():
        return Response({
            'available': False,
            'message': 'Car is not available',
            'reason': f'Car is located at {car.location}, not {pickup_location}'
        })
    
    # Проверка 5: Конфликт времени
    conflicting_rentals = RentalRecord.objects.filter(
        car_id=car_id,
        start_datetime__lt=end_datetime,
        end_datetime__gt=start_datetime
    )
    
    if conflicting_rentals.exists():
        conflict = conflicting_rentals.first()
        return Response({
            'available': False,
            'message': 'Car is not available',
            'reason': 'Time conflict with existing booking',
            'conflict_details': {
                'existing_booking_start': conflict.start_datetime,
                'existing_booking_end': conflict.end_datetime
            }
        })
    
    # Все проверки пройдены - машина доступна
    return Response({
        'available': True,
        'message': 'Car is available',
        'car_details': {
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'color': car.color,
            'fuel_type': car.fuel_type,
            'fuel_level': car.fuel_level if car.fuel_type != 'electric' else car.battery_level,
            'location': car.location,
            'hourly_rate': str(car.hourly_rate),
            'daily_rate': str(car.daily_rate),
            'image_url': car.image_url
        }
    })


@api_view(['POST'])
def register_rental(request):
    """Регистрация подтвержденного бронирования"""
    
    serializer = RentalRecordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    rental_record = serializer.save()
    
    # Обновляем статус машины
    try:
        car = Car.objects.get(car_id=rental_record.car_id)
        car.is_available = False
        car.save()
    except Car.DoesNotExist:
        pass
    
    return Response({
        'status': 'success',
        'message': 'Rental registered successfully',
        'rental_record': RentalRecordSerializer(rental_record).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def approve_booking(request, rental_id):
    """Подтвердить заявку на бронирование"""
    
    try:
        # Обновляем статус в Rental Service
        response = requests.patch(
            f"{settings.RENTAL_SERVICE_URL}/api/rentals/{rental_id}/",
            json={'status': 'approved'},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            # Обновляем статус локальной записи
            try:
                rental_record = RentalRecord.objects.get(rental_id=rental_id)
                rental_record.status = 'approved'
                rental_record.save()
                
                # Обновляем статус машины (если это еще не сделано)
                # Машина может быть занята
                try:
                    car = Car.objects.get(car_id=rental_record.car_id)
                    car.is_available = False # Машина теперь "занята" (хотя технически это может быть в будущем)
                    car.save()
                except Car.DoesNotExist:
                    pass
                    
            except RentalRecord.DoesNotExist:
                print(f"Warning: RentalRecord for rental_id {rental_id} not found locally")
            
            return Response({
                'status': 'success',
                'message': 'Booking approved successfully'
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to approve booking'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except requests.exceptions.RequestException as e:
        return Response({
            'status': 'error',
            'message': f'Could not connect to rental service: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
def reject_booking(request, rental_id):
    """Отклонить заявку на бронирование"""
    
    rejection_reason = request.data.get('reason', 'No reason provided')
    
    try:
        # Обновляем статус в Rental Service
        response = requests.patch(
            f"{settings.RENTAL_SERVICE_URL}/api/rentals/{rental_id}/",
            json={
                'status': 'rejected',
                'rejection_reason': rejection_reason
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            # Обновляем статус локальной записи
            try:
                rental_record = RentalRecord.objects.get(rental_id=rental_id)
                rental_record.status = 'rejected'
                rental_record.save()
            except RentalRecord.DoesNotExist:
                print(f"Warning: RentalRecord for rental_id {rental_id} not found locally")
                
            return Response({
                'status': 'success',
                'message': 'Booking rejected successfully'
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Failed to reject booking'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except requests.exceptions.RequestException as e:
        return Response({
            'status': 'error',
            'message': f'Could not connect to rental service: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
