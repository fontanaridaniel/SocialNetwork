var id_chat;
var receiver;
var id_user;
var isChatOpen = false;

function loadChatList() {
    if (document.getElementById("compiled")) {
        isChatOpen = true;
        if ($(window).width() <= 792) {
            $(".chatLeft").hide();
        }
        resizeChat();
    }
    if (isChatOpen == false) {
        $.ajax({
            url: "/chat_list_component",
            type: "get",
            success: function (response) {
                $("#chatLeft").html(response);
            },
            error: function (xhr) { }
        });
    }
}

function loadChat(id, username, user) {
    id_user = user;
    id_chat = id;
    $('#id_user').val(id_user);
    $('#id_chat').val(id_chat)
    receiver = username;
    window.history.pushState('', '', 'http://' + document.domain + ':' + location.port + '/chat/' + username);
    loadProfile(username);
    $.ajax({
        url: "/chat_msg_component",
        type: "get",
        data: {
            jsdata: username,
            id_chat: id_chat
        },
        success: function (response) {
            isChatOpen = true;
            if ($(window).width() <= 792) {
                $(".chatLeft").hide();
            }
            $(".chatRight").html(response);
            $(".chatRight").css('display', 'grid');
            $("#chat").scrollTop($("#chat")[0].scrollHeight);
        }
    });
    $('#id_chat').val(id_chat);
    $('#messageBox').focus()
}

function returnOnChatListMobile() {
    isChatOpen = false;
    window.history.pushState('', '', 'http://' + document.domain + ':' + location.port + '/chat');
    $("#profile").html("");
    $(".chatLeft").show();
    $(".chatRight").hide();
}

$(window).resize(function () { resizeChat(); });
function resizeChat() {
    if ($(window).width() <= 792 && !isChatOpen) {
        $(".chatLeft").show();
        $(".chatRight").hide();
    }
    else if ($(window).width() <= 792 && isChatOpen) {
        $(".chatLeft").hide();
        $(".chatRight").css('display', 'grid');
    }
    else if ($(window).width() > 792 && !isChatOpen) {
        $(".chatLeft").show();
        $(".chatRight").hide();
    }
    else if ($(window).width() > 792 && isChatOpen) {
        $(".chatLeft").show();
        $(".chatRight").css('display', 'grid');
    }
}

function toggleFollow(username) {
    $.ajax({
        url: "/toggle_follow",
        type: "get",
        data: {
            jsdata: username
        },
        success: function (response) { },
        error: function (xhr) { }
    });
    loadProfile(username);
}

function loadProfile(username) {
    $.ajax({
        url: "/profile_component",
        type: "get",
        data: {
            jsdata: username
        },
        success: function (response) {
            $(".right").html(response);
        },
        error: function (xhr) { }
    });
}

function loadedPage() {
    $("#chatLeft").css("visibility", "visible");
    $("#chatRight").css("visibility", "visible");
    $("#profile").css("visibility", "visible");
    isChatOpen = true;
    try {
        $("#chat").scrollTop($("#chat")[0].scrollHeight);
    } catch (error) { }
}