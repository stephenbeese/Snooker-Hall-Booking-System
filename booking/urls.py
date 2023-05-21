from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('review/', views.Testimonial.as_view(), name='review'),
    path('tables/', views.GameTables.as_view(), name='tables'),
    path('reservation/', views.ReservationView.as_view(), name='reservation')
]
