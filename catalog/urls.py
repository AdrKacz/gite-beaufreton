from django.urls import path

from . import views

urlpatterns = [
	# The main mage (first page)
	path('', views.index, name='index'),

	# The detail page (second page)
	path('home-details/', views.details, name="home-details"),

	# The booking page (third page)
	path('booking/', views.booking, name="booking"),

	# Intern fetch reservation
	path('reservation-dates/', views.reservation_dates, name="reservation-dates"),

	# Get Reservation (for Airbnb and others)
	path('reservation-calendar/', views.ReservationFeed(), name="reservation-calendar")
]