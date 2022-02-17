$(document).ready(function() {
    $('#ul-filter li a').click(function(){
        var value = $(this).attr('data-filter');
        if(value === 'all') {
            $('.filter').show('1000');
            $('#ul-filter li a').removeClass('active-button')
            $(this).addClass('active-button');
        }
        else {
            $(".filter").not('.'+value).hide('3000');
            $('.filter').filter('.'+value).show('3000');
            $('#ul-filter li a').removeClass('active-button')
            $(this).addClass('active-button');
        }
    });
});