from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Working"), (1, "Maintenance"))
GAME = ((0, "Snooker"), (1, "English Pool"), (2, "American Pool"))


class GameTable(models.Model):
    table_number = models.IntegerField(primary_key=True)
    game_type = models.IntegerField(choices=GAME)
    available_from = models.TimeField()
    available_to = models.TimeField()
    price = models.FloatField()
    status = models.IntegerField(choices=STATUS, default=0)
    image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ['-game_type']

    def __str__(self):
        if self.game_type == 0:
            return f"Snooker table number: {self.table_number}, status: {self.status}"
        elif self.game_type == 1:
            return f"English Pool table number: {self.table_number}, status: {self.status}"
        else:
            return f"American table number: {self.table_number}, status: {self.status}"


class Reservation(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    table_number = models.ForeignKey(GameTable(), on_delete=models.CASCADE, related_name="table_bookings")
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
