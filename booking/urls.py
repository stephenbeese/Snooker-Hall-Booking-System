from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.Home.as_view(),
        name='home'),
    path(
        'review/',
        views.TestimonialView.as_view(),
        name='review'),
    path(
        'tables/',
        views.GameTables.as_view(),
        name='tables'),
    path(
        'reservation/',
        views.ReservationView.as_view(),
        name='reservation'),
    path(
        'my_bookings/',
        views.UserBookings.as_view(),
        name='bookings'),
    path(
        'edit_booking/<int:booking_id>',
        views.EditBooking.as_view(),
        name='edit_booking'),
    path(
        'bookings/<int:booking_id>/confirm_delete',
        views.ConfirmDelete.as_view(),
        name='confirm_delete'),
    path(
        'bookings/<int:booking_id>/delete',
        views.DeleteBooking.as_view(),
        name='delete_booking'),
]
