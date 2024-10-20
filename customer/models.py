from django.db import models

from administrator.models import *

# Create your models here.


class Customer(models.Model):
    Cust_name=models.CharField(max_length=50,null=True,blank=False)
    ph_no=models.BigIntegerField()
    email=models.EmailField()
    address=models.TextField(max_length=100,null=True,blank=False)
    country=models.CharField(max_length=50)
    Cid=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.Cust_name
  

class Reviews(models.Model):
    
    resort=models.ForeignKey(Resort,on_delete=models.CASCADE)
    review=models.TextField(max_length=100)
    rating=models.IntegerField()

    def __str__(self):
        return f"{self.rating}"
    
class Customerwallet(models.Model):
    Rid=models.ForeignKey(Resort,on_delete=models.CASCADE)
    cust_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    account_no=models.BigIntegerField()
    balance=models.IntegerField()

    def __str__(self):
        return self.cust_id.Cust_name


class Booking(models.Model):
    rooms_booked = models.IntegerField()
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.resort} - {self.customer}"
    

