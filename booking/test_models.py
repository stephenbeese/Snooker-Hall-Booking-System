"""Imports for the model tests"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import GameTable, Reservation, Testimonial


class GameTableTestCase(TestCase):
    """
    Test case for the GameTable model.

    This test case verifies the behavior and functionality of the GameTable
    model, including its field values, string representation, and ordering
    """

    def setUp(self):
        self.table1 = GameTable.objects.create(
            table_number=1,
            game_type=0,
            available_from='11:00:00',
            available_to='23:00:00',
            price=10.0,
            status=0,
            image='placeholder'
        )
        self.table2 = GameTable.objects.create(
            table_number=2,
            game_type=1,
            available_from='11:00:00',
            available_to='23:00:00',
            price=15.0,
            status=1,
            image='placeholder'
        )

    def test_table_str_representation(self):
        """
        Test the string representation of GameTable objects when ordered in
        ascending order of table_number.

        The table representation should match the expected format
        "{table_number} - {game_type}".
        """
        tables = GameTable.objects.order_by('table_number')
        self.assertEqual(str(tables[0]), '1 - Snooker')
        self.assertEqual(str(tables[1]), '2 - English Pool')

    def test_table_fields(self):
        """
        Test the values of various fields of GameTable objects.
        Each field should have the expected value as set in the setUp method.
        """
        self.assertEqual(self.table1.table_number, 1)
        self.assertEqual(self.table1.game_type, 0)
        self.assertEqual(self.table1.available_from, '11:00:00')
        self.assertEqual(self.table2.available_to, '23:00:00')
        self.assertEqual(self.table1.price, 10.0)
        self.assertEqual(self.table1.status, 0)
        self.assertEqual(self.table1.image, 'placeholder')

        self.assertEqual(self.table2.table_number, 2)
        self.assertEqual(self.table2.game_type, 1)
        self.assertEqual(self.table2.available_from, '11:00:00')
        self.assertEqual(self.table2.available_to, '23:00:00')
        self.assertEqual(self.table2.price, 15.0)
        self.assertEqual(self.table2.status, 1)
        self.assertEqual(self.table2.image, 'placeholder')


class ReservationTestCase(TestCase):
    """
    Test case for the Reservation model

    This test case verifies the behavior and functionality of the Reservation
    model. It includes test methods to ensure the creation of Reservation
    objects and the validation logic implemented in the clean method of the
    Reservation model.
    """

    def setUp(self):
        self.table1 = GameTable.objects.create(
            table_number=1,
            game_type=0,
            available_from='09:00',
            available_to='21:00',
            price=10.0,
            status=0,
            image='placeholder'
        )

    def test_reservation_creation(self):
        """
        Test the creation of a Reservation object.
        """
        # Create a User instance for the reservation
        user = User.objects.create(username="john_doe")

        _ = Reservation.objects.create(
            user_id=user,
            table_number=self.table1,
            name="John Doe",
            date="2023-05-29",
            start_time='10:00',
            end_time='11:00',
            total_price=10.0
        )

    def test_reservation_clean_method(self):
        """
        Test the clean method of the Reservation model.

        This test case verifies the clean method of the Reservation model
        by creating conflicting reservations and reservations with invalid
        time ranges. It asserts that the expected ValidationError is raised
        when attempting to save the conflicting or invalid reservations.
        """
        user1 = User.objects.create(username="john_doe")
        user2 = User.objects.create(username="jane_smith")

        # reservation1
        _ = Reservation.objects.create(
            user_id=user1,
            table_number=self.table1,
            name="John Doe",
            date="2023-05-29",
            start_time='10:00',
            end_time='11:00',
            total_price=10.0
        )

        # Create a conflicting reservation with overlapping time
        conflicting_reservation = Reservation(
            user_id=user2,
            table_number=self.table1,
            name="Jane Smith",
            date="2023-05-29",
            start_time='10:30',
            end_time='11:30',
            total_price=10.0
        )
        with self.assertRaises(ValidationError):
            conflicting_reservation.clean()

        # Create a reservation with end time earlier than start time
        invalid_reservation = Reservation(
            user_id=user1,
            table_number=self.table1,
            name="Alice Johnson",
            date="2023-05-29",
            start_time='12:00',
            end_time='11:00',
            total_price=10.0
        )
        with self.assertRaises(ValidationError):
            invalid_reservation.clean()


class TestimonialTestCase(TestCase):
    """
    Test case for the Testimonial model.

    This test case verifies the behavior and functionality of the Testimonial
    model. It includes test methods to ensure the string representation,
    approval status, and ordering of testimonials based on their created_on
    date.
    """

    def setUp(self):
        self.user = User.objects.create(username="john_doe")
        self.testimonial = Testimonial.objects.create(
            user_id=self.user,
            name="John Doe",
            comment="This is a great place!",
            approved=True
        )

    def test_testimonial_str_representation(self):
        """
        This test case verifies that the string representation of
        a Testimonial object returns the expected value.
        """
        expected_string = f"Comment: {self.testimonial.comment} by {self.testimonial.name}"
        self.assertEqual(str(self.testimonial), expected_string)

    def test_testimonial_approval_status(self):
        """
        This test case verifies that the approval status of a
        Testimonial object is correctly set and retrieved.
        """
        self.assertTrue(self.testimonial.approved)

    def test_testimonial_ordering(self):
        """
        This test case verifies that the testimonials are ordered
        correctly based on their created_on date.
        """
        testimonial2 = Testimonial.objects.create(
            user_id=self.user,
            name="John Doe",
            comment="Another testimonial",
            approved=True
        )
        testimonial3 = Testimonial.objects.create(
            user_id=self.user,
            name="John Doe",
            comment="Yet another testimonial",
            approved=True
        )

        testimonials = Testimonial.objects.all()
        expected_order = [testimonial3, testimonial2, self.testimonial]
        self.assertEqual(list(testimonials), expected_order)
