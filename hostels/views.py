import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import LandlordRegistrationForm, StudentRegistrationForm, RoomForm, LandlordPhoneForm, MessageForm
from .models import landlord, room, student, roomrequest


def register_landlord(request):
    if request.method == 'POST':
        form = LandlordRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            code = str(random.randint(100000, 999999))
            request.session['otp_code'] = code
            request.session['otp_user_id'] = user.id
            send_mail('Your Hostel Finder verification code', 'Your verification code is ' + code, 'ugochukwugreat07@gmail.com', [email], fail_silently=False)
            return redirect('verify_otp')
    else:
        form = LandlordRegistrationForm()
    return render(request, 'hostels/register.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data['email']
            code = str(random.randint(100000, 999999))
            request.session['otp_code'] = code
            request.session['otp_user_id'] = user.id
            send_mail('Your Hostel Finder verification code', 'Your verification code is ' + code, 'ugochukwugreat07@gmail.com', [email], fail_silently=False)
            return redirect('verify_otp')
    else:
        form = StudentRegistrationForm()
    return render(request, 'hostels/register_student.html', {'form': form})

@login_required
def room_list(request):
    rooms = room.objects.all()
    max_price = request.GET.get('max_price')
    room_type = request.GET.get('room_type')
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if room_type:
        rooms = rooms.filter(room_type__icontains=room_type)
    return render(request, 'hostels/room_list.html', {'rooms': rooms})

@login_required
def add_room(request):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.landlord = my_landlord
            new_room.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'hostels/add_room.html', {'form': form})


def landing(request):
    rooms = room.objects.all()
    q = request.GET.get('q')
    if q:
        rooms = rooms.filter(location__icontains=q)
    return render(request, 'hostels/landing.html', {'rooms': rooms})

def room_detail(request, pk):
    my_room = get_object_or_404(room, pk=pk)
    phone = my_room.landlord.phone
    if phone.startswith('0'):
        whatsapp_phone = '234' + phone[1:]
    else:
        whatsapp_phone = phone
    return render(request, 'hostels/room_detail.html', {'room': my_room, 'whatsapp_phone': whatsapp_phone})

def login_landlord(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                landlord.objects.get(user=user)
                return redirect('my_rooms')
            except landlord.DoesNotExist:
                return redirect('room_list')
    else:
        form = AuthenticationForm()
    return render(request, 'hostels/login.html', {'form': form})


def logout_landlord(request):
    logout(request)
    return redirect('landing')

def verify_otp(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session.get('otp_code'):
            user = User.objects.get(pk=request.session.get('otp_user_id'))
            del request.session['otp_code']
            del request.session['otp_user_id']
            login(request, user)
            return redirect('room_list')
        else:
            return render(request, 'hostels/verify.html', {'error': 'Wrong code. Try again.'})
    return render(request, 'hostels/verify.html')

@login_required
def my_rooms(request):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    rooms = room.objects.filter(landlord=my_landlord)
    return render(request, 'hostels/my_rooms.html', {'rooms': rooms})

@login_required
def edit_room(request, pk):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    my_room = get_object_or_404(room, pk=pk, landlord=my_landlord)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=my_room)
        if form.is_valid():
            form.save()
            return redirect('my_rooms')
    else:
        form = RoomForm(instance=my_room)
    return render(request, 'hostels/edit_room.html', {'form': form})


@login_required
def delete_room(request, pk):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    my_room = get_object_or_404(room, pk=pk, landlord=my_landlord)
    if request.method == 'POST':
        my_room.delete()
        return redirect('my_rooms')
    return render(request, 'hostels/delete_room.html', {'room': my_room})

@login_required
def edit_phone(request):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    if request.method == 'POST':
        form = LandlordPhoneForm(request.POST, instance=my_landlord)
        if form.is_valid():
            form.save()
            return redirect('my_rooms')
    else:
        form = LandlordPhoneForm(instance=my_landlord)
    return render(request, 'hostels/edit_phone.html', {'form': form})

@login_required
def request_room(request, pk):
    my_room = get_object_or_404(room, pk=pk)
    try:
        my_student = student.objects.get(user=request.user)
    except student.DoesNotExist:
        return redirect('room_list')
    roomrequest.objects.get_or_create(student=my_student, room=my_room)
    return redirect('room_detail', pk=pk)

@login_required
def my_requests(request):
    try:
        my_landlord = landlord.objects.get(user=request.user)
    except landlord.DoesNotExist:
        return redirect('room_list')
    requests = roomrequest.objects.filter(room__landlord=my_landlord)
    return render(request, 'hostels/my_requests.html', {'requests': requests})

@login_required
def message_landlord(request, pk):
    my_room = get_object_or_404(room, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['message']
            send_mail(
                'Room message: ' + my_room.location,
                'From ' + request.user.username + ': ' + text,
                'ugochukwugreat07@gmail.com',
                [my_room.landlord.user.email],
            )
            return redirect('room_detail', pk=pk)
    else:
        form = MessageForm()
    return render(request, 'hostels/message.html', {'form': form, 'room': my_room})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('room_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'hostels/change_password.html', {'form': form})





