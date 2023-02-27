from django import forms

class DateSearch(forms.Form):
    start_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
