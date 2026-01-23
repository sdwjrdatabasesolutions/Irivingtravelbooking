from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class RoomType(models.Model):
    """Different types of rooms/accommodations"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default='fas fa-bed')  # FontAwesome icon
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Amenity(models.Model):
    """Amenities available in accommodations"""
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default='fas fa-check')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"

class Room(models.Model):
    """Accommodation unit"""
    name = models.CharField(max_length=200)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    available = models.BooleanField(default=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    featured_image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Room features
    has_wifi = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=True)
    has_breakfast = models.BooleanField(default=False)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    
    def __str__(self):
        return f"{self.name} - ${self.price_per_night}/night"
    
    class Meta:
        ordering = ['-created_at']
    
    def is_available(self, check_in, check_out):
        """Check if room is available for given dates"""
        overlapping_reservations = Reservation.objects.filter(
            room=self,
            check_out_date__gt=check_in,
            check_in_date__lt=check_out,
            status__in=['confirmed', 'pending']
        )
        return not overlapping_reservations.exists() and self.available

class Reservation(models.Model):
    """Booking reservation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_code = models.CharField(max_length=10, unique=True, blank=True)
    
    def __str__(self):
        return f"{self.guest_name} - {self.room.name} ({self.check_in_date} to {self.check_out_date})"
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            import random
            import string
            self.confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Calculate total price if not set
        if not self.total_price and self.check_in_date and self.check_out_date:
            nights = (self.check_out_date - self.check_in_date).days
            if nights > 0:
                self.total_price = self.room.price_per_night * nights
        
        super().save(*args, **kwargs)
    
    @property
    def number_of_nights(self):
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0
