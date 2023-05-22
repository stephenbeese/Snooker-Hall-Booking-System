from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('review/', views.Testimonial.as_view(), name='review'),
    path('tables/', views.GameTables.as_view(), name='tables'),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
    path('my_bookings/', views.UserBookings.as_view(), name='bookings'),
    path('edit_booking/<booking_id>', views.EditBooking.as_view(), name='edit_booking'),
]
