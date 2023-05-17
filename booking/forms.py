from .models import Testimonial
from django import forms


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('comment',)
