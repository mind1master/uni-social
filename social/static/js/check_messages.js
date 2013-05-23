$(function() {
    function check_messages() {
        $.ajax({
            type: "POST",
            url: "/messages/check/",
            data: {
                user_pk: window.USER_PK
            }
        }).done(function ( data ) {
            if (data>0) {
                $(".new-messages").text("(" + data + ")");
            }
        });
    }

    check_messages();
    setInterval(check_messages, 5000);
});
