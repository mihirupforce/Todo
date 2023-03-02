from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UsernameField


class DateSearch(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if (start_date and end_date) and (start_date > end_date):
            raise forms.ValidationError(
                "Start date should be smaller than end date")


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
