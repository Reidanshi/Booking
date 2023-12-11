from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.email



class Hotel(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    description = models.TextField()
    photos = models.ImageField(upload_to='hotel_images/', blank=False, null=False)
    rating = models.PositiveSmallIntegerField(default=0, choices=[(i,i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return f'/hotels/{self.id}'



class Room(models.Model):
    ROOM_TYPES = [
        ('Standart', 'Standart'),
        ('Bedroom', 'Bedroom'),
        ('Superior', 'Superior'),
        ('Studio', 'Studio'),
        ('Family Room', 'Family Room'),
        ('Family Studio', 'Family Studio'),
        ('Suite', 'Suite'),
        ('Junior Suite', 'Junior Suite'),
        ('De Luxe', 'De Luxe'),
        ('Executive Suite', 'Executive Suite'),
        ('Business Room', 'Business Room'),
        ('Connected Room', 'Connected Room'),
        ('Duplex', 'Duplex'),
        ('Apartment', 'Apartment'),
        ('King Suites', 'King Suites'),
        ('President Suites', 'President Suites'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    photos = models.ImageField(upload_to='room_images/', blank=False, null=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.room_type



class Booking(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)





class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=0, choices=[(i,i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} - {self.rating}"