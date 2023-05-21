from django import forms
from django.utils import timezone
from .models import Testimonial, Reservation


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('comment',)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('table_number', 'name', 'date', 'start_time', 'end_time',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'value': '11:00'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'value': '23:00'})
        }
