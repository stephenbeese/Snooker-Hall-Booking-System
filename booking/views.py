from datetime import datetime
from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Testimonial, GameTable, Reservation
from .forms import TestimonialForm, ReservationForm


class Home(generic.ListView):
    model = Testimonial
    queryset = Testimonial.objects.filter(approved=True).order_by('-created_on')
    template_name = 'index.html'


class Testimonial(View):
    def get(self, request):
        return render(
            request,
            "review.html",
            {
                "reviewed": False,
                "testimonial_form": TestimonialForm()
            },
        )

    def post(self, request):
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


class GameTables(generic.ListView):
    model = GameTable
    template_name = 'tables.html'
    context_object_name = 'tables'
    ordering = 'table_number'


class ReservationView(View):
    def get(self, request):
        form = ReservationForm()
        game_tables = GameTable.objects.all()
        context = {
            'form': form,
            'game_tables': game_tables
        }
        return render(request, 'reservation.html', context)

    def post(self, request):
        form = ReservationForm(request.POST)
        game_tables = GameTable.objects.all()
        context = {
            'form': form,
            'game_tables': game_tables
        }

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            game_table = form.cleaned_data.get('table_number')
            reservation.table_number = game_table

            # calculate total_price
            start_time = datetime.combine(datetime.today(), reservation.start_time)
            end_time = datetime.combine(datetime.today(), reservation.end_time)
            time_difference = end_time - start_time
            total_price = (time_difference.total_seconds() / 3600) * game_table.price
            reservation.total_price = total_price

            form.save()
            return redirect('bookings')

        return render(request, 'reservation.html', context)


class UserBookings(generic.ListView):
    model = Reservation
    template_name = 'bookings.html'
    context_object_name = 'bookings'
    ordering = 'date'
