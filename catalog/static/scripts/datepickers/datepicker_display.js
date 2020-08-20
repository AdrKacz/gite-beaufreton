// Selectors
const dates = document.querySelector("div.date-container");
const inputs = document.querySelectorAll("div.date-container input");
const spans = document.querySelectorAll("div.date-container span");
// Create the DatePicker
const datepicker = new Datepicker(dates);

// Event to dispatch for the inputs
const change_event = new Event("change");

// Date object for Today
const today = new Date();

// List that store dates (0: start_date, 1: end_date)
const dates_list = [null, null];

// List that store fetch result
let _fetch_reservations = {};

// Function that displays dates on node if enable
function display_date(node, content) {
	node.textContent = content;
};

// Function that updates input
function update_inputs() {
	// Update start_date and end_date if any
	for (let i = dates_list.length - 1; i >= 0; i--) {
		if (dates_list[i]) {
			const date_number = '0' + dates_list[i].getDate();
			const month_number = '0' + (dates_list[i].getMonth() + 1);

			inputs[i].value = [
				dates_list[i].getFullYear(),
				month_number.substring(month_number.length - 2),
				date_number.substring(date_number.length - 2),
				].join('-');		
		};
	};

	if (dates_list[0] && dates_list[1]) {
		inputs[0].dispatchEvent(change_event);
	};
};

// Function that update displayed text
function update_text() {
	// This function is only called when the inputs as ended
	// We perform a test none the least
	for (let i = dates_list.length - 1; i >= 0; i--) {
		if (dates_list[i]) {
			spans[i].textContent = [
				// WEEKDAYS_SHORT[dates_list[i].getDay()],
				dates_list[i].getDate(),
				MONTHS_SHORT[dates_list[i].getMonth()],
				dates_list[i].getFullYear(),
				].join(' ');
		};
	};
};

// Function that handle the click on date
// Declared this way because init in datepicker.js
handle_date_selection = function () {
	// Add date to dates_list
	const selected_date = datepicker.getDate()
	if (!dates_list[0]) {
		// First time selecting
		dates_list[0] = selected_date;

	}
	else {
		if (!dates_list[1]) {		
			// Second time selecting
			if (dates_list[0] < selected_date) {
				// Correct order
				dates_list[1] = selected_date
			}
			else if (dates_list[0] > selected_date) {
				// Re-order, end before start
				dates_list[1] = dates_list[0];
				dates_list[0] = selected_date;
			}
			else {
				// Impossible, end and start the same day
				console.log("Come and Leave the same day > Impossible")
			};

		} else {
			// Reset the dates if both were selected and click again
			dates_list[0] = selected_date;
			dates_list[1] = null;
		};
	};

	// Update the inputs for the server
	update_inputs();

	// Close the datepicker if selection ended
	if (dates_list[0] && dates_list[1]) {
		datepicker.show(false);
		update_text();
	};
};

// Function for the DatePickers
function enabled_days(date) {
	for (const [uid, dates] of Object.entries(_fetch_reservations)) {
  		if (date >= new Date(dates.start) && date <= new Date(dates.end)) {
  			return false;
  		};
	};
	return true;
};

function format_date(date) {

	// // Set visible value
	// display_date(dates[0].childNodes[0], [
	// 	WEEKDAYS_SHORT[date.getDay()],
	// 	date.getDate(),
	// 	MONTHS_SHORT[date.getMonth()],
	// 	date.getFullYear(),
	// 	].join(' '));

	return '';
};

// Fetch date THEN Config
fetch("/catalog/reservation-dates/")
	.then((response) => response.json())
	.then((json) => {
		_fetch_reservations = json;
	}).then((_) => {
		// Config the DatePickers
		datepicker.config({
			first_date: today,
		    initial_date: today,
		    enabled_days: enabled_days,
		    format: format_date,
		    first_day_of_week: "Monday",
		});
	}).then((_) => {
		// Set the text to the date value if any
		if (inputs[0].value.length > 0 && inputs[1].value.length) {
			datepicker.setDate(new Date(inputs[0].value));
			datepicker.setDate(new Date(inputs[1].value));
		};
	})
	.catch((error) => {
		console.error('Error while fetching reserved dates from server or config the datepicker')
	});
// Config the DatePickers
// datepicker.config({
// 	first_date: today,
//     initial_date: today,
//     enabled_days: enabled_days,
//     format: format_date,
//     first_day_of_week: "Monday",
// });

