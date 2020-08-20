const form = document.querySelector("form");
const details_section = document.querySelector("#price_details");
const option_section = document.querySelector("#price_details > section");
const div_night = document.querySelector("section#price_details > div:first-child");
const price = document.querySelector("#price_total");

const day_price = parseFloat(document.querySelector("#price_total").getAttribute("price"));

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

	// Clean the option section
	while (option_section.childElementCount > 0) {
  		option_section.removeChild(option_section.childNodes[0]);
	};

	// Calculte total price and update option_section
	for (let i = form.elements.length - 1; i >= 0; i--) {
		const element = form.elements[i];
		if (element.id) {
			
			if (element.type === "checkbox") {
				// Is a checkbox
				if (element.checked) {
					// Add the price value
					const price_item = parseInt(document.querySelector("label[for="+element.id).getAttribute('price'));

					price_value += price_item;

					// Add a line to the details section

					// Create the <p> tag and fill them
					const div_container = document.createElement('div');
					const option_info = document.createElement('p');
					const option_price = document.createElement('p');

					option_info.textContent = document.querySelector("label[for="+element.id).getAttribute('name');
					option_price.textContent = '' + price_item + '€';

					// Append them to the option section
					div_container.appendChild(option_info);
					div_container.appendChild(option_price);
					option_section.appendChild(div_container);
				};
			}
			else if (element.type === "number") {
				// Is a number
				// Add the price value times the number of elements
				const element_value = parseInt(element.value);
				const price_unit = parseInt(document.querySelector("label[for="+element.id).getAttribute('price'));
				const price_item = element_value * price_unit;

				price_value +=  price_item;

				// Add a line to the details section if more than 0
				if (element_value > 0) {
					// Create the <p> tag and fill them
					const div_container = document.createElement('div');
					const option_info = document.createElement('p');
					const option_price = document.createElement('p');

					option_info.textContent = '' + price_unit + '€ x ' + element_value + ' ' + document.querySelector("label[for="+element.id).getAttribute('name') + '(s)';
					option_price.textContent = '' + price_item + '€';

					// Append them to the option section
					div_container.appendChild(option_info);
					div_container.appendChild(option_price);
					option_section.appendChild(div_container);
				};

			} else {
				// Else is a date
				// Is a date (text format --> SANATIZE INPUT, NOT DONE HERE)
				// Sanetize should occur here on element.value
				if (element.id === "id_start_date") {
					start_date = new Date(element.value);
				}
				else if (element.id === "id_end_date") {
					end_date = new Date(element.value);
				};
			};
		};
	};

	// Check if both date are valid and calculate the difference if so
	if (start_date.valueOf() && end_date.valueOf()) {
		const differenceInDays = getDateDifferenceInDays(start_date, end_date);
		const price_item = differenceInDays * day_price;
		price_value += price_item;

		// Update the "number of nights"  (i.e. div_night) line
		div_night.querySelector("p:first-child").textContent = '' + day_price + '€ x ' + differenceInDays + ' Nuit(s)'
		div_night.querySelector("p:last-child").textContent = '' + price_item + '€';

	} else {
		// Update the div_night with 0 night
		div_night.querySelector("p:first-child").textContent = '' + day_price + '€ x 0 Nuit';
		div_night.querySelector("p:last-child").textContent = '0€';
	};

	// Update the price displayed
	price.textContent = "" + price_value + "€";
};

// Add the event listener
for (let i = form.elements.length - 1; i >= 0; i--) {
	if (form.elements[i].id) {
		form.elements[i].addEventListener('change', updatePrice);
	};
};

// First Update when the page is loading
updatePrice()