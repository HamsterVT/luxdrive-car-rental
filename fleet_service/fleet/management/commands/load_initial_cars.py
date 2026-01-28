from django.core.management.base import BaseCommand
from fleet.models import Car


class Command(BaseCommand):
    help = 'Load initial car data'

    def handle(self, *args, **kwargs):
        # Проверяем, есть ли уже машины
        if Car.objects.exists():
            self.stdout.write(self.style.WARNING('Cars already exist. Skipping...'))
            return

        cars_data = [
            {
                'car_id': 'M5F90',
                'brand': 'BMW',
                'model': 'M5 F90',
                'year': 2023,
                'color': 'Black',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Downtown Station',
                'hourly_rate': 150,
                'daily_rate': 1200,
                'is_available': True,
                'image_url': '/static/images/bmw_m5_f90_1769585537447.png'
            },
            {
                'car_id': 'M3G80',
                'brand': 'BMW',
                'model': 'M3 G80',
                'year': 2024,
                'color': 'White',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Downtown Station',
                'hourly_rate': 120,
                'daily_rate': 1000,
                'is_available': True,
                'image_url': '/static/images/bmw_m3_g80_1769587817963.png'
            },
            {
                'car_id': 'M8COMP',
                'brand': 'BMW',
                'model': 'M8 Competition',
                'year': 2023,
                'color': 'Blue',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Airport Terminal',
                'hourly_rate': 180,
                'daily_rate': 1500,
                'is_available': True,
                'image_url': '/static/images/bmw_m8_competition_1769588008746.png'
            },
            {
                'car_id': 'F812',
                'brand': 'Ferrari',
                'model': '812 Competizione',
                'year': 2024,
                'color': 'Red',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Downtown Station',
                'hourly_rate': 300,
                'daily_rate': 2500,
                'is_available': True,
                'image_url': '/static/images/ferrari_812_competizione_1769588222950.png'
            },
            {
                'car_id': 'G63AMG',
                'brand': 'Mercedes',
                'model': 'G63 AMG',
                'year': 2023,
                'color': 'Black',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'City Center',
                'hourly_rate': 140,
                'daily_rate': 1100,
                'is_available': True,
                'image_url': '/static/images/mercedes_g63_1769586376400.png'
            },
            {
                'car_id': 'G636X6',
                'brand': 'Mercedes',
                'model': 'G63 6x6',
                'year': 2024,
                'color': 'Matte Black',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Airport Terminal',
                'hourly_rate': 200,
                'daily_rate': 1800,
                'is_available': True,
                'image_url': '/static/images/mercedes_g63_6x6_1769588309525.png'
            },
            {
                'car_id': 'GHOST',
                'brand': 'Rolls-Royce',
                'model': 'Ghost',
                'year': 2024,
                'color': 'Silver',
                'fuel_type': 'petrol',
                'fuel_level': 100,
                'battery_level': 0,
                'location': 'Downtown Station',
                'hourly_rate': 250,
                'daily_rate': 2000,
                'is_available': True,
                'image_url': '/static/images/rolls_royce_ghost_1769588635498.png'
            },
        ]

        # Создаём машины
        for car_data in cars_data:
            Car.objects.create(**car_data)
            self.stdout.write(self.style.SUCCESS(f'Created car: {car_data["brand"]} {car_data["model"]}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(cars_data)} cars!'))
