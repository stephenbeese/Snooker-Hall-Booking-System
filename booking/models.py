from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# SNOOKER = 0
# EN_POOL = 1
# AM_POOL = 2

STATUS = ((0, "Working"), (1, "Maintenance"))
GAME = ((0, "Snooker"), (1, "English Pool"), (2, "American Pool"))


class GameTable(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_type = models.IntegerField(choices=GAME)
    available_from = models.TimeField()
    available_to = models.TimeField()
    price = models.IntegerField()
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-game_type']

    def __str__(self):
        if self.game_type == 0:
            return f"Snooker table, ID: {self.game_id}, status: {self.status}"
        elif self.game_type == 1:
            return f"English Pool table, ID: {self.game_id}, status: {self.status}"
        else:
            return f"American table, ID: {self.game_id}, status: {self.status}"


class Reservation(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    game_id = models.ForeignKey(GameTable(), on_delete=models.CASCADE, related_name="table_bookings")
    name = models.CharField(max_length=40)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.IntegerField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Booked by {self.name} for {self.date} at {self.start_time}"


class Testimonial(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="testimonials")
    name = models.CharField(max_length=40)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Comment: {self.comment} by {self.name}"


class DateOfBirth(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="birth_date")
    birth_date = models.DateField()

    class Meta:
        ordering = ['-user_id']

    def __str__(self):
        return f"User {self.user_id}'s birthday is {self.birth_date}"
