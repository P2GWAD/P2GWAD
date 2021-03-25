$(document).ready(function() {
    var textarea = document.getElementById('chat-window');
    textarea.scrollTop = textarea.scrollHeight;
    var latest_message_id = -1;

    $('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function () {
        var group_id = document.getElementById('data-group-id').value;
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        var user_id = $(this).attr('data-user-id');
        document.getElementById('chat-message-input').value = '';

        if (message !== '') {
            $.get('/P2G/group_add_message/',
                {'message': message, 'user_id': user_id, 'group_id': group_id},
                function (data) {
                    $('#chat-log').html(data);
                    var textarea = document.getElementById('chat-window');
                    textarea.scrollTop = textarea.scrollHeight;
                })
        }
    };

    $('#group-new-score-input').focus();
    document.querySelector('#group-new-score-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#group-new-score-submit').click();
        }
    };

    document.querySelector('#group-new-score-submit').onclick = function () {
        var scoreInputDom = document.querySelector('#group-new-score-input');
        var score = scoreInputDom.value;
        var user_id = $(this).attr('data-user-id');
        var group_id = $(this).attr('data-group-id');
        if(score !== '') {
            if (!isNaN(score)) {
                document.getElementById('group-new-score-input').value = '';
                $.get('/P2G/add_score/',
                {'score': score, 'user_id': user_id, 'group_id': group_id},
                function (data) {
                    $('#highscores').html(data);
                });
            } else {
                alert('The Score you have entered is non numerical, please check and submit again.');
            }
        }
        var start = new Date().getTime();
        var end = start;
        while(end < start + 200){
            end = new Date().getTime();
        }
        $.get('/P2G/approve_score/',
            {'score_id': -1, 'user_id': user_id},
            function (data) {
                $('#approvals').html(data);
        });

    };

    $('.group-approve-score').click(function(){
        var group_id = document.getElementById('data-group-id').value;
        var user_id = document.getElementById('data-user-id').value;
        var score_id = $(this).attr('data-score-id');
        $.get('/P2G/approve_score/',
            {'score_id':score_id, 'user_id':user_id},
            function (data) {
                $('#approvals').html(data);
        });
        $.get('/P2G/add_score/',
                {'score': -1, 'user_id': -1, 'group_id': group_id},
                function (data) {
                    $('#highscores').html(data);
        });
    });

    $('.group-deny-score').click(function(){
        var group_id = document.getElementById('data-group-id').value;
        var user_id = document.getElementById('data-user-id').value;
        var score_id = $(this).attr('data-score-id');
        $.get('/P2G/remove_score/',
            {'score_id':score_id, 'user_id':user_id},
            function (data) {
                $('#approvals').html(data);
        });
        $.get('/P2G/add_score/',
                {'score': -1, 'user_id': -1, 'group_id': group_id},
                function (data) {
                    $('#highscores').html(data);
        });
    });

    var intervalId = window.setInterval(function () {
        var group_id = document.getElementById('data-group-id').value;
        var user_id = document.getElementById('data-user-id').value;
        $.get('/P2G/message_check/',
            {'latest_message_id': latest_message_id, 'group_id': group_id},
            function (data) {
                if (data !== 'False') {
                    $.get('/P2G/group_update/',
                        {'group_id': group_id},
                        function (data) {
                            $('#chat-log').html(data);
                            var textarea = document.getElementById('chat-window');
                            textarea.scrollTop = textarea.scrollHeight;
                        });
                    latest_message_id = data;
                }
            })
    }, 5000);
});