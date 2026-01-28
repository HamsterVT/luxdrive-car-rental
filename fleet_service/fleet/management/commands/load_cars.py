from django.core.management.base import BaseCommand
from fleet.models import Car
from datetime import date


class Command(BaseCommand):
    help = 'Load luxury cars into the database'

    def handle(self, *args, **kwargs):
        # Удаляем существующие машины
        Car.objects.all().delete()
        
        luxury_cars = [
            # BMW M5 F90
            {
                'car_id': 'M5F90',
                'brand': 'BMW',
                'model': 'M5 F90',
                'year': 2023,
                'color': 'Marina Bay Blue',
                'car_type': 'sedan',
                'fuel_type': 'petrol',
                'fuel_level': 85,
                'location': 'Downtown Station',
                'hourly_rate': 150.00,
                'daily_rate': 1200.00,
                'mileage': 5000,
                'is_available': True,
            },
            
            # Mercedes E63S AMG
            {
                'car_id': 'E63S',
                'brand': 'Mercedes-Benz',
                'model': 'E63S AMG',
                'year': 2024,
                'color': 'Obsidian Black',
                'car_type': 'sedan',
                'fuel_type': 'petrol',
                'fuel_level': 90,
                'location': 'Airport Terminal',
                'hourly_rate': 160.00,
                'daily_rate': 1300.00,
                'mileage': 3000,
                'is_available': True,
            },
            
            # BMW M8 Competition
            {
                'car_id': 'M8COMP',
                'brand': 'BMW',
                'model': 'M8 Competition',
                'year': 2024,
                'color': 'Frozen Dark Grey',
                'car_type': 'sports',
                'fuel_type': 'petrol',
                'fuel_level': 75,
                'location': 'Shopping Mall',
                'hourly_rate': 180.00,
                'daily_rate': 1500.00,
                'mileage': 2000,
                'is_available': True,
            },
            
            # BMW M3 G80
            {
                'car_id': 'M3G80',
                'brand': 'BMW',
                'model': 'M3 G80',
                'year': 2023,
                'color': 'Isle of Man Green',
                'car_type': 'sedan',
                'fuel_type': 'petrol',
                'fuel_level': 80,
                'location': 'University Campus',
                'hourly_rate': 140.00,
                'daily_rate': 1100.00,
                'mileage': 8000,
                'is_available': True,
            },
            
            # Mercedes G63 AMG (Гелик)
            {
                'car_id': 'G63AMG',
                'brand': 'Mercedes-Benz',
                'model': 'G63 AMG',
                'year': 2024,
                'color': 'Obsidian Black',
                'car_type': 'suv',
                'fuel_type': 'petrol',
                'fuel_level': 70,
                'location': 'Business District',
                'hourly_rate': 200.00,
                'daily_rate': 1600.00,
                'mileage': 1500,
                'is_available': True,
            },
            
            # Lamborghini Revuelto
            {
                'car_id': 'REVUELTO',
                'brand': 'Lamborghini',
                'model': 'Revuelto',
                'year': 2024,
                'color': 'Verde Mantis',
                'car_type': 'supercar',
                'fuel_type': 'hybrid',
                'fuel_level': 95,
                'battery_level': 100,
                'location': 'Downtown Station',
                'hourly_rate': 500.00,
                'daily_rate': 4000.00,
                'mileage': 500,
                'is_available': True,
            },
            
            # Ferrari SF90 Stradale
            {
                'car_id': 'SF90',
                'brand': 'Ferrari',
                'model': 'SF90 Stradale',
                'year': 2024,
                'color': 'Rosso Corsa',
                'car_type': 'supercar',
                'fuel_type': 'hybrid',
                'fuel_level': 88,
                'battery_level': 95,
                'location': 'Airport Terminal',
                'hourly_rate': 550.00,
                'daily_rate': 4500.00,
                'mileage': 800,
                'is_available': True,
            },
            
            # Ferrari 812 Competizione (12 цилиндров)
            {
                'car_id': '812COMP',
                'brand': 'Ferrari',
                'model': '812 Competizione',
                'year': 2023,
                'color': 'Giallo Modena',
                'car_type': 'supercar',
                'fuel_type': 'petrol',
                'fuel_level': 92,
                'location': 'Shopping Mall',
                'hourly_rate': 600.00,
                'daily_rate': 5000.00,
                'mileage': 600,
                'is_available': True,
            },
            
            # Mercedes G-Class 6x6
            {
                'car_id': 'G6X6',
                'brand': 'Mercedes-Benz',
                'model': 'G63 AMG 6x6',
                'year': 2023,
                'color': 'Designo Platinum Magno',
                'car_type': 'suv',
                'fuel_type': 'petrol',
                'fuel_level': 65,
                'location': 'Business District',
                'hourly_rate': 350.00,
                'daily_rate': 2800.00,
                'mileage': 3000,
                'is_available': True,
            },
            
            # Rolls-Royce Phantom
            {
                'car_id': 'PHANTOM',
                'brand': 'Rolls-Royce',
                'model': 'Phantom',
                'year': 2024,
                'color': 'Arctic White',
                'car_type': 'luxury',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'location': 'Downtown Station',
                'hourly_rate': 400.00,
                'daily_rate': 3200.00,
                'mileage': 1000,
                'is_available': True,
            },
            
            # Rolls-Royce Ghost
            {
                'car_id': 'GHOST',
                'brand': 'Rolls-Royce',
                'model': 'Ghost',
                'year': 2024,
                'color': 'Diamond Black',
                'car_type': 'luxury',
                'fuel_type': 'petrol',
                'fuel_level': 95,
                'location': 'Airport Terminal',
                'hourly_rate': 380.00,
                'daily_rate': 3000.00,
                'mileage': 1200,
                'is_available': True,
            },
            
            # Одна машина с низким топливом для демонстрации
            {
                'car_id': 'M5LOW',
                'brand': 'BMW',
                'model': 'M5 Competition',
                'year': 2023,
                'color': 'Frozen Black',
                'car_type': 'sedan',
                'fuel_type': 'petrol',
                'fuel_level': 15,  # Низкий уровень
                'location': 'University Campus',
                'hourly_rate': 150.00,
                'daily_rate': 1200.00,
                'mileage': 10000,
                'is_available': True,
            },
        ]
        
        for car_data in luxury_cars:
            car = Car.objects.create(**car_data)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created: {car.brand} {car.model} ({car.car_id})')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🚗 Successfully loaded {len(luxury_cars)} luxury cars!')
        )
