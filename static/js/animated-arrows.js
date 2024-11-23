$('.pre-arrow').on('click', function() {
    $(this).children().toggleClass('active');
});

$('.pre-expandable').on('click', function() {
    $(this).children().toggleClass('is-expanded');
});

$('.icon-expandable').on('click', function() {
    $(this).toggleClass('is-expanded');
});
