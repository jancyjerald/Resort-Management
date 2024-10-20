from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from customer.models import Customer,Booking
from administrator.models import *
from administrator.views import logins
from django.conf import settings
from django.contrib.auth import authenticate




def about(request):
    return render (request,'about.html')
def blog(request):
    return render(request,'blog.html')
def contact(request):
    return render(request,'contact.html')
def gallery(request):
    return render(request,'gallery.html')
def room(request):
    return render(request,'room.html')

def customer_reg(request):
    if request.method=='POST':
        cust_name=request.POST['custname']
        phonenum=request.POST['phonenum']
        email=request.POST['email']
        Country=request.POST['Country']
        address=request.POST['address']
        password=request.POST['password']
        username=request.POST['username']
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")

        x=User.objects.create_user(username=username,password=password,email=email,usertype='Customer')
        y=Customer.objects.create(Cust_name=cust_name,ph_no=phonenum,email=email,country=Country,address=address,Cid=x)
        y.save()
        return redirect(logins)
    else:
         return render(request,'customerreg.html')



def customer_booking(request, resort_id, room_id, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        resort = Resort.objects.get(id=resort_id)
        room = Rooms.objects.get(id=room_id)
    except (Customer.DoesNotExist, Resort.DoesNotExist, Rooms.DoesNotExist):
        raise Http404("Customer, Resort, or Room does not exist")

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        rooms_booked = int(request.POST.get('rooms_booked'))

        
        available_rooms = Rooms.objects.filter(
             R_id=resort
        ).exclude(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        )

        if available_rooms.count() >= rooms_booked:
            
            booking = Booking.objects.create(
                rooms_booked=rooms_booked,
                check_in=check_in,
                check_out=check_out,
                resort=resort,
                customer=customer,
                room=room
            )
            booking.save()
            return render(request, 'booking_confirmation.html', {'booking': booking})
        else:
            
            error_message = 'Not enough available rooms for booking'
            return render(request, 'booking_form.html', {'resort': resort, 'room_id': room_id, 'customer': customer, 'error': error_message, 'available_rooms': available_rooms})
    else:
        
        available_rooms = Rooms.objects.filter(R_id=resort)
        return render(request, 'booking_form.html', {'resort': resort, 'customer': customer, 'room_id': room_id, 'available_rooms': available_rooms})

def owner_booking_view(request):
    if request.user.is_authenticated:
        try:
            owner=Owner.objects.get(O_id=request.user)
            bookings = Booking.objects.filter(resort__Own_id=owner)

            return render(request, 'owner_booking_view.html', {'bookings': bookings})
        
        except Owner.DoesNotExist:
            return render(request, 'error.html', {'message': 'You do not have permission to view bookings.'})
    else:
        return redirect(logins)
