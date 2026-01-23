from django.core.management.base import BaseCommand
from reservations.models import RoomType, Amenity, Room
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Create room types
        room_types_data = [
            {'name': 'Standard Room', 'description': 'Comfortable room with basic amenities', 'icon_class': 'fas fa-bed'},
            {'name': 'Deluxe Suite', 'description': 'Spacious suite with premium features', 'icon_class': 'fas fa-couch'},
            {'name': 'Family Room', 'description': 'Perfect for families with extra space', 'icon_class': 'fas fa-home'},
            {'name': 'Executive Suite', 'description': 'Luxury accommodation for business travelers', 'icon_class': 'fas fa-briefcase'},
        ]
        
        for data in room_types_data:
            RoomType.objects.get_or_create(**data)
        
        # Create amenities
        amenities_data = [
            {'name': 'Free WiFi', 'icon_class': 'fas fa-wifi'},
            {'name': 'Air Conditioning', 'icon_class': 'fas fa-snowflake'},
            {'name': 'TV', 'icon_class': 'fas fa-tv'},
            {'name': 'Mini Bar', 'icon_class': 'fas fa-wine-bottle'},
            {'name': 'Room Service', 'icon_class': 'fas fa-concierge-bell'},
            {'name': 'Swimming Pool', 'icon_class': 'fas fa-swimming-pool'},
            {'name': 'Gym Access', 'icon_class': 'fas fa-dumbbell'},
            {'name': 'Breakfast Included', 'icon_class': 'fas fa-utensils'},
        ]
        
        for data in amenities_data:
            Amenity.objects.get_or_create(**data)
        
        # Create sample rooms
        rooms_data = [
            {
                'name': 'Ocean View Room',
                'room_type': RoomType.objects.get(name='Standard Room'),
                'description': 'Beautiful room with ocean view, perfect for couples.',
                'price_per_night': Decimal('120.00'),
                'capacity': 2,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'rating': 4.5,
            },
            {
                'name': 'Presidential Suite',
                'room_type': RoomType.objects.get(name='Deluxe Suite'),
                'description': 'Luxurious suite with separate living area and jacuzzi.',
                'price_per_night': Decimal('350.00'),
                'capacity': 4,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'has_breakfast': True,
                'rating': 4.8,
            },
            {
                'name': 'Family Deluxe',
                'room_type': RoomType.objects.get(name='Family Room'),
                'description': 'Spacious room with two queen beds, ideal for families.',
                'price_per_night': Decimal('200.00'),
                'capacity': 6,
                'has_wifi': True,
                'has_tv': True,
                'has_ac': True,
                'rating': 4.3,
            },
        ]
        
        for data in rooms_data:
            room, created = Room.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                # Add some amenities
                amenities = Amenity.objects.filter(name__in=['Free WiFi', 'Air Conditioning', 'TV'])
                room.amenities.set(amenities)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))
