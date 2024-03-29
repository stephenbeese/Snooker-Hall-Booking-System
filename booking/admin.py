from django.contrib import admin
from .models import GameTable, Reservation, Testimonial


@admin.register(GameTable)
class GameTableAdmin(admin.ModelAdmin):
    """
    Admin Display for the GameTable Model
    """
    list_display = (
        'table_number',
        'game_type',
        'available_from',
        'available_to',
        'price',
        'status')
    list_filter = ('game_type', 'status')
    search_fields = ['game_type']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin Display for the Reservation Model
    """
    list_display = (
        'booking_id',
        'table_number',
        'user_id',
        'name',
        'date',
        'start_time',
        'end_time',
        'total_price')
    list_filter = ('date', 'start_time', 'end_time')
    search_fields = ['name', 'date']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin Display for the Testimonial Model
    """
    list_filter = ('created_on', 'approved')
    list_display = ('user_id', 'name', 'comment', 'created_on', 'approved')
    search_fields = ['name', 'comment']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
