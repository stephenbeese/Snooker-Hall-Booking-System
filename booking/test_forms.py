from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .forms import TestimonialForm, ReservationForm
from .models import Testimonial, GameTable, Reservation


class TestimonialFormTest(TestCase):
    user = None

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data required for the TestimonialFormTest class.

        This method creates a User object with a username and password.
        The created user will be used in the test methods.
        """
        cls.user = User.objects.create(
            username='testuser',
            password='testpassword'
        )

    def test_form_fields(self):
        """
        Test the fields of the TestimonialForm.

        This method asserts that the Meta model of the TestimonialForm is set to the Testimonial model.
        It also asserts that the Meta fields of the form include only the 'comment' field.
        """
        form = TestimonialForm()
        self.assertEqual(
            form.Meta.model,
            Testimonial,
            "The form's Meta model should be set to the Testimonial model."
        )
        self.assertEqual(
            form.Meta.fields,
            ('comment',),
            "The form's Meta fields should include only the 'comment' field."
        )

    def test_valid_form(self):
        """
        Test a valid TestimonialForm.

        This method creates a TestimonialForm with valid data and asserts that it is considered valid.
        """
        form_data = {
            'comment': 'This is a test comment.',
        }
        form = TestimonialForm(data=form_data)
        self.assertTrue(form.is_valid(), "The form should be valid with valid data.")

    def test_invalid_form(self):
        """
        Test an invalid TestimonialForm.

        This method creates a TestimonialForm with an empty comment and asserts that it is considered invalid.
        """
        form_data = {
            'comment': '',
        }
        form = TestimonialForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid with empty comment.")

    def test_save_form(self):
        """
        Test saving a TestimonialForm.

        This method creates a TestimonialForm with valid data, associates it with the user,
        saves the form, and then asserts the correctness of the saved Testimonial object.
        """
        form_data = {
            'comment': 'This is a test comment.',
        }
        form = TestimonialForm(data=form_data)
        form.instance.user_id = self.user
        testimonial = form.save()
        self.assertIsInstance(testimonial, Testimonial, "The form should save a Testimonial object.")
        self.assertEqual(testimonial.comment, form_data['comment'], "The saved Testimonial's comment should match the form data.")
        self.assertEqual(testimonial.user_id, self.user, "The saved Testimonial should be associated with the user.")


class ReservationFormTest(TestCase):
    """
    Test case for the ReservationForm.

    This test case class contains tests to verify the behavior and validation
    of the ReservationForm. It includes tests for valid and invalid form
    submissions, as well as the queryset filter of the table_number field.
    """

    def setUp(self):
        self.table = GameTable.objects.create(
            table_number=1,
            game_type=0,
            available_from='11:00:00',
            available_to='23:00:00',
            price=10.0,
            status=0,
            image='placeholder'
        )

    def test_valid_form(self):
        """
        Test a valid ReservationForm.

        This method creates a ReservationForm with valid data and asserts that it is considered valid.
        """
        form_data = {
            'table_number': self.table.pk,
            'name': 'John Doe',
            'date': "2023-05-29",
            'start_time': '11:00',
            'end_time': '12:00',
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid(), "The form should be valid with valid data.")

    def test_invalid_form(self):
        """
        Test an invalid ReservationForm.

        This method creates a ReservationForm with invalid data and asserts that it is considered invalid.
        """
        form_data = {
            'table_number': None,  # Invalid table number
            'name': '',
            'date': timezone.now().date(),
            'start_time': '10:00',  # Invalid start time
            'end_time': '09:00',  # Invalid end time
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid(), "The form should be invalid with invalid data.")

    def test_table_number_filter(self):
        """
        Test the table_number queryset filter of the ReservationForm.

        This method asserts that the table_number field of the form only
        includes working tables (status=0).
        """
        # Create non-working table
        non_working_table = GameTable.objects.create(
            table_number=2,
            game_type=0,
            available_from='11:00:00',
            available_to='23:00:00',
            price=10.0,
            status=1,
            image='placeholder'
        )

        form = ReservationForm()
        queryset = form.fields['table_number'].queryset
        self.assertIn(self.table, queryset, "The queryset should include working tables.")
        self.assertNotIn(non_working_table, queryset, "The queryset should exclude non-working tables.")
