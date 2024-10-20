from django.urls import path
from administrator import views
# from .import*
urlpatterns = [
    path('',views.Home,name='Home'),
    path('ad',views.adminpage,name='adminpage'),
    path('re',views.register_owner,name='register_owner'),
    path('log',views.logins,name='logins'),
    path('reresort/<int:id>',views.registerresort,name='registerresort'),
    path('add/<int:id>',views.addresorts,name='addresorts'),
    path('adminview',views.adminresortview,name='adminresortview'),
    path('ownerviews/<int:id>', views.ownerresortview, name='ownerresortview'),
    path('editresort/<int:owner_id>/<int:resort_id>/', views.resortedit, name='resortedit'),
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete/', views.delete_resort_or_rooms, name='delete_resort_or_rooms'),
    path('logout',views.logouts,name='logouts'),
    path('approve/', views.approve_owner, name='approve_owner'),
    path('owner-approve/<int:owner_approve_id>/', views.owner_approve, name='owner_approve'),
    path('owner-reject/<int:owner_approve_id>/', views.owner_reject, name='owner_reject'),
    path('customer_view/<int:customer_id>/',views.customer_view, name='customer_view'),
   

    
]
