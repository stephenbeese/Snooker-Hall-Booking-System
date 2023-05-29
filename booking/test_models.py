from django.test import TestCase
from django.contrib.auth.models import User
from .models import GameTable, Reservation


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_game_table_str(self):
        game_table = GameTable.objects.create(
            table_number=1,
            game_type=0,
            available_from='11:00:00',
            available_to='23:00:00',
            price=10.00
        )
        self.assertEqual(str(game_table), "1 - Snooker")

    def test_reservation_str(self):
        reservation = Reservation.objects.create(
            booking_id=1,
            user_id=self.user,
            table_number=test_game_table_str(),
            name='John Doe',
            date='June 10, 2023',
            start_time='11:00:00',
            end_time='13:00:00',
            total_price=20,
        )
        self.assertEqual(str(Reservation), "Booked by John Doe for June 10, 2023 at {11:00:00")
