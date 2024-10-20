from django.urls import path
from customer import views

urlpatterns = [
  
    path('',views.customer_reg,name='customer_reg'),
    path('customer_booking/<int:resort_id>/<int:customer_id>/<int:room_id>/',views.customer_booking,name='customer_booking'),
    path('owner_booking_view',views.owner_booking_view,name='owner_booking_view'),
    path('about',views.about,name='about'),
    path('blog',views.blog,name='blog'),
    path('contact',views.contact,name='contact'),
    path('gallery',views.gallery,name='gallery'),
    path('room',views.room,name='room'),
]