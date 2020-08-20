from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

# To handle forms
from catalog.forms import PickDatesForm, PickDatesOptionsForm


# To replace character in date
import re

# Create your views here.

from .models import Logement, Reservation, Photographie, Caracteristique, Option

# To update the Db
from .calendar_handling import update_database

# To send reservation outside
from django_ical.views import ICalFeed

def index(request):
	"""View function for home page of site.
	Handle a form in its core.
	"""
	# Get one image to put as background

	# Do not retreive "image" to save memory
	# Only take those who can be put on background
	# Shuffle and take the first one
	background_image = Photographie.objects.filter(page_principale__exact=True).order_by('?')[:1]

	# Get the other image for the gallery
	all_images = Photographie.objects.all().order_by('?')[:10]

	# [DEBUG ONLY] Create more image from one
	# ###
	# if all_images.count() < 10:
	# 	all_images = [image[0] for image in list(all_images.values_list('image'))] * 10
	# 	all_images = all_images[:10]
	# ###
	

	# Get the "caracteristique"
	characteristics = Caracteristique.objects.all().order_by("z_axis")[:8]

	# Create the context
	context = {
	'background': background_image, 
	'all_images': all_images,
	'characteristics': characteristics}

	# Handle the form (date choices)

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with the data from the request (binding)
		form = PickDatesForm(request.POST)
		context['form'] = form

		# Check if the form is valid
		if form.is_valid():
			# Stock the data in the session for the next pages
			request.session['start_date'] = str(form.cleaned_data['start_date'])
			request.session['end_date'] = str(form.cleaned_data['end_date'])

			return HttpResponseRedirect(reverse('home-details'))

	# If this is a GET (or any other method) create the default form (update the reservations before)
	else:
		update_database()
		form = PickDatesForm()
		context['form'] = form


	# Render the HTML template index.html with the data in the context variable.
	return render(
		request,
		'index.html',
		context=context,
		)


def details(request):
	"""View function for second page of the site.
	Home details and second date selection.
	"""

	# Get 5 photos of the home at random
	home_images = Photographie.objects.exclude(logement__exact=None).order_by('?')[:5]

	# [DEBUG]
	home_images = Photographie.objects.all().order_by('?')[:5]

	# [DEBUG]
	###
	# if home_images.count() < 5:
	# 	home_images = [image[:1] for image in list(home_images.values_list('image'))] * 5
	# 	home_images = home_images[:5]
	###

	# Variable init
	context = {
	'big_image': home_images[:1],
	'home_images': home_images[1:],
	}

	form = None

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with the data from the request (binding)
		form = PickDatesOptionsForm(request.POST)

		# Check if the form is valid
		if form.is_valid():
			# Stock the data in the session for the next pages
			request.session['start_date'] = str(form.cleaned_data['start_date'])
			request.session['end_date'] = str(form.cleaned_data['end_date'])

			options = dict()
			for field in form.cleaned_data:
				if not field in ('start_date', 'end_date'):
					options[field] = form.cleaned_data[field]

			request.session['options'] = options

			return HttpResponseRedirect(reverse('booking'))

	# If this is a GET (or any other method), create the default form
	else:
		# Get the previous date enter by the user (if any)
		start_date = request.session.get("start_date", None)
		end_date = request.session.get("end_date", None)

		# Check the data and add it to the form if they are correct
		initial = dict()
		if start_date and end_date:
			# Field the initials
			initial["start_date"] = start_date
			initial["end_date"] = end_date
			# Check if the received date are correct
			form = PickDatesOptionsForm(initial)
			for field in list(form.fields.keys()):
				if field not in initial:
					form.fields.pop(field)

			# If not, reset the initial
			if not form.is_valid():
				initial = dict()

		form = PickDatesOptionsForm(initial=initial)


	# Link the Options info with the Form result
	form_options = list()
	for field in form:
		if field.help_text == "option":
			form_options.append((field, Option.objects.get(pk=int(field.auto_id[3:]))))

	# Price of the night
	night_price = 0
	if Logement.objects.all().count() > 0:
		# To modify when there will be numerous "logement"
		night_price = Logement.objects.only("prix")[:1].prix


	context['form_options'] = form_options
	context['night_price'] = night_price
	context['form'] = form

	return render(
		request,
		'home-details.html',
		context=context,
		)


def booking(request):
	"""View function for third/last page of the site.
	Bookind, option/date selection and redirect to a paiment link if possible.
	"""
	# Variable init
	context = dict()
	form = None

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with the data from the request (binding)
		form = PickDatesOptionsForm(request.POST)


	# If this is a GET (or any other method), create the default form
	else:
		# Get the previous date enter by the user (if any)
		start_date = request.session.get("start_date", None)
		end_date = request.session.get("end_date", None)
		options = request.session.get("options", None)

		# Check the data and add it to the form if they are correct
		initial = dict()
		if start_date and end_date and options:
			# Field the initials
			initial["start_date"] = start_date
			initial["end_date"] = end_date
			for option in options:
				initial[option] = options[option]
			# Check if the received date are correct
			form = PickDatesOptionsForm(initial)
			for field in list(form.fields.keys()):
				if field not in initial:
					form.fields.pop(field)

			# If not, reset the initial
			if not form.is_valid():
				initial = dict()

		form = PickDatesOptionsForm(initial=initial)

	# Link the Options info with the Form result
	form_options = list()
	for field in form:
		if field.help_text == "option":
			form_options.append((field, Option.objects.get(pk=int(field.auto_id[3:]))))

	# Price of the night
	night_price = 0
	if Logement.objects.all().count() > 0:
		# To modify when there will be numerous "logement"
		night_price = Logement.objects.only("prix")[:1].prix


	context['form_options'] = form_options
	context['night_price'] = night_price
	context['form'] = form

	return render(
		request,
		'booking.html',
		context=context,
		)


def reservation_dates(request):
	"""View function that return JSON file,
	With the dates of the reserved days.
	"""

	# Create the dictionary with dates
	dates = dict()
	for date in Reservation.objects.only("debut", "fin", "uid").iterator():
		dates[date.uid] = {"start":date.debut, "end":date.fin}

	return JsonResponse(dates)


class ReservationFeed(ICalFeed):
	"""Class taht generate an i-cal (.ics file) for Airbnb (and other)
	Relates reservation that was done on this website.
	"""

	product_id = "-//beaufretonhomes.com"
	timezone = "UTC+2"
	file_name = "reservations.ics"

	def items(self):
		return Reservation.objects.filter(source__isnull=True).order_by("-debut")

	def item_guid(self, item):
		return f"{item.uid}{'@beaufretonhomes'}"

	def item_title(self, item):
		return f"Reservation {item.debut}-{item.fin}"

	def item_description(self, item):
		return f"{item.description}"

	def item_start_datetime(self, item):
		return item.debut

	def item_end_datetime(self, item):
		return item.fin

	def item_link(self, item):
		return ""