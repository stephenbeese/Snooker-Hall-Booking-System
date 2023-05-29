"""Imports for the views tests"""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .views import Home, GameTables
from .models import Testimonial, GameTable


class HomeViewTestCase(TestCase):
    """
    Test case for the Home view.

    This test case verifies the behavior and functionality of the Home view.
    It includes test methods to ensure that the view renders the correct
    template, retrieves the appropriate testimonials, and orders them by
    their created_on date.
    """
    def setUp(self):
        # Create a User instance for the testimonial
        user1 = User.objects.create(username="john_doe")
        user2 = User.objects.create(username="jane_smith")
        user3 = User.objects.create(username="alice_johnson")

        self.testimonial1 = Testimonial.objects.create(
            user_id=user1,
            name="John Doe",
            comment="This is a great place!",
            created_on=timezone.now(),
            approved=True
        )
        self.testimonial2 = Testimonial.objects.create(
            user_id=user2,
            name="Jane Smith",
            comment="Amazing experience!",
            created_on=timezone.now(),
            approved=True
        )

        self.testimonial3 = Testimonial.objects.create(
            user_id=user3,
            name="Alice Johnson",
            comment="Not a good experience.",
            created_on=timezone.now(),
            approved=False
        )

    def test_home_view_template(self):
        """
        Test the template used by the Home view.

        This test case verifies that the Home view uses the correct template
        to render the response.
        """
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")

    def test_home_view_testimonials(self):
        """
        Test the testimonials retrieved by the Home view.

        This test case verifies that the Home view retrieves the appropriate
        testimonials and passes them to the template context.
        """
        response = self.client.get(reverse("home"))
        testimonials = response.context["object_list"]
        self.assertQuerysetEqual(
            testimonials, [repr(self.testimonial1), repr(self.testimonial2)], ordered=False
        )

    def test_home_view_ordering(self):
        """
        Test the ordering of testimonials by created_on date.

        This test case verifies that the testimonials displayed by the Home
        view are ordered correctly based on their created_on date.
        """
        response = self.client.get(reverse("home"))
        testimonials = response.context["object_list"]
        self.assertEqual(
            list(testimonials), [self.testimonial2, self.testimonial1]
        )

    def test_home_view_approved_false_testimonial(self):
        """
        Test the display of a testimonial with approved=False.

        This test case verifies that a testimonial with approved=False is not
        displayed by the Home view.
        """
        response = self.client.get(reverse("home"))
        testimonials = response.context["object_list"]
        self.assertNotIn(self.testimonial3, testimonials)


class GameTablesViewTestCase(TestCase):
    """
    Test case for the GameTables view.
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
            price=5.50,
            status=1,
            image='placeholder'
        )
        self.table3 = GameTable.objects.create(
            table_number=3,
            game_type=2,
            available_from='11:00:00',
            available_to='23:00:00',
            price=7.50,
            status=1,
            image='placeholder'
        )

    def test_view_template(self):
        """
        Test the template used by the GameTables view.

        This test case verifies that the GameTables view uses the correct
        template to render the response.
        """
        response = self.client.get(reverse("tables"))
        self.assertTemplateUsed(response, "tables.html")

    def test_view_context(self):
        """
        Test the context of the GameTables view.

        This test case verifies that the GameTables view passes the correct
        context data to the template.
        """
        response = self.client.get(reverse("tables"))
        tables = response.context["tables"]

        self.assertEqual(len(tables), 3)
        self.assertIn(self.table1, tables)
        self.assertIn(self.table2, tables)
        self.assertIn(self.table3, tables)

    def test_view_ordering(self):
        """
        Test the ordering of game tables in the GameTables view.

        This test case verifies that the game tables are ordered correctly
        based on the table_number field.
        """
        response = self.client.get(reverse("tables"))
        tables = response.context["tables"]

        table_numbers = [table.table_number for table in tables]

        self.assertEqual(table_numbers, [1, 2, 3])
