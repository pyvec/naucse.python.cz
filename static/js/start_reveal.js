function start_reveal() {
    var links;

    function add_css(src) {
        var head = document.getElementsByTagName('head')[0];
        var s = document.createElement('link');
        s.setAttribute('rel', 'stylesheet');
        s.setAttribute('type', 'text/css');
        s.setAttribute('href', src);
        head.appendChild(s);
    }

    while (true) {
        links = document.getElementsByTagName('link');
        if (links.length) {
            links[0].remove();
        } else {
            break;
        }
    }

    var details = document.getElementsByTagName('details');
    for(i=0; i < details.length; i++) {
        details[i].setAttribute('style', 'display: none');
    }

    add_css("../reveal.js/css/reveal.min.css");
    add_css("../css/reveal-theme.css");
    document.body.setAttribute('class', 'reveal');

    Reveal.initialize({
        controls: true,
        progress: true,
        history: true,
        center: true,

        transition: 'linear',
        transitionSpeed: 'fast',
        backgroundTransition: 'linear',

        dependencies: [
            { src: 'plugin/highlight/highlight.js', async: true, callback: function() { hljs.initHighlightingOnLoad(); } },
            { src: 'plugin/zoom-js/zoom.js', async: true, condition: function() { return !!document.body.classList; } },
        ]
    });
}

if (window.location.hash.substr(0, 2) == '#/') start_reveal();
