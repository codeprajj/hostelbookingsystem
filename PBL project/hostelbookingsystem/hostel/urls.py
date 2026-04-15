from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='hostel/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('blocks/', views.blocks_list_view, name='blocks_list'),
    path('block/<int:block_id>/', views.block_layout_view, name='block_layout'),
    path('room/<int:room_id>/', views.room_detail_view, name='room_detail'),
    path('room/<int:room_id>/confirm/', views.confirm_booking_view, name='confirm_booking'),
    path('room/<int:room_id>/book/', views.book_room_view, name='book_room'),
    path('room/<int:room_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
]
