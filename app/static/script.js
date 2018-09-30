function favourite(imdbID) {

    $.ajax({
        url : '/favourites/'+imdbID
    })
        .done(function(response) {
            $('#heart'+imdbID).toggleClass('favourite-transform');
            $('#heart'+imdbID).toggleClass('glyphicon-heart').toggleClass('glyphicon-heart-empty');
        })
        .fail(function() {
            alert( "Wystąpił błąd w połączniu");
        })
        .always(function() {
            //alert('always');
        });

}


