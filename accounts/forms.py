from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Order, Customer


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-sm'}))
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-sm'}))
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control-sm'}))
    password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control-sm'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already in use")
        return data


class OrderForm(ModelForm):
    
    class Meta:
        model = Order
        fields = ('product', 'status')


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['date_created', 'user']