from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from administrator.models import User,Owner,Resort,Rooms,ResortImage,RoomImage,OwnerApprove
from customer.models import Customer
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def adminpage(request):
    return render(request,'admin.html')
def Home(request):
    return render(request,'home.html')

def register_owner(request):
    if request.method=='POST':
        on=request.POST['Oname']
        cn=request.POST['Cname']
        l=request.POST['Location']
        c=request.POST['Country']
        ph=request.POST['Contact']
        email=request.POST['email']
        username=request.POST['username']
        psw=request.POST['psw']

        # x=User.objects.create_user(username=username,password=psw,email=email,usertype='Owner')
        y=OwnerApprove.objects.create(owner=on,Name=cn,Location=l,Country=c,Contact=ph,username=username,password=psw,email=email)
        y.save()
        return redirect(logins)
        
    
    else:
        return render(request,'registerowner.html')

def logins(request):
    if request.method=='POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')

        user = authenticate(request,username=usern,password=passw)
        
        if user is not None and user.is_superuser== 1:
            login(request,user)
            request.session['ad_id']=user.id
            return redirect(adminpage)

        elif user is not None and user.usertype == 'Owner':
            if user.is_approved==True:
                login(request,user)
                Own=Owner.objects.get(O_id=user.id)
                request.session['on_id']=Own.O_id.id
                return render(request,'ownerhome.html',{'data':Own})
            else:
                return HttpResponse('you canot enter website,you are in waiting list')
        
        elif user is not None and user.usertype=='Customer':
            if user.is_approved==False:
                login(request,user)
                print(user.id)
                Cust=Customer.objects.get(Cid=user.id)
                request.session['cust_id']=Cust.Cid.id
                # return render(request,'customerhome.html',{'text':Cust})
                return redirect(customer_view,customer_id=Cust.id)
        
        else:
            return HttpResponse('INVALID USER')
    else:
        return render(request, 'loginuser.html')


def approve_owner(request):
    owner_approvals = OwnerApprove.objects.all()
    return render(request, 'approve.html', {'data': owner_approvals})

def owner_approve(request, owner_approve_id):
    owner_approval = OwnerApprove.objects.get(id=owner_approve_id)
    user = User.objects.create_user(username=owner_approval.username, password=owner_approval.password, email=owner_approval.email, usertype='Owner')
    owner = Owner.objects.create(owner=owner_approval.owner, Name=owner_approval.Name, Location=owner_approval.Location, Country=owner_approval.Country, Contact=owner_approval.Contact, O_id=user)
    user.is_approved = True
    user.save()
    
    owner_approval.delete()  
    return redirect('logins')

def owner_reject(request, owner_approve_id):
    owner_approval = OwnerApprove.objects.get(id=owner_approve_id)
    user = User.objects.get(username=owner_approval.username)
    user.delete()
    owner_approval.delete()
    return HttpResponse("Your registration has been rejected. Please wait.")


def registerresort(request,id):
    return render(request,'ownerhome.html')



def addresorts(request, id):
    if request.method == 'POST':
        rname = request.POST['resort_name']
        lc = request.POST['location']
        cntry = request.POST['country']
        desc = request.POST['description']
        cnt = request.POST['contact']
        img_files = request.FILES.getlist('resort_images')

        
        o = Owner.objects.get(id=id)
        u = request.user

        
        a = Resort.objects.create(Name=rname, Location=lc, Country=cntry, Description=desc, Contact=cnt, Own_id=o, Re_id=u)

      
        for img_file in img_files:
            ResortImage.objects.create(image=img_file, resort=a)

        total_rooms = int(request.POST['total_room'])
        room_types = request.POST.getlist('room_type[]')
        capacities = request.POST.getlist('capacity[]')
        prices = request.POST.getlist('price[]')
        room_images_list = request.FILES.getlist('room_images[]')
        for i in range(total_rooms):
            if i < len(room_types) and i < len(capacities) and i < len(prices):
                room_type = room_types[i]
                capacity = capacities[i]
                price = prices[i]
                room_number = f"Room {i+1}"  
                
                room = Rooms.objects.create(Room_type=room_type, Capacity=capacity, total_room=1, room_number=room_number, Price=price, R_id=a)
                if i < len(room_images_list):
                    room_image = room_images_list[i]
                    if room_image:
                        RoomImage.objects.create(image=room_image, room=room)


        
        return redirect('ownerresortview', id=id)

    else:
        return render(request, 'addresorts.html')

       
        # for i in range(total_rooms):
        #     room_type = room_types[i]
        #     capacity = capacities[i]
        #     price = prices[i]
        #     room_number = f"Room {i+1}"

            
        #     room = Rooms.objects.create(Room_type=room_type, Capacity=capacity, total_room=1, room_number=room_number, Price=price, R_id=a)
        #     room_image = room_images_list[i]
            
        #     if room_image:
        #        RoomImage.objects.create(image=room_image, room=room)



def ownerresortview(request, id):
    if request.user.is_authenticated:
        try:
            owner = Owner.objects.get(O_id=request.user)
            resorts = Resort.objects.filter(Own_id=owner)
            
            resort_data = []
            for resort in resorts:
                resort_images = ResortImage.objects.filter(resort=resort)
                rooms = Rooms.objects.filter(R_id=resort)
                room_data = []
                for room in rooms:
                    room_images = RoomImage.objects.filter(room=room)
                    room_data.append({'room': room, 'room_images': room_images})
                    
                resort_data.append({'resort': resort, 'resort_images': resort_images, 'rooms': room_data})

            return render(request, 'ownerresortview.html', {'owner': owner, 'resort_data': resort_data})
        
        except Owner.DoesNotExist:
            return HttpResponse("Owner not found")
    else:
        return HttpResponse("Authentication required")



