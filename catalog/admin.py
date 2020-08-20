from django.contrib import admin

# Register your models here.

from .models import Logement, Reservation, Photographie, Caracteristique, Option, Calendrier


""" Minimal registrations of Model exemple
admin.site.register(Logement)
"""



class ReservationsInline(admin.TabularInline):
	"""Defines format of inline reservation insertion (used in LogementAdmin)"""
	model = Reservation
	extra = 0

@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
	"""Administration object for Logement models.
	Defines:
		- 	fields to be displayed in list view (list_display)
	"""

	list_display = ('nom', 'prix', 'capacite')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	"""Administration object for Reservation models.
	Defines:
		- 	fields to be displayed in list view (list_display)
		-	filters that will be displayed in sidebar (list_filter)
		- 	grouping of fields into sections (fieldsets)
	"""

	list_display = ('debut', 'fin', "source", "uid")
	list_filter = ('debut', 'fin', "source")

	fieldsets = (
		(None, {
			'fields': ('source', "uid", "description")
		}),
		('Dates', {
			'fields': ('debut', 'fin')
		}),
	)

@admin.register(Photographie)
class PhotographieAdmin(admin.ModelAdmin):
	"""Administration object for Caracteristique models.
	Defines:
		- 	fields to be displayed in list view (list_display)
		-	filters that will be displayed in sidebar (list_filter)
	"""

	list_display = ('nom', 'logement', 'page_principale')
	list_filter = ('logement', 'page_principale')

@admin.register(Caracteristique)
class CaracteristiqueAdmin(admin.ModelAdmin):
	"""Administration object for Caracteristique models.
	Defines:
		- 	fields to be displayed in list view (list_display)
		-	filters that will be displayed in sidebar (list_filter)
	"""

	list_display = ('description', 'icon', 'z_axis')
	list_filter = ('z_axis',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	"""Administration object for Option models.
	Defines:
		- 	fields to be displayed in list view (list_display)
		-	filters that will be displayed in sidebar (list_filter)
	"""

	list_display = ('nom', 'prix', 'plusieurs')
	list_filter = ('prix', 'plusieurs')


@admin.register(Calendrier)
class CalendrierAdmin(admin.ModelAdmin):
	"""Administration object for Calendrier models.
	Defines:
		-	fields to be displayed in list view (list_display)
		- 	adds inline addition of Reservation instances in Logement view (inlines)
	"""

	list_display = ("nom", "url")
	inlines = [ReservationsInline]
