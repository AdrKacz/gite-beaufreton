# Handling Date
from datetime import date
from django.utils import timezone

# Models needed to update the DB
from .models import Reservation, Calendrier

# To request the calendar from outside
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Read .ics file and return list of reservation
def read_calendar(calendar_lines):
	# Split and keep only the Event (do not care about the rest)
	calendar_lines = calendar_lines.split("\n")
	event_blocks = []
	has_event = False
	for line in calendar_lines:
		if line == "BEGIN:VEVENT":
			event_blocks.append(list())
			has_event = True
		elif line == "END:VEVENT":
			has_event = False

		if has_event:
			event_blocks[-1].append(line)

	# Create the event object
	events = list()
	for event_block in event_blocks:
		events.append({"start_date":None, "end_date":None, "uid":None, "description":None})
		last_append = ""
		for line in event_block:
			if line.startswith("DTEND"):
				date_str = line[line.find("DATE:")+len("DATE:"):]
				events[-1]['end_date'] = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
				last_append = "end_date"

			elif line.startswith("DTSTART"):
				date_str = line[line.find("DATE:")+len("DATE:"):]
				events[-1]['start_date'] = date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
				last_append = "start_date"

			elif line.startswith("UID"):
				events[-1]['uid'] = line[line.find("UID:")+len("UID:"):]
				last_append = "uid"

			elif line.startswith("DESCRIPTION"):
				events[-1]['description'] = line[line.find("DESCRIPTION:")+len("DESCRIPTION:"):]
				last_append = "description"

			if len(last_append) > 0 and (line.startswith(" ") or line.startswith("\t")):
				events[-1][last_append] += line[1:]

	return events

def update_database():
	if Calendrier.objects.all().count() > 0:
		old_reservations = Reservation.objects.all()
		new_reservations = list()
		try:
			url = Calendrier.objects.only('url')[0].url
			req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # headers to hide that this is a scraper
			html = urlopen(req).read().decode()
			new_reservations = read_calendar(html)
		except (HTTPError, URLError): # HAVE TO PRECISE THE TYPE OF ERROR
			# Access Forbidden
			print("Access to Calendar FORBIDDEN")

		# Update the Reservation library
		for new_reservation in new_reservations:
			# Check if reservation is not yet in the Database
			if not Reservation.objects.filter(uid__exact=new_reservation["uid"]).exists():
				reservation = Reservation(
					uid=new_reservation["uid"],
					debut=new_reservation["start_date"].isoformat(),
					fin=new_reservation["end_date"].isoformat(),
					description=new_reservation["description"],
					source=Calendrier.objects.all()[0])
				reservation.save()