(function () {
    var details = document.getElementsByTagName('details');
    function get_show_func(detail) {
        return function () {
            detail.innerHTML = detail.getAttribute('data-innerhtml');
            detail.setAttribute('style', '');
            detail.setAttribute('class', '');
        }
    }
    function show_all(detail) {
        for(i=0; i < details.length; i++) {
            get_show_func(details[i])();
        }
        window.location.hash = '#showall';
    }
    for(i=0; i < details.length; i++) {
        details[i].setAttribute('data-innerhtml', details[i].innerHTML);
        details[i].setAttribute('style', 'margin-bottom:100em');
        var btn = document.createElement('input');
        btn.setAttribute('type', 'button');
        btn.setAttribute('class', 'btn');
        btn.setAttribute('value', 'Řešení »');
        btn.addEventListener('click', get_show_func(details[i]));
        get_show_func(details[i]);
        details[i].setAttribute('class', 'detail-not-expanded');
        details[i].innerHTML = '';
        details[i].appendChild(btn);
    }
    document.getElementById('show-all').addEventListener('click', show_all);
    if(window.location.hash.contains('showall')) {
        show_all();
    }
    document.body.addEventListener('copy', function () {return false;});
    document.body.addEventListener('cut', function () {return false;});
})()