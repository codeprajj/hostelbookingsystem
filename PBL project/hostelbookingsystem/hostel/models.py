from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Block(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    block_name = models.CharField(max_length=50, unique=True)  # e.g., B1, B2, B3, G1, G2, G3
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.block_name} ({self.get_gender_display()})"

    class Meta:
        ordering = ['block_name']


class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField()

    def __str__(self):
        return f"{self.block.block_name} - Floor {self.floor_number}"

    class Meta:
        ordering = ['block', 'floor_number']
        unique_together = ['block', 'floor_number']


class Room(models.Model):
    room_number = models.CharField(max_length=50)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField(default=1)
    booked_by_users = models.ManyToManyField(User, related_name='booked_rooms', blank=True)
    
    # Keep for backward compatibility and quick queries
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='primary_booked_rooms')

    def __str__(self):
        return f"{self.floor.block.block_name} - {self.room_number}"
    
    def get_current_occupancy(self):
        """Get current number of occupants"""
        return self.booked_by_users.count()
    
    def is_full(self):
        """Check if room is at full capacity"""
        return self.get_current_occupancy() >= self.capacity
    
    def get_available_spots(self):
        """Get number of available spots"""
        return max(0, self.capacity - self.get_current_occupancy())
    
    def save(self, *args, **kwargs):
        # Update is_booked and booked_by if room already exists
        # Note: ManyToManyField changes require calling save() after add/remove
        # The views handle this explicitly, but this helps for admin/other direct saves
        if self.pk:
            # Note: ManyToMany count is accurate even before save() for in-memory changes
            self.is_booked = self.is_full()
            # Keep booked_by as the first user for backward compatibility
            if self.booked_by_users.exists() and not self.booked_by:
                self.booked_by = self.booked_by_users.first()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['floor', 'room_number']
        unique_together = ['floor', 'room_number']
