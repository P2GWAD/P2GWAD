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

    $('#search-other-players').keyup(function(){
        var query;
        var user_id = $(this).attr('data-user-id');
        query = $(this).val();

        $.get('/P2G/search_others/',
            {'suggestion': query, 'user_id': user_id},
            function(data){
                $('#others-listing').html(data);
            })
    });

    $('#search-friends').keyup(function(){
        var query;
        var user_id = $(this).attr('data-user-id');
        query = $(this).val();

        $.get('/P2G/search_friends/',
            {'suggestion': query, 'user_id': user_id},
            function(data){
                $('#friend-list').html(data);
            })
    });

    $('.P2G-add-friend').click(function(){
        var clickedButton = $(this);
        var user_id = $(this).attr('data-user-id');
        var friend_id = $(this).attr('data-friend-id');

        clickedButton.attr('disabled','disabled')
        clickedButton.attr('value','Your Friend')
        clickedButton.attr('class', "btn")

        $.get('/P2G/add_friend/', {'user_id': user_id, 'friend_id': friend_id});
    });

    $('.P2G-remove-friend').click(function(){
        var user_id = $(this).attr('data-user-id');
        var friend_id = $(this).attr('data-friend-id');
        var friend_name = $(this).attr('data-friend-name');
        var message = "Are you sure you don't want to be friends with " + friend_name + " anymore?";

        if(confirm(message)){
            $.get('/P2G/remove_friend/',
            {'user_id': user_id, 'friend_id': friend_id},
            function (data){
                $('#friend-list').html(data);
            });
        };
    });

    $('.rango-add-user').click(function(){
        var clickedButton = $(this);
        var username = $(this).attr('data-username');
        var user_id = $(this).attr('data-user-id');
        document.getElementById('current-members-names').append(", " + username);
        var curr_ids = document.getElementById('current-members-ids').getAttribute('value');
        var new_ids = curr_ids + ',' + user_id;
        document.getElementById('current-members-ids').setAttribute('value', new_ids);
        clickedButton.hide();
    });
});