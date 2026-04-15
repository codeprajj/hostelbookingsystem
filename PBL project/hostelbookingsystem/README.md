# 🏠 Hostel Booking System

A modern, Django-based web application for managing hostel room bookings with gender-based block filtering. Built with clean design, user-friendly interface, and comprehensive booking management features.

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite)

## ✨ Features

### 🔐 User Authentication
- **User Registration**: Create accounts with full name (first name, last name), username, email, gender, and password
- **Secure Login/Logout**: Django's built-in authentication system with custom logout handling
- **User Profile**: Display full name, gender, and booking information
- **Gender-Based Access Control**: Strict enforcement - users can only view and book rooms in blocks matching their gender

### 🏢 Block Management System
- **Block System**: Organized into gender-specific blocks
  - **Male Blocks**: B1, B2, B3
  - **Female Blocks**: G1, G2, G3
- **Block Layout Visualization**: Interactive grid-based layout showing floors and rooms for each block
- **Room Status**: Real-time availability status (Available/Partially Booked/Full) with color coding
- **Room Details**: Comprehensive room information including block, floor, capacity, occupancy, and booking status
- **Occupancy Tracking**: Display current occupancy (e.g., "2/4") and available spots for each room

### 📅 Booking System
- **Multi-Occupancy Support**: Multiple users can book the same room based on room capacity (e.g., if capacity is 2, two users can share the room)
- **One Room Per User**: Users can book only one room at a time (but can share rooms with others)
- **Gender-Based Filtering**: Users automatically see only blocks matching their gender
- **Booking Confirmation**: Confirmation page before finalizing booking
- **Booking Validation**: Prevents booking full rooms, double booking same room, and booking multiple rooms
- **Occupancy Display**: Real-time display of current occupancy (e.g., "1/2", "2/2 Full") and available spots
- **Occupant List**: View all current occupants of a room with their full names
- **Cancel Booking**: Users can cancel their current booking
- **Room Switching**: Users can switch to a different room (automatically cancels old booking)
- **Full Name Display**: Shows the full name of all students who have booked the room
- **Booking Management**: Easy booking, cancellation, and viewing of room details

### 🎨 Modern UI/UX
- **Clean Design**: Modern blue color scheme with gradient effects
- **SVG Icons**: Beautiful, scalable icons throughout the interface
- **Responsive Layout**: Mobile-friendly design that works on all devices
- **Intuitive Navigation**: Easy-to-use navigation and user interface
- **Modern Footer**: Clean footer with copyright (2025) and author information

## 📋 Project Structure

