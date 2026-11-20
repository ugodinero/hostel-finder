from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import landlord, room, student

class LandlordRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        landlord.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user

class StudentRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        student.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user

class RoomForm(forms.ModelForm):
    class Meta:
        model = room
        fields = ['location', 'price', 'room_type', 'description', 'photo', 'photo2', 'photo3']

class LandlordPhoneForm(forms.ModelForm):
    class Meta:
        model = landlord
        fields = ['phone']

class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)


