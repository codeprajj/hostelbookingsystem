from django.contrib import admin
from .models import Block, Floor, Room, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'get_full_name']
    list_filter = ['gender']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['block_name', 'gender', 'description']
    list_filter = ['gender']
    search_fields = ['block_name']


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['block', 'floor_number']
    list_filter = ['block']
    search_fields = ['block__block_name', 'floor_number']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'block_name', 'floor', 'capacity', 'is_booked', 'booked_by']
    list_filter = ['is_booked', 'floor__block', 'floor']
    search_fields = ['room_number', 'floor__block__block_name']
    readonly_fields = ['is_booked', 'booked_by']
    
    def block_name(self, obj):
        return obj.floor.block.block_name
    block_name.short_description = 'Block'