```
hostel_booking/
├── hostel/                      # Main Django application
│   ├── models.py                # Database models (Block, Floor, Room, UserProfile)
│   ├── views.py                 # View functions
│   ├── forms.py                 # Custom user registration form with gender
│   ├── urls.py                  # URL routing
│   ├── admin.py                 # Admin interface configuration
│   ├── management/
│   │   └── commands/
│   │       └── populate_sample_data.py  # Management command for sample data
│   └── templates/
│       └── hostel/              # HTML templates
│           ├── base.html
│           ├── login.html
│           ├── register.html
│           ├── dashboard.html
│           ├── blocks_list.html
│           ├── block_layout.html
│           ├── room_detail.html
│           └── confirm_booking.html
├── hostel_booking/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── css/
│       └── style.css            # Modern CSS styling
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hostel-booking
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Populate sample data** (optional, for testing)
   ```bash
   python manage.py populate_sample_data
   ```
   This creates:
   - 6 blocks (3 male blocks: B1, B2, B3; 3 female blocks: G1, G2, G3)
   - 18 floors (3 floors per block)
   - 90 rooms (5 rooms per floor)

6. **Create superuser** (for admin access)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - **Main Application**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### For Administrators

1. **Access Admin Panel**
   - Navigate to http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. **Manage Blocks**
   - Create new blocks with block name (e.g., B1, G1), gender, and description
   - Edit existing block information
   - View all blocks and their gender assignments

3. **Manage Floors**
   - Add floors to blocks (typically 3 floors per block)
   - Set floor numbers

4. **Manage Rooms**
   - Create rooms for each floor
   - Set room numbers and capacity
   - View booking status and see which student booked which room

5. **Manage User Profiles**
   - View user profiles and their gender assignments
   - Edit user information if needed

### For Students/Users

1. **Registration**
   - Navigate to `/register/`
   - Fill in:
     - Username
     - First Name
     - Last Name
     - Email (optional)
     - **Gender** (Male/Female) - **Required**
     - Password
     - Password Confirmation
   - Your gender determines which blocks you can access

2. **Login**
   - Navigate to `/login/`
   - Enter username and password

3. **View Available Blocks**
   - Click "Blocks" in the navigation
   - You will see only blocks matching your gender:
     - **Male users**: B1, B2, B3
     - **Female users**: G1, G2, G3

4. **View Block Layout**
   - Click on a block to view its layout
   - Browse available rooms organized by floors
   - Color-coded room status:
     - **Green** = Available
     - **Yellow** = Partially Booked (has occupants but spots available)
     - **Red** = Full (at capacity)
   - See occupancy information (e.g., "1/2", "2/2")

5. **Book a Room**
   - Click on an available room (or partially booked room with available spots)
   - View room details including:
     - Block, floor, capacity
     - Current occupancy (e.g., "1/2")
     - Available spots
     - List of current occupants (if any)
   - Click "Book This Room" button
   - **Confirmation page** will appear showing occupancy information
   - Click "Yes, Confirm Booking" to finalize
   - You can book a room even if others have already booked it, as long as there are available spots

6. **Cancel Booking**
   - Go to Dashboard or Room Detail page
   - Click "Cancel Booking" button
   - Confirm in the popup dialog
   - Your booking will be cancelled

7. **Switch Rooms**
   - If you have a booking and want to change rooms
   - View another available room
   - Click "Click here to switch to this room"
   - Confirm on the confirmation page
   - Your old booking will be automatically cancelled

8. **View Dashboard**
   - Access your dashboard to see:
     - Personal information (including full name and gender)
     - Current booking details (if any)
     - Block and room information
     - Room occupancy information (e.g., "2/4 occupants")
     - Quick action links

## 🗄️ Database Models

### UserProfile
- `user`: OneToOneField to User
- `gender`: CharField - Gender of the user (M/F)

### Block
- `block_name`: CharField - Block identifier (e.g., B1, G1)
- `gender`: CharField - Gender assigned to the block (M/F)
- `description`: TextField - Description of the block

### Floor
- `block`: ForeignKey to Block
- `floor_number`: IntegerField - Floor number (typically 1-3)

### Room
- `room_number`: CharField - Room identifier
- `floor`: ForeignKey to Floor
- `capacity`: IntegerField - Maximum occupancy (e.g., 1, 2, 4)
- `booked_by_users`: ManyToManyField to User - All students currently in the room
- `is_booked`: BooleanField - True when room is at full capacity
- `booked_by`: ForeignKey to User (nullable) - Primary occupant (first student who booked)
- **Methods**:
  - `get_current_occupancy()`: Returns current number of occupants
  - `is_full()`: Returns True if room is at capacity
  - `get_available_spots()`: Returns number of available spots

## 🎨 Design Features

- **Modern Blue Color Scheme**: Professional gradient-based design
- **SVG Icons**: Scalable vector icons for better visual appeal
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Clean UI**: Minimalist design with clear visual hierarchy
- **User-Friendly**: Intuitive navigation and clear call-to-action buttons
- **Gender Badges**: Color-coded badges for male (blue) and female (pink) blocks

## ✅ Features Implemented

- ✅ User registration with full name and gender support
- ✅ Secure login/logout functionality
- ✅ Gender-based block filtering with strict access control
- ✅ User dashboard with booking information
- ✅ Block layout visualization (grid-based)
- ✅ Room detail pages with comprehensive information
- ✅ Booking confirmation page
- ✅ Multi-occupancy room booking system (multiple users can share rooms based on capacity)
- ✅ Occupancy tracking and display (current occupants/available spots)
- ✅ Booking cancellation functionality
- ✅ Room switching (cancel old, book new)
- ✅ Booking validation (prevents booking full rooms, double booking same room)
- ✅ Full name display for all room occupants
- ✅ Partially-booked status visualization
- ✅ Modern, responsive UI with SVG icons
- ✅ Admin interface for managing blocks, floors, and rooms
- ✅ Sample data population command
- ✅ Modern footer with author credits (2025)

## 🛠️ Technology Stack

- **Backend Framework**: Django 5.2.8
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3 (no JavaScript frameworks)
- **Template Engine**: Django Template Language
- **Icons**: SVG (inline)

## 📝 Important Notes

- **Gender-Based Access**: Users can only view and book rooms in blocks matching their gender
  - Male users see: B1, B2, B3
  - Female users see: G1, G2, G3
  - Access is strictly enforced - attempting to access wrong gender blocks results in error
- **Multi-Occupancy Rooms**: Multiple users can book the same room if it has available capacity
  - If a room has capacity 2, two different users can book it
  - If a room has capacity 4, up to four users can share it
  - Occupancy is displayed as "current/capacity" (e.g., "2/4")
- **One Room Per User**: Users can only book one room at a time (but can share that room with others)
- **Booking Confirmation**: All bookings require confirmation before finalizing
- **Booking Cancellation**: Users can cancel their bookings at any time
- **Room Switching**: Users can switch rooms, which automatically cancels the old booking
- **Room Status**: 
  - **Available**: Room has no occupants
  - **Partially Booked**: Room has some occupants but spots are still available
  - **Full**: Room is at capacity and cannot accept more bookings
- **Occupant Display**: Shows all current occupants with their full names when viewing room details
- **Responsive Design**: All pages are mobile-friendly and responsive
- **No JavaScript Required**: Pure HTML/CSS implementation for MVP

## 👨‍💻 Authors

**Made by Prajjwal Sinha

Built with ❤️ using Django