def resortedit(request,owner_id,resort_id):
    if request.method=='POST':
        rname=request.POST['resort_name']
        lc=request.POST['location']
        cntry=request.POST['country']
        desc=request.POST['description']
        cnt=request.POST['contact']
        img_files =request.FILES.getlist('resort_images')
        
        
        edit = Resort.objects.get(id=resort_id)
        edit.Name=rname
        edit.Location=lc
        edit.Country=cntry
        edit.Description=desc
        edit.Contact=cnt
        edit.save()
        
        for img_file in img_files:
            ResortImage.objects.create(image=img_file, resort=edit)

    
        delete_resort_image_ids = request.POST.getlist('delete_images')
        for image_id in delete_resort_image_ids:
            try:
                image = ResortImage.objects.get(id=image_id)
                image.delete()
            except ResortImage.DoesNotExist:
                return HttpResponse("image does not exist")
        return redirect(ownerresortview, id=owner_id)
    else:
        try:
        
            
            owner = Owner.objects.get(id=owner_id)
            resorts = Resort.objects.filter(Own_id=owner)

            # get the specific resort to edit
            selected_resort = Resort.objects.get(id=resort_id)

            
            resort_images = ResortImage.objects.filter(resort=selected_resort)

            return render(request, 'ownerresortedit.html', {'owner': owner, 'resorts': resorts, 'selected_resort': selected_resort, 'resort_images': resort_images})
        except (Owner.DoesNotExist, Resort.DoesNotExist):
            return HttpResponse("Owner or resort not found")


def edit_room(request, room_id):
    if request.user.is_authenticated:
        try:
            room = Rooms.objects.get(id=room_id)
            if request.method == 'POST':
                pr = request.POST['price']
                total_room = request.POST['total_room']
                r_img_files = request.FILES.getlist('room_images')
                room.Price = pr
                room.total_room = total_room
                room.save()
                
               
                for r_img_file in r_img_files:
                    RoomImage.objects.create(image=r_img_file, room=room)

                # Delete selected images
                delete_image_ids = request.POST.getlist('delete_images')
                for image_id in delete_image_ids:
                    try:
                        image = RoomImage.objects.get(id=image_id)
                        image.delete()
                    except RoomImage.DoesNotExist:
                        pass
                    
                if room.R_id:
                    return redirect('ownerresortview', id=room.R_id.id)
            else:
                resort = room.R_id
                owner = resort.Own_id
                room_images = RoomImage.objects.filter(room=room)
                return render(request, 'ownerroomedit.html', {'owner': owner, 'resort': resort, 'room': room, 'room_images': room_images})
        except Rooms.DoesNotExist:
            return HttpResponse("Room not found")
    else:
        return HttpResponse("Authentication required")



def delete_resort_or_rooms(request):
    if request.user.is_authenticated:
        try:
            owner = Owner.objects.get(O_id=request.user)
            resorts = Resort.objects.filter(Own_id=owner)
            room_data = []

            for resort in resorts:
                
                rooms = Rooms.objects.filter(R_id=resort).select_related('R_id')
                room_data.append({'resort': resort, 'rooms': rooms})

            if request.method == 'POST':
                selected_resorts = request.POST.getlist('selected_resorts')
                selected_rooms = request.POST.getlist('selected_rooms')

                for resort_id in selected_resorts:
                    try:
                        resort = Resort.objects.get(id=resort_id, Own_id=owner)
                        resort.delete()
                    except Resort.DoesNotExist:
                        return HttpResponse(f"Resort with ID {resort_id} not found. Continuing with the next one.")

                for room_id in selected_rooms:
                    try:
                        room = Rooms.objects.get(id=room_id, R_id__Own_id=owner)
                        room.delete()
                    except Rooms.DoesNotExist:
                        return HttpResponse(f"Room with ID {room_id} not found. Continuing with the next one.")

                return HttpResponse("Selected resorts and rooms deleted successfully.")

            else:
                return render(request, 'ownerresortviewdelete.html', {'owner': owner, 'room_data': room_data})

        except Owner.DoesNotExist:
            return HttpResponse("Owner not found")
    else:
        return HttpResponse("Authentication required")

        

def adminresortview(request):
    resorts = Resort.objects.all()
    rooms = Rooms.objects.all()
    resort_images = ResortImage.objects.all()
    room_images = RoomImage.objects.all()
    return render(request, 'adminresortview.html', {'resorts': resorts, 'rooms': rooms, 'resort_images': resort_images, 'room_images': room_images})


def customer_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    location = request.GET.get('location')
    
    resorts = Resort.objects.all()

    if location:
        resorts = resorts.filter(Location=location)

    resort_images = ResortImage.objects.all()
    room_images = RoomImage.objects.all()

    resorts_data = {}

    for resort in resorts:
        resort_data = {
            'resort': resort,
            'images': resort_images.filter(resort=resort)
        }

        rooms = Rooms.objects.filter(R_id=resort)
        rooms_data = {}

        if rooms.exists():
            for room in rooms:
                room_data = {
                    'room': room,
                    'images': room_images.filter(room=room)
                }
                rooms_data[room] = room_data

        resort_data['rooms'] = rooms_data
        resorts_data[resort] = resort_data

    return render(request, 'customerhome.html', {'resorts_data': resorts_data, 'customer': customer})


def logouts(request):
     logout(request)
     return redirect(logins) 