from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Room, Reservation, RoomType, Amenity
from datetime import datetime, timedelta
import json

def available_rooms(request):
    """Display available rooms with filtering options"""
    rooms = Room.objects.filter(available=True)
    
    # Get filter parameters
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    room_type = request.GET.get('room_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    guests = request.GET.get('guests')
    
    # Apply filters
    if check_in and check_out:
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Filter rooms that are available for these dates
            available_room_ids = []
            for room in rooms:
                if room.is_available(check_in_date, check_out_date):
                    available_room_ids.append(room.id)
            rooms = rooms.filter(id__in=available_room_ids)
        except ValueError:
            pass
    
    if room_type:
        rooms = rooms.filter(room_type__id=room_type)
    
    if min_price:
        rooms = rooms.filter(price_per_night__gte=min_price)
    
    if max_price:
        rooms = rooms.filter(price_per_night__lte=max_price)
    
    if guests:
        rooms = rooms.filter(capacity__gte=guests)
    
    room_types = RoomType.objects.all()
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
        'filter_data': {
            'check_in': check_in,
            'check_out': check_out,
            'room_type': room_type,
            'min_price': min_price,
            'max_price': max_price,
            'guests': guests,
        }
    }
    return render(request, 'reservations/available_rooms.html', context)

def make_reservation(request, room_id):
    """Handle room booking"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        # Get form data
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone', '')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        number_of_guests = request.POST.get('number_of_guests', 1)
        special_requests = request.POST.get('special_requests', '')
        
        # Validate dates
        try:
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            
            # Check if room is available
            if not room.is_available(check_in, check_out):
                messages.error(request, 'Sorry, this room is not available for the selected dates.')
                return render(request, 'reservations/make_reservation.html', {'room': room})
            
            # Calculate total price
            nights = (check_out - check_in).days
            total_price = room.price_per_night * nights
            
            # Create reservation
            reservation = Reservation.objects.create(
                room=room,
                guest_name=guest_name,
                guest_email=guest_email,
                guest_phone=guest_phone,
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_guests=number_of_guests,
                total_price=total_price,
                special_requests=special_requests,
                status='confirmed'
            )
            
            # Redirect to success page
            return redirect('reservation_success', reservation_id=reservation.id)
            
        except ValueError:
            messages.error(request, 'Please enter valid dates.')
    
    # Default dates (tomorrow for check-in, day after for check-out)
    tomorrow = timezone.now().date() + timedelta(days=1)
    day_after = tomorrow + timedelta(days=1)
    
    context = {
        'room': room,
        'default_check_in': tomorrow.strftime('%Y-%m-%d'),
        'default_check_out': day_after.strftime('%Y-%m-%d'),
    }
    return render(request, 'reservations/make_reservation.html', context)

def reservation_success(request, reservation_id):
    """Display reservation confirmation"""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservations/reservation_success.html', {'reservation': reservation})

def home(request):
    """Home page with featured rooms"""
    featured_rooms = Room.objects.filter(available=True).order_by('-rating')[:3]
    room_types = RoomType.objects.all()
    
    context = {
        'featured_rooms': featured_rooms,
        'room_types': room_types,
    }
    return render(request, 'reservations/home.html', context)
