from django.db import models


class Car(models.Model):
    """Модель автомобиля в автопарке"""
    
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    CAR_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('sports', 'Sports Car'),
        ('luxury', 'Luxury'),
        ('supercar', 'Supercar'),
    ]
    
    car_id = models.CharField(max_length=20, primary_key=True, verbose_name="License Plate")
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=30)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    fuel_level = models.IntegerField(default=100, help_text="Fuel level in percentage (0-100)")
    battery_level = models.IntegerField(default=100, help_text="Battery level for electric cars (0-100)")
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_under_maintenance = models.BooleanField(default=False)
    last_service_date = models.DateField(null=True, blank=True)
    mileage = models.IntegerField(default=0)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['brand', 'model']
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.car_id})"


class RentalRecord(models.Model):
    """Запись о бронировании для проверки конфликтов"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rental_id = models.IntegerField(unique=True, help_text="ID from Rental Service")
    car_id = models.CharField(max_length=20)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pickup_location = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rental #{self.rental_id} - {self.car_id} ({self.status})"
