from django.db import models
from django.contrib.auth.models import User

class landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class room(models.Model):
    landlord = models.ForeignKey(landlord, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    room_type = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='room_photos/', null=True, blank=True)


    def __str__(self):
        return self.location

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class roomrequest(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.user.username + ' wants ' + self.room.location
    

