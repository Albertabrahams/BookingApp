from rest_framework.viewsets import ModelViewSet
from .models import Room
from booking.models import Booking
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum

class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        attendees = request.GET.get('attendees')
        
        if not start_date or not end_date:
            return Response({'error': 'Start date and end dates are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(
            Q(start_date__lt=end_date) & Q(end_date__gt=start_date)
        )

        available_rooms = Room.objects.exclude(bookings__in=bookings)

        total_capacity = available_rooms.aggregate(total_capacity=Sum('size'))['total_capacity']

        if total_capacity is None or total_capacity < int(attendees):
            return Response({'error': 'Total capacity of all rooms is not sufficient for the number of attendees.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)

