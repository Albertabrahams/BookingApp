from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Booking
from .serializers import BookingSerializer
from django.db.models import Q
from room.models import Room
from django.utils import timezone
from django.db.models import Sum

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        attendees = request.data.get('attendees')

        if not (start_date and end_date and attendees):
            return Response({'error': 'Start date, end date, and number of attendees are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        capacity = Room.objects.aggregate(capacity=Sum('size'))['capacity']
        
        rez_capacity = Booking.objects.filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        ).aggregate(rez_capacity=Sum('attendees'))['rez_capacity'] or 0
        
        print("total_capacity", capacity, rez_capacity)

        total_capacity = capacity - rez_capacity

        
        if total_capacity < int(attendees):
            return Response({'error': 'Total capacity of all rooms is not sufficient for the number of attendees.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_booking = Booking.objects.filter(
            # room__in=available_rooms,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

        if existing_booking:
            return Response({'error': 'There is already a booking for the selected dates and number of attendees.'}, status=status.HTTP_400_BAD_REQUEST)


        selected_room = available_rooms.first()

        if not selected_room:
            return Response({'error': 'No available rooms for the selected dates and number of attendees.'}, status=status.HTTP_400_BAD_REQUEST)

        booking_data = {
            'room': selected_room.pk,
            'start_date': start_date,
            'end_date': end_date,
            'attendees': attendees
            # Add other fields as needed
        }
        serializer = self.get_serializer(data=booking_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



