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
        ;
    };

    var intervalId = window.setInterval(function () {
        var group_id = document.getElementById('data-group-id').value;
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