from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    usertype=models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)

    

class OwnerApprove(models.Model):
    owner=models.CharField(max_length=30,null=True,blank=False)
    Name=models.CharField(max_length=50,null=True,blank=False,unique=True)
    Location=models.CharField(max_length=30,null=True,blank=False)
    Country=models.CharField(max_length=30,default="India")
    Contact=models.BigIntegerField()
    username=models.CharField(max_length=40)
    password=models.CharField(max_length=40)
    email=models.EmailField(max_length=30)



class Owner(models.Model):   
    owner=models.CharField(max_length=30,null=True,blank=False)
    Name=models.CharField(max_length=50,null=True,blank=False,unique=True)
    Location=models.CharField(max_length=30,null=True,blank=False)
    Country=models.CharField(max_length=30,default="India")
    Contact=models.BigIntegerField()
    O_id=models.OneToOneField(User,on_delete=models.CASCADE,related_name='owner_profile')
    def __str__(self):
        return self.Name



class Resort(models.Model):
    Name=models.CharField(max_length=50,null=True,blank=False)
    Location=models.CharField(max_length=30,null=True,blank=False)
    Country=models.CharField(max_length=30,default="India")
    Description=models.TextField(max_length=300,null=True,blank=False)
    Contact=models.BigIntegerField()
    Own_id=models.ForeignKey(Owner,on_delete=models.CASCADE,related_name='resorts')
    Re_id=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
   

class Rooms(models.Model):
    Room_status=models.CharField(max_length=40, default="Available")
    room_type=(("1","premium"),("2","deluxe"),("3","basic"),)
    Room_type=models.CharField(max_length=50,choices=room_type)
    Capacity=models.IntegerField()
    room_number = models.CharField(max_length=10) 
    total_room = models.IntegerField()
    Price=models.FloatField(default=5000)
    R_id= models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='rooms')

def __str__(self):
    return f"Room {self.room_number} - Type: {self.get_Room_type_display()} - Capacity: {self.Capacity} - Price: {self.Price}"




class ResortImage(models.Model):
    resort = models.ForeignKey('Resort', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='resort_images')

class RoomImage(models.Model):
    room = models.ForeignKey('Rooms', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images')




