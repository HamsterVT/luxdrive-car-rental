from django.db import models


class Rental(models.Model):
    """Модель аренды автомобиля"""
    
    RENTAL_TYPE_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    car_id = models.CharField(max_length=20, verbose_name="License Plate")
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=20)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pickup_location = models.CharField(max_length=100)
    return_location = models.CharField(max_length=100, blank=True)
    rental_type = models.CharField(max_length=10, choices=RENTAL_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.car_id} - {self.user_name} ({self.status})"
