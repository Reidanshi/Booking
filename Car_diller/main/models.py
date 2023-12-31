from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group
from .managers import HotelManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    photos = models.ImageField(upload_to='user_images/', blank=False, null=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    hotel = models.ForeignKey('main.Hotel', on_delete=models.CASCADE, null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    passport_data = models.CharField(max_length=255, blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.id:  # Проверяем, что id установлен
            super().save(*args, **kwargs)  # Сначала сохраняем пользователя, чтобы у него был id
            if self.is_superuser:
                group, created = Group.objects.get_or_create(name='Hotel Administrator')
                self.groups.add(group)
        else:
            super().save(*args, **kwargs)


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    description = models.TextField()
    photos = models.ImageField(upload_to='hotel_images/', blank=False, null=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    room_count = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_hotel')
    objects = HotelManager()

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
    description = models.TextField()
    beds_counter = models.PositiveSmallIntegerField()
    number_room = models.PositiveSmallIntegerField()
    level = models.PositiveSmallIntegerField()
    photos = models.ImageField(upload_to='room_images/', blank=False, null=False)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number_room} - {self.room_type}"



class Booking(models.Model):
    STATUS_CHOICES = [
        ('on_review', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='on_review')

    def __str__(self):
        return f"{self.user.username} - {self.room.room_type} - {self.check_in_date} to {self.check_out_date}"


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