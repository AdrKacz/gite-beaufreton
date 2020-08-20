# Forms Handling
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime

# Import Option to count them before creating the Form
# Import Reservations to check if the reservation is available

from .models import Reservation, Option, Logement, Calendrier

# Function to handle calendar import
from .calendar_handling import read_calendar, update_database


class PickDatesForm(forms.Form):
	start_date = forms.DateField(
		help_text="Arrivée",
		required=True,
		widget=forms.HiddenInput(attrs={
			"price": Logement.objects.only("prix")[0].prix}))

	end_date = forms.DateField(
		help_text="Départ",
		required=True,
		widget=forms.HiddenInput(attrs={}))

	def clean_start_date(self):
		data = self.cleaned_data['start_date']

		# Check if the date is not in the past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - start date in the past'))

		return data

	def clean_end_date(self):
		data = self.cleaned_data['end_date']

		# Check if the date is not in the past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - end date in the past'))

		return data

	def clean(self):
		# Get the cleaned date
		cleaned_data = super().clean()
		data_start = cleaned_data.get("start_date")
		data_end = cleaned_data.get("end_date")

		# Basic check
		if data_start and data_end:
			if data_end <= data_start:
				raise ValidationError(_('Invalid date - end date before start date'))

		# Get the calendar from outside (Airbnb)
		try:
			update_database()
		except:
			print("Error while updating the Reservations Database")

		# Check if not in reservation
		is_between = Reservation.objects.filter(debut__lte=data_end, fin__gte=data_start).exists()
		print("Between?", is_between)
		if is_between:
			raise ValidationError(_('Invalid date - date already reserved'))

		return cleaned_data
		
class PickDatesOptionsForm(PickDatesForm):

	def __init__(self, *args, **kwargs):
		super(PickDatesOptionsForm, self).__init__(*args, **kwargs)

		# Dynamic Field
		for option in Option.objects.all():
			if option.plusieurs:
				self.fields[str(option.id)] = forms.IntegerField(
					label=option.nom,
					initial=0,
					min_value=0,
					max_value=int(option.maximum),
					help_text="option", 
					required=True)
			else:
				self.fields[str(option.id)] = forms.BooleanField(
					label=option.nom,
					help_text="option",
					required=False)

	# Static Field
	# Already defined above, with clean_static-field() and clean()



