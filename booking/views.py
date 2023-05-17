from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Testimonial
from .forms import TestimonialForm


class Home(generic.ListView):
    model = Testimonial
    queryset = Testimonial.objects.filter(approved=True).order_by('-created_on')
    template_name = 'index.html'


class Testimonial(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "review.html",
            {
                "reviewed": False,
                "testimonial_form": TestimonialForm()
            },
        )

    def post(self, request, *args, **kwargs):
        testimonial_form = TestimonialForm(request.POST)

        if testimonial_form.is_valid():
            testimonial_form.user_id = request.user.username
            review = testimonial_form.save(commit=False)
            review.user_id = request.user
            review.save()
        else:
            testimonial_form = TestimonialForm()

        return render(
            request,
            "review.html",
            {
                "reviewed": True,
                "testimonial_form": testimonial_form
            },
        )
