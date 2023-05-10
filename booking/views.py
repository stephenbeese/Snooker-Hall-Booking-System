from django.shortcuts import render
from django.views import generic
from .models import Testimonial


class TestimonialList(generic.ListView):
    model = Testimonial
    queryset = Testimonial.objects.filter(approved=True).order_by('-created_on')
    template_name = 'index.html'
