# from rest_framework import serializers, viewsets
# from .models import Hotel, Room, Booking, Review, User
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
# class HotelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hotel
#         fields = '__all__'
#
# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = '__all__'
#
# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'
#
# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class HotelViewSet(viewsets.ModelViewSet):
#     queryset = Hotel.objects.all()
#     serializer_class = HotelSerializer
#
# class RoomViewSet(viewsets.ModelViewSet):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#
# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#
# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer