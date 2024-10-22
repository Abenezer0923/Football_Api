from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Item

# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'password1', 'password2')


# Custom Authentication Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


# Item Form for CRUD operations
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item  # Assuming there is an Item model defined in models.py
        fields = ['name', 'description']  # Adjust the fields according to the Item model's fields

