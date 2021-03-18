$(document).ready(function(){
    $('#search-game-games').keyup(function(){
        var query;
        query = $(this).val();

        $.get('/P2G/suggest/',
            {'suggestion': query},
            function(data){
                $('#game-listing').html(data);
            })
    });
});