from django import forms
from django.utils import timezone
from .models import Testimonial, Reservation, GameTable


class TestimonialForm(forms.ModelForm):
    """
    Testimonial Form is the form so a user can submit a testimonial.
    """
    class Meta:
        model = Testimonial
        fields = ('comment',)


class ReservationForm(forms.ModelForm):
    """
    Reservation Form is the main form for a user to create a booking.
    """
    # Filters Working tables
    table_number = forms.ModelChoiceField(
        queryset=GameTable.objects.filter(status=0),
    )

    class Meta:
        """
        Meta class sets fields for the From and sets widgets for the date,
        start time and end time
        """
        model = Reservation
        fields = ('table_number', 'name', 'date', 'start_time', 'end_time',)
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': timezone.now().date()}),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'value': '11:00',
                    'min': '11:00',
                    'max': '22:00'}),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                            'value': '23:00',
                            'min': '12:00',
                            'max': '23:00'})}
