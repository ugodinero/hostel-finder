from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('register/', views.register_landlord, name='landlord_register'),
    path('register/student/', views.register_student, name='student_register'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_landlord, name='login_landlord'),
    path('logout/', views.logout_landlord, name='logout_landlord'),
    path('add/', views.add_room, name='add_room'),
    path('my-rooms/', views.my_rooms, name='my_rooms'),
    path('<int:pk>/edit/', views.edit_room, name='edit_room'),
    path('<int:pk>/delete/', views.delete_room, name='delete_room'),
    path('edit-phone/', views.edit_phone, name='edit_phone'),
    path('<int:pk>/request/', views.request_room, name='request_room'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('<int:pk>/message/', views.message_landlord, name='message_landlord'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='hostels/password_reset_form.html'), name='password_reset'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='hostels/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='hostels/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='hostels/password_reset_complete.html'), name='password_reset_complete'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
]
