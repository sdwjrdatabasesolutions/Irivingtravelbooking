from django.contrib import admin
from .models import Room, Reservation, RoomType, Amenity

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    list_filter = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'price_per_night', 'capacity', 'available', 'rating']
    list_filter = ['room_type', 'available', 'has_wifi', 'has_ac']
    search_fields = ['name', 'description']
    filter_horizontal = ['amenities']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'room_type', 'description', 'price_per_night', 'capacity', 'available', 'rating')
        }),
        ('Features', {
            'fields': ('has_wifi', 'has_tv', 'has_ac', 'has_breakfast', 'amenities')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status', 'check_in_date', 'room']
    search_fields = ['guest_name', 'guest_email', 'confirmation_code']
    readonly_fields = ['created_at', 'confirmation_code']
    
    fieldsets = (
        ('Reservation Details', {
            'fields': ('room', 'guest_name', 'guest_email', 'guest_phone')
        }),
        ('Stay Information', {
            'fields': ('check_in_date', 'check_out_date', 'number_of_guests', 'special_requests')
        }),
        ('Payment & Status', {
            'fields': ('total_price', 'status')
        }),
        ('System Info', {
            'fields': ('confirmation_code', 'created_at'),
            'classes': ('collapse',)
        }),
    )
