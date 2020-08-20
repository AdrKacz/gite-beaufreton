const confirm_div = document.querySelector("section#info_logement > form > div");
const div_em = document.querySelector("div#div-for-em");

function get_em_value(value){
    div_em.style.height = value;
    return div_em.offsetHeight;
}

// Reference: http://www.html5rocks.com/en/tutorials/speed/animations/

let last_known_scroll_position = 0;
let ticking = false;

function doSomething(scroll_pos) {
 	if (scroll_pos > get_em_value('calc(5em + 1vh')) {
 		confirm_div.style.position = "static";
 	} else {
 		confirm_div.style.position = "fixed";
 	}
};

window.addEventListener('scroll', function(e) {
  last_known_scroll_position = window.scrollY;

  if (!ticking) {
    window.requestAnimationFrame(function() {
      doSomething(last_known_scroll_position);
      ticking = false;
    });

    ticking = true;
  }
});