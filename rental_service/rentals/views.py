from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import Rental
from .serializers import RentalSerializer, RentalCreateSerializer


def home(request):
    """Главная страница Rental Service"""
    context = {
        'FLEET_SERVICE_URL': settings.FLEET_SERVICE_URL
    }
    return render(request, 'rentals/home.html', context)


def my_bookings(request):
    """Страница со списком заявок пользователя"""
    return render(request, 'rentals/my_bookings.html')


class RentalViewSet(viewsets.ModelViewSet):
    """ViewSet для управления арендой автомобилей"""
    
    queryset = Rental.objects.all().order_by('-created_at')
    serializer_class = RentalSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RentalCreateSerializer
        return RentalSerializer
    
    def create(self, request):
        """Создание новой заявки на аренду с проверкой доступности через Fleet Service"""
        
        serializer = RentalCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверка доступности через Fleet Service
        availability_data = {
            'car_id': serializer.validated_data['car_id'],
            'start_datetime': serializer.validated_data['start_datetime'].isoformat(),
            'end_datetime': serializer.validated_data['end_datetime'].isoformat(),
            'pickup_location': serializer.validated_data['pickup_location'],
        }
        
        try:
            fleet_response = requests.post(
                f"{settings.FLEET_SERVICE_URL}/api/check-availability/",
                json=availability_data,
                timeout=5
            )
            
            if fleet_response.status_code != 200:
                return Response({
                    'error': 'Fleet service unavailable'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            availability_result = fleet_response.json()
            
            if not availability_result.get('available'):
                # Создаем запись с отклонением
                rental = Rental.objects.create(
                    **serializer.validated_data,
                    status='rejected',
                    rejection_reason=availability_result.get('reason', 'Car not available')
                )
                
                return Response({
                    'status': 'rejected',
                    'message': availability_result.get('message'),
                    'reason': availability_result.get('reason'),
                    'rental_id': rental.id
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Машина доступна - создаем заявку на бронирование (pending)
            car_details = availability_result.get('car_details', {})
            
            # Вычисляем стоимость
            duration_hours = (serializer.validated_data['end_datetime'] - 
                            serializer.validated_data['start_datetime']).total_seconds() / 3600
            
            hourly_rate = float(car_details.get('hourly_rate', 10))
            total_price = duration_hours * hourly_rate
            
            rental = Rental.objects.create(
                **serializer.validated_data,
                status='pending',  # Заявка ожидает подтверждения
                total_price=total_price
            )
            
            # Регистрируем бронирование в Fleet Service
            try:
                rental_data = {
                    'rental_id': rental.id,
                    'car_id': rental.car_id,
                    'user_name': rental.user_name,
                    'user_email': rental.user_email,
                    'user_phone': rental.user_phone,
                    'start_datetime': rental.start_datetime.isoformat(),
                    'end_datetime': rental.end_datetime.isoformat(),
                    'pickup_location': rental.pickup_location,
                    'total_price': str(total_price),
                    'status': 'pending'
                }
                
                fleet_register_response = requests.post(
                    f"{settings.FLEET_SERVICE_URL}/api/rentals/register/",
                    json=rental_data,
                    timeout=5
                )
                
                if fleet_register_response.status_code != 201:
                    print(f"Warning: Failed to register rental in Fleet Service: {fleet_register_response.text}")
            except Exception as e:
                print(f"Warning: Could not register rental in Fleet Service: {str(e)}")
            
            return Response({
                'status': 'success',
                'message': 'Booking request submitted successfully. Awaiting approval.',
                'rental': RentalSerializer(rental).data,
                'car_details': car_details,
                'total_price': str(total_price)
            }, status=status.HTTP_201_CREATED)
            
        except requests.exceptions.RequestException as e:
            return Response({
                'error': 'Could not connect to fleet service',
                'details': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def partial_update(self, request, pk=None):
        """Частичное обновление заявки (PATCH) - для approve/reject"""
        try:
            rental = self.get_object()
            
            # Обновляем только разрешенные поля
            if 'status' in request.data:
                rental.status = request.data['status']
            if 'rejection_reason' in request.data:
                rental.rejection_reason = request.data['rejection_reason']
            
            rental.save()
            
            return Response({
                'status': 'success',
                'rental': RentalSerializer(rental).data
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """Обновление статуса заявки (для approve/reject)"""
        try:
            rental = self.get_object()
            
            # Обновляем только разрешенные поля
            if 'status' in request.data:
                rental.status = request.data['status']
            if 'rejection_reason' in request.data:
                rental.rejection_reason = request.data['rejection_reason']
            
            rental.save()
            
            return Response({
                'status': 'success',
                'rental': RentalSerializer(rental).data
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
