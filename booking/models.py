from django.db import models
from django.core.exceptions import ValidationError
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
        ordering = ['-table_number']

    def __str__(self):
        if self.game_type == 0:
            return f"{self.table_number} - Snooker"
        elif self.game_type == 1:
            return f"{self.table_number} - English Pool"
        else:
            return f"{self.table_number} - American Pool"


class Reservation(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    table_number = models.ForeignKey(GameTable, on_delete=models.CASCADE, related_name="table_bookings")
    name = models.CharField(max_length=40)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_price = models.DecimalField(decimal_places=2, max_digits=5)

    class Meta:
        ordering = ['-date']

    def clean(self):
        # Check if the end time is earlier than or equal to the start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time should be later than the start time.")

        # Check if there are any existing reservations with overlapping times on the same table
        conflicting_reservations = Reservation.objects.filter(
            table_number=self.table_number,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        if conflicting_reservations.exists():
            raise ValidationError("This table is already booked for the selected time. Please try a different table.")

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
