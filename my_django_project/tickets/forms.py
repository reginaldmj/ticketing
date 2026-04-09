from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyTicket, MyUser


class TicketForm(forms.ModelForm):
    """
    ModelForm for creating and editing MyTicket instances.
    We exclude 'creator' because it's set automatically in the view.
    """
    class Meta:
        model  = MyTicket
        fields = ['title', 'description', 'status', 'user_assigned_to', 'user_who_completed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make completion field optional
        self.fields['user_who_completed'].required = False
        self.fields['user_assigned_to'].required   = False

class SignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password','display_name', 'age']


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username', 'display_name', 'age')


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('username', 'display_name', 'age', 'is_active', 'is_staff')