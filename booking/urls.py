from . import views
from django.urls import path

urlpatterns = [
    path('', views.TestimonialList.as_view(), name='home')
]
