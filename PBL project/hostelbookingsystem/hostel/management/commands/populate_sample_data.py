from django.core.management.base import BaseCommand
from hostel.models import Block, Floor, Room


class Command(BaseCommand):
    help = 'Populates the database with sample block data'

    def handle(self, *args, **options):
        # Create male blocks (B1, B2, B3)
        male_blocks = []
        for i in range(1, 4):
            block_name = f"B{i}"
            block, created = Block.objects.get_or_create(
                block_name=block_name,
                defaults={
                    'gender': 'M',
                    'description': f'Male Block {i} with modern amenities'
                }
            )
            male_blocks.append(block)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created block: {block.block_name}'))
        
        # Create female blocks (G1, G2, G3)
        female_blocks = []
        for i in range(1, 4):
            block_name = f"G{i}"
            block, created = Block.objects.get_or_create(
                block_name=block_name,
                defaults={
                    'gender': 'F',
                    'description': f'Female Block {i} with modern amenities'
                }
            )
            female_blocks.append(block)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created block: {block.block_name}'))
        
        all_blocks = male_blocks + female_blocks
        
        # Create floors for each block (3 floors per block)
        total_floors = 0
        total_rooms = 0
        
        for block in all_blocks:
            floors = []
            for floor_num in range(1, 4):
                floor, created = Floor.objects.get_or_create(
                    block=block,
                    floor_number=floor_num,
                    defaults={}
                )
                floors.append(floor)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created floor: {floor}'))
                    total_floors += 1
            
            # Create rooms for each floor (5 rooms per floor)
            for floor in floors:
                for room_num in range(1, 6):
                    room_number = f"{floor.floor_number}{room_num:02d}"  # e.g., 101, 102, etc.
                    room, created = Room.objects.get_or_create(
                        floor=floor,
                        room_number=room_number,
                        defaults={'capacity': 2}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created room: {block.block_name} - {room.room_number}'))
                        total_rooms += 1
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created: {len(all_blocks)} blocks ({len(male_blocks)} male, {len(female_blocks)} female)'))
        self.stdout.write(self.style.SUCCESS(f'Created: {total_floors} floors (3 per block)'))
        self.stdout.write(self.style.SUCCESS(f'Created: {total_rooms} rooms (5 per floor)'))
        self.stdout.write(self.style.SUCCESS('='*50))
