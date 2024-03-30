from django import forms
from .models import User_profile, debt

from django.contrib.auth.forms import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User_profile
        fields = ['personal_id']


class paymentForm(forms.Form):
    amount = forms.DecimalField()

class AddDebtForm(forms.ModelForm):
    class Meta:
        model = debt
        fields = ['amount']