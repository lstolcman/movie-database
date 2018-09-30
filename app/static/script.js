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


