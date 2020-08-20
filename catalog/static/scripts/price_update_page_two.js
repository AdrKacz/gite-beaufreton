const form = document.querySelector("form");
const price = document.querySelector("form h2");

const day_price = parseFloat(document.querySelector("#prix").getAttribute("price"));

const _MS_PER_DAY = 1000 * 60 * 60 * 24;

function getDateDifferenceInDays(start_date, end_date) {
	// start_date and end_date have to be Date objects
	// Discard the time and time-zone information.
 	const utc_start = Date.UTC(start_date.getFullYear(), start_date.getMonth(), start_date.getDate());
 	const utc_end = Date.UTC(end_date.getFullYear(), end_date.getMonth(), end_date.getDate());

 	return Math.floor((utc_end - utc_start) / _MS_PER_DAY);
};


function updatePrice() {
	let price_value = 0;

	let start_date;
	let end_date;

	for (let i = form.elements.length - 1; i >= 0; i--) {
		const element = form.elements[i];
		if (element.id) {
			
			if (element.type === "checkbox") {
				// Is a checked checkbox
				if (element.checked) {
					// Add the price value
					price_value += parseInt(document.querySelector("label[for="+element.id).getAttribute('price'));
				};
			}
			else if (element.type === "number") {
				// Is a number
				// Add the price value times the number of elements
				price_value += parseInt(element.value) * parseInt(document.querySelector("label[for="+element.id).getAttribute('price'));
			} else {
				// Else is a date
				// Is a date (text format --> SANATIZE INPUT, NOT DONE HERE)
				// Sanetize should occur here on element.value
				if (element.id === "id_start_date") {
					start_date = new Date(element.value)
				}
				else if (element.id === "id_end_date") {
					end_date = new Date(element.value)
				};
			};
		};
	};

	// Check if both date are valid and calculate the difference if so
	if (start_date.valueOf() && end_date.valueOf()) {
		const differenceInDays = getDateDifferenceInDays(start_date, end_date)
		price_value += differenceInDays * day_price;
	};

	// Update the price displayed
	price.textContent = "Prix: " + price_value + "€";
};

// Add the event listener
for (let i = form.elements.length - 1; i >= 0; i--) {
	if (form.elements[i].id) {
		form.elements[i].addEventListener('change', updatePrice);
	};
};

// First Update when the page is loading
updatePrice()