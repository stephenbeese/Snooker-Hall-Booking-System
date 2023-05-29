from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views


class UrlsTestCase(SimpleTestCase):
    """
    Test case for URL configurations.

    This test case verifies the correctness of the URL patterns and their
    associated view functions or classes.
    """

    def test_home_url(self):
        """
        Test the home URL pattern.

        This test case verifies that the home URL pattern resolves to the
        correct view class.
        """
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, views.Home)

    def test_review_url(self):
        """
        Test the review URL pattern.

        This test case verifies that the review URL pattern resolves to the
        correct view class.
        """
        url = reverse('review')
        self.assertEqual(resolve(url).func.view_class, views.TestimonialView)

    def test_tables_url(self):
        """
        Test the tables URL pattern.

        This test case verifies that the tables URL pattern resolves to the
        correct view class.
        """
        url = reverse('tables')
        self.assertEqual(resolve(url).func.view_class, views.GameTables)

    def test_reservation_url(self):
        """
        Test the reservation URL pattern.

        This test case verifies that the reservation URL pattern resolves to
        the correct view class.
        """
        url = reverse('reservation')
        self.assertEqual(resolve(url).func.view_class, views.ReservationView)

    def test_bookings_url(self):
        """
        Test the bookings URL pattern.

        This test case verifies that the bookings URL pattern resolves to the
        correct view class.
        """
        url = reverse('bookings')
        self.assertEqual(resolve(url).func.view_class, views.UserBookings)

    def test_edit_booking_url(self):
        """
        Test the edit_booking URL pattern.

        This test case verifies that the edit_booking URL pattern resolves to
        the correct view class.
        """
        booking_id = 1
        url = reverse('edit_booking', args=[booking_id])
        self.assertEqual(resolve(url).func.view_class, views.EditBooking)

    def test_confirm_delete_url(self):
        """
        Test the confirm_delete URL pattern.

        This test case verifies that the confirm_delete URL pattern resolves
        to the correct view class.
        """
        booking_id = 1
        url = reverse('confirm_delete', args=[booking_id])
        self.assertEqual(resolve(url).func.view_class, views.ConfirmDelete)

    def test_delete_booking_url(self):
        """
        Test the delete_booking URL pattern.

        This test case verifies that the delete_booking URL pattern resolves
        to the correct view class.
        """
        booking_id = 1
        url = reverse('delete_booking', args=[booking_id])
        self.assertEqual(resolve(url).func.view_class, views.DeleteBooking)
