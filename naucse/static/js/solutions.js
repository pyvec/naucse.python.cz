(function () {
    'use strict';
    var attach_click_handler = function (detail) {
        var links = detail.getElementsByTagName('a');
        var handler = function (e) {
            detail.classList.add('opened');

            var bodies = detail.getElementsByClassName('solution-body');
            for(var i=0; i < bodies.length; i++) {
                bodies[i].setAttribute('aria-hidden', 'false');
            }
            for(var i=0; i < links.length; i++) {
                links[i].setAttribute('aria-hidden', 'true');
            }

            e.preventDefault();
        };
        for(var i=0; i < links.length; i++) {
            links[i].addEventListener('click', handler, false);
        }
    }

    var details = document.getElementsByClassName('solution');
    for(var i=0; i < details.length; i++) {
        attach_click_handler(details[i]);
    }
})()
