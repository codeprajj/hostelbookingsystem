from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Block, Floor, Room, UserProfile
from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = f"{user.first_name} {user.last_name}".strip()
            if full_name:
                messages.success(request, f'Account created for {full_name}!')
            else:
                messages.success(request, f'Account created for {user.username}!')
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hostel/register.html', {'form': form})


def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


@login_required
def dashboard_view(request):
    # Find room where user is an occupant
    user_room = Room.objects.filter(booked_by_users=request.user).first()
    context = {
        'user': request.user,
        'user_room': user_room,
    }
    return render(request, 'hostel/dashboard.html', context)


@login_required
def blocks_list_view(request):
    """Show list of blocks filtered by user's gender"""
    # Get user's gender from profile - with proper error handling
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
        messages.warning(request, 'Your profile was missing. Please update your gender information.')
        return redirect('dashboard')
    
    user_gender = user_profile.gender
    
    # STRICT: Only show blocks matching user's gender
    if not user_gender:
        messages.error(request, 'Gender information is required to view blocks. Please contact administrator or re-register with gender information.')
        return redirect('dashboard')
    
    blocks = Block.objects.filter(gender=user_gender).order_by('block_name')
    
    context = {
        'blocks': blocks,
        'user_gender': user_gender,
    }
    return render(request, 'hostel/blocks_list.html', context)


@login_required
def block_layout_view(request, block_id):
    """Show layout of a specific block"""
    block = get_object_or_404(Block, id=block_id)
    
    # STRICT Check if user has access to this block based on gender
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        messages.error(request, 'Your profile was missing. Please update your gender information.')
        return redirect('dashboard')
    
    user_gender = user_profile.gender
    
    # CRITICAL: Deny access if gender doesn't match or is not set
    if not user_gender:
        messages.error(request, 'Gender information is required. Access denied.')
        return redirect('dashboard')
    
    if block.gender != user_gender:
        messages.error(request, f'Access denied: You do not have permission to view {block.block_name} block. This block is for {block.get_gender_display()}s only.')
        return redirect('blocks_list')
    
    floors = Floor.objects.filter(block=block).order_by('floor_number')
    
    # Organize rooms by floor
    floors_data = []
    for floor in floors:
        rooms = Room.objects.filter(floor=floor).order_by('room_number')
        floors_data.append({
            'floor': floor,
            'rooms': rooms
        })
    
    context = {
        'block': block,
        'floors_data': floors_data,
    }
    return render(request, 'hostel/block_layout.html', context)


@login_required
def room_detail_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # STRICT Check if user has access to this room's block
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        messages.error(request, 'Your profile was missing. Please update your gender information.')
        return redirect('dashboard')
    
    user_gender = user_profile.gender
    
    # CRITICAL: Deny access if gender doesn't match or is not set
    if not user_gender:
        messages.error(request, 'Gender information is required. Access denied.')
        return redirect('dashboard')
    
    if room.floor.block.gender != user_gender:
        messages.error(request, f'Access denied: You cannot access rooms in {room.floor.block.block_name} block. This block is for {room.floor.block.get_gender_display()}s only.')
        return redirect('blocks_list')
    
    # Check if user is already in this room
    user_in_room = room.booked_by_users.filter(id=request.user.id).exists()
    # Check if user has any booking
    user_has_booking = Room.objects.filter(booked_by_users=request.user).exists()
    # Check if room has available spots
    available_spots = room.get_available_spots()
    can_book = available_spots > 0 and not user_in_room
    
    # Get all occupants
    occupants = room.booked_by_users.all()
    
    context = {
        'room': room,
        'can_book': can_book,
        'user_has_booking': user_has_booking,
        'user_in_room': user_in_room,
        'available_spots': available_spots,
        'current_occupancy': room.get_current_occupancy(),
        'occupants': occupants,
    }
    return render(request, 'hostel/room_detail.html', context)


