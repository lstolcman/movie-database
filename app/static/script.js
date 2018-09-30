function favourite(imdbID) {
    $.ajax({
        url : '/favourites/'+imdbID,
        beforeSend: function() {
            $('#heart'+imdbID).addClass('favourite-transform')
                .delay(600)
                .queue(function(){$(this)
                .removeClass('favourite-transform')
                .dequeue();
                });
        }
    })
        .done(function(response) {
            $('#heart'+imdbID)
            .toggleClass('glyphicon-heart-empty')
            .toggleClass('glyphicon-heart');
        })
        .fail(function() {
            //alert("error occured");
        })
        .always(function() {
            //alert('always');
        });
}


var pages = $('.pagination li');
var activePage = $('.pagination li.active').index();
hide_pages = function() {
    for (var i = 3; i < activePage-3; i++)
        $('#'+pages[i].id).hide();
    for (var i = activePage+3; i < pages.length-3; i++)
        $('#'+pages[i].id).hide();

    if (activePage > 3)
        $('#'+pages[activePage-3].id).show().addClass('disabled').html('<a>...</a>');
    if (activePage < pages.length-3)
        $('#'+pages[activePage+3].id).show().addClass('disabled').html('<a>...</a>');
};

hide_pages();


