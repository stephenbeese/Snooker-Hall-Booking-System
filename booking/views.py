from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django import template
from .models import Testimonial, GameTable, Reservation
from .forms import TestimonialForm, ReservationForm

register = template.Library()


class Home(generic.ListView):
    """
    View for the home page.

    Displays a list of approved testimonials on the home page.
    """
    model = Testimonial
    queryset = Testimonial.objects.filter(
        approved=True).order_by('-created_on')
    template_name = 'index.html'


class TestimonialView(View):
    """Allows users to submit testimonials through a form"""

    def get(self, request):
        """
        Handle GET request for submitting a testimonial.

        Renders the testimonial submission form
        """
        return render(
            request,
            "review.html",
            {
                "reviewed": False,
                "testimonial_form": TestimonialForm()
            },
        )

    def post(self, request):
        """
        Handle POST request for submitting a testimonial.

        Saves the submitted testimonial if it is valid.
        """
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
    """
    View for displaying game tables.

    Lists all game tables in the database.
    """
    model = GameTable
    template_name = 'tables.html'
    context_object_name = 'tables'
    ordering = 'table_number'


class ReservationView(View):
    """
    View for making reservations.

    Allows users to make reservations through a form.
    """

    def get(self, request):
        """
        Handle GET request for making a reservation.

        Renders the reservation form.
        """
        form = ReservationForm(
            initial={
                'start_time': '11:00',
                'end_time': '23:00'})
        game_tables = GameTable.objects.all()
        context = {
            'form': form,
            'game_tables': game_tables
        }
        return render(request, 'reservation.html', context)

    def post(self, request):
        """
        Handle POST request for making a reservation.

        Saves the reservation if it is valid and performs custom validation to
        prevent conflicting reservations.
        """
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
            start_time = datetime.combine(
                datetime.today(), reservation.start_time)
            end_time = datetime.combine(datetime.today(), reservation.end_time)
            time_difference = end_time - start_time
            total_price = (time_difference.total_seconds() /
                           3600) * game_table.price
            reservation.total_price = total_price

            # Custom validation to prevent user booking two tables at
            # conflicting times
            conflicting_user_reservations = Reservation.objects.filter(
                user_id=request.user,
                date=reservation.date,
                start_time__lt=reservation.end_time,
                end_time__gt=reservation.start_time
            ).exclude(pk=reservation.pk)

            if conflicting_user_reservations.exists():
                form.add_error(
                    None,
                    "You have already booked another table for the selected \
                     time. Please select a different date/time")
                return render(request, 'reservation.html', context)

            form.save()
            return redirect('bookings')

        return render(request, 'reservation.html', context)


class UserBookings(generic.ListView):
    """
    View for displaying user bookings.

    Lists the past and future bookings of the authenticated user.
    """
    model = Reservation
    template_name = 'bookings.html'
    context_object_name = 'past_bookings'

    def get_queryset(self):
        """
        Get the queryset for past bookings.

        Returns a queryset of past bookings for the authenticated user.
        """
        today = date.today()
        if self.request.user.is_authenticated:
            user_bookings = Reservation.objects.filter(
                user_id=self.request.user)
            past_bookings = user_bookings.filter(
                date__lt=today).order_by('-date')
            return past_bookings

    def get_context_data(self, **kwargs):
        """
        Get additional context data.

        Adds the future bookings to the context data.
        """
        context = super().get_context_data(**kwargs)
        today = date.today()
        if self.request.user.is_authenticated:
            user_bookings = Reservation.objects.filter(
                user_id=self.request.user)
            context['future_bookings'] = user_bookings.filter(
                date__gte=today).order_by('date')
        return context


class EditBooking(View):
    """
    View for editing a booking.

    Allows users to edit an existing booking.
    """

    def get(self, request, booking_id):
        """
        Handle GET request for editing a booking.

        Renders the booking edit form.
        """
        booking = get_object_or_404(Reservation, booking_id=booking_id)
        form = ReservationForm(instance=booking)
        context = {
            'form': form,
            'booking': booking
        }
        return render(request, 'edit_booking.html', context)

    def post(self, request, booking_id):
        """
        Handle POST request for editing a booking.

        Saves the edited booking if it is valid.
        """
        booking = get_object_or_404(Reservation, booking_id=booking_id)
        form = ReservationForm(request.POST, instance=booking)
        context = {
            'form': form
        }
        if form.is_valid():
            reservation = form.save(commit=False)
            game_table = form.cleaned_data.get('table_number')
            reservation.table_number = game_table

            # calculate total_price
            start_time = datetime.combine(
                datetime.today(), reservation.start_time)
            end_time = datetime.combine(datetime.today(), reservation.end_time)
            time_difference = end_time - start_time
            total_price = (time_difference.total_seconds() /
                           3600) * game_table.price
            reservation.total_price = total_price

            # Custom validation to prevent user booking two tables at
            # conflicting times
            conflicting_user_reservations = Reservation.objects.filter(
                user_id=request.user,
                date=reservation.date,
                start_time__lt=reservation.end_time,
                end_time__gt=reservation.start_time
            ).exclude(pk=reservation.pk)

            if conflicting_user_reservations.exists():
                form.add_error(
                    None,
                    "You have already booked another table for the selected \
                     time. Please select a different date/time")
                return render(request, 'reservation.html', context)

            form.save()
            return redirect('bookings')
        else:
            print(form.errors)
        return render(request, 'edit_booking.html', context)


class ConfirmDelete(View):
    """
    View for confirming booking deletion.

    Displays a confirmation page before deleting a booking.
    """

    def get(self, request, booking_id):
        """
        Handle GET request for confirming booking deletion.

        Renders the confirmation page.
        """
        booking = get_object_or_404(Reservation, booking_id=booking_id)
        context = {'booking': booking}
        return render(request, 'confirm_delete.html', context)


class DeleteBooking(View):
    """
    View for deleting a booking.

    Deletes a booking and redirects to the bookings page.
    """

    def get(self, request, booking_id):
        """
        Handle GET request for deleting a booking.

        Renders the confirmation page.
        """
        booking = get_object_or_404(Reservation, booking_id=booking_id)
        context = {'booking': booking}
        return render(request, 'confirm_delete.html', context)

    def post(self, request, booking_id):
        """
        Handle POST request for deleting a booking.

        Deletes the booking and redirects to the bookings page.
        """
        booking = get_object_or_404(Reservation, booking_id=booking_id)
        booking.delete()
        return redirect('bookings')
