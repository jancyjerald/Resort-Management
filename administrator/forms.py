from django import forms
from administrator.models import Resort,Rooms,Owner

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=Owner
        fields='__all__'
class ResortForm(forms.ModelForm):
    class Meta:
        model = Resort
        fields = ['Name', 'Location', 'Country', 'Description', 'Contact']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['Room_status','Room_type', 'Capacity', 'Price']