@login_required
def confirm_booking_view(request, room_id):
    """Confirmation page before booking"""
    room = get_object_or_404(Room, id=room_id)
    
    # STRICT Check if user has access to this room's block
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        messages.error(request, 'Your profile was missing. Please update your gender information.')
        return redirect('dashboard')
    
    user_gender = user_profile.gender
    
    # CRITICAL: Deny access if gender doesn't match or is not set
    if not user_gender:
        messages.error(request, 'Gender information is required. Access denied.')
        return redirect('dashboard')
    
    if room.floor.block.gender != user_gender:
        messages.error(request, f'Access denied: You cannot book rooms in {room.floor.block.block_name} block. This block is for {room.floor.block.get_gender_display()}s only.')
        return redirect('blocks_list')
    
    # Check if room is full
    if room.is_full():
        messages.error(request, 'This room is at full capacity.')
        return redirect('room_detail', room_id=room.id)
    
    # Check if user is already in this room
    if room.booked_by_users.filter(id=request.user.id).exists():
        messages.error(request, 'You are already booked in this room.')
        return redirect('room_detail', room_id=room.id)
    
    user_has_booking = Room.objects.filter(booked_by_users=request.user).exists()
    available_spots = room.get_available_spots()
    
    context = {
        'room': room,
        'user_has_booking': user_has_booking,
        'available_spots': available_spots,
        'current_occupancy': room.get_current_occupancy(),
    }
    return render(request, 'hostel/confirm_booking.html', context)


@login_required
def book_room_view(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    # STRICT Check if user has access to this room's block
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        messages.error(request, 'Your profile was missing. Please update your gender information.')
        return redirect('dashboard')
    
    user_gender = user_profile.gender
    
    # CRITICAL: Deny access if gender doesn't match or is not set
    if not user_gender:
        messages.error(request, 'Gender information is required. Access denied.')
        return redirect('dashboard')
    
    if room.floor.block.gender != user_gender:
        messages.error(request, f'Access denied: You cannot book rooms in {room.floor.block.block_name} block. This block is for {room.floor.block.get_gender_display()}s only.')
        return redirect('blocks_list')
    
    # Check if room is full
    if room.is_full():
        messages.error(request, 'This room is at full capacity.')
        return redirect('room_detail', room_id=room.id)
    
    # Check if user is already in this room
    if room.booked_by_users.filter(id=request.user.id).exists():
        messages.error(request, 'You are already booked in this room.')
        return redirect('room_detail', room_id=room.id)
    
    # Check if user already has a booking in another room
    user_other_room = Room.objects.filter(booked_by_users=request.user).exclude(id=room.id).first()
    if user_other_room:
        # Allow booking if they want to switch (we'll cancel the old one)
        if request.POST.get('confirm_switch') == 'yes':
            # Remove user from old room
            user_other_room.booked_by_users.remove(request.user)
            # Refresh from database
            user_other_room.refresh_from_db()
            # Update old room's booked_by and is_booked
            if user_other_room.booked_by == request.user:
                if user_other_room.booked_by_users.exists():
                    user_other_room.booked_by = user_other_room.booked_by_users.first()
                else:
                    user_other_room.booked_by = None
            user_other_room.is_booked = user_other_room.is_full()
            user_other_room.save()
        else:
            messages.error(request, 'You already have a room booked. Please cancel it first or confirm to switch rooms.')
            return redirect('room_detail', room_id=room.id)
    
    # Add user to the room
    room.booked_by_users.add(request.user)
    # Refresh from database to get updated count
    room.refresh_from_db()
    # Update is_booked and booked_by
    room.is_booked = room.is_full()
    if not room.booked_by:
        room.booked_by = request.user
    room.save()
    
    current_occupancy = room.get_current_occupancy()
    messages.success(request, f'Successfully booked room {room.room_number} in {room.floor.block.block_name}! ({current_occupancy}/{room.capacity} occupants)')
    return redirect('dashboard')


@login_required
def cancel_booking_view(request, room_id):
    """Cancel a booking"""
    room = get_object_or_404(Room, id=room_id)
    
    # Check if user is in this room
    if not room.booked_by_users.filter(id=request.user.id).exists():
        messages.error(request, 'You are not booked in this room.')
        return redirect('dashboard')
    
    # Remove user from room
    room.booked_by_users.remove(request.user)
    # Refresh from database to get updated count
    room.refresh_from_db()
    
    # Update booked_by and is_booked
    if room.booked_by == request.user:
        if room.booked_by_users.exists():
            room.booked_by = room.booked_by_users.first()
        else:
            room.booked_by = None
    
    room.is_booked = room.is_full()
    room.save()
    
    messages.success(request, f'Successfully cancelled booking for room {room.room_number}.')
    return redirect('dashboard')
