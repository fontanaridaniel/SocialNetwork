var mod = null;

$("#load").on("load", function () {});

function fastLoad() {
    loadDB($("#fastLoad").val());
    window.history.pushState('', '', 'http://' + document.domain + ':' + location.port + '/admin');
    $("div" + $("#fastLoad").val()).css("background", "blue");
}

function modify_chat(chat_id) {
    if (mod != chat_id && mod != null) { //Do not modify
        return 0;
    } else if (mod == chat_id) { //save modifications
        $("#edit" + chat_id).children("i").removeClass("fas fa-times").addClass("fas fa-edit");
        $("#del" + chat_id).css("visibility", "hidden");
        $("#row" + chat_id).children("td").css("background", "");
        mod = null;
        return 1;
    }
    $("#edit" + chat_id).children("i").removeClass("fas fa-edit").addClass("fas fa-times");
    $("#del" + chat_id).css("visibility", "visible");
    $("#row" + chat_id).children("td").css("background", "rgb(206, 66, 66)")
    mod = chat_id;
}

function delete_chat(chat_id) {
    mod = null;
    $.ajax({
        url: "/ADMIN_delete_chat",
        type: "get",
        data: {
            chat_id: chat_id
        },
        success: function (response) {
            $("#result").html(response);
        },
        error: function (xhr) { }
    });
}

function modify_posts(post_id, user_id) {
    if (mod != post_id && mod != null) { //Do not modify
        return 0;
    } else if (mod == post_id) { //save modifications
        $("form").children("#profileImageFile").remove();
        $("#profileImageFile").clone().appendTo("#form");
        $("#title").val($("#row" + post_id).children("#post_title").children("textarea").val());
        $("#description").val($("#row" + post_id).children("#post_description").children("textarea").val());
        $("#hashtag").val($("#row" + post_id).children("#post_hashtags").children("textarea").val());
        $("#id_post").val(post_id);
        $("#id_user").val(user_id);
        $("#submitBtn").click();
        return 1;
    }
    $("#edit" + post_id).css("visibility", "hidden");
    $("#save" + post_id).css("visibility", "visible");
    $("#undo" + post_id).css("visibility", "visible");
    mod = post_id;
    var post_title = $("#row" + post_id).children("#post_title");
    var post_description = $("#row" + post_id).children("#post_description");
    var post_hashtags = $("#row" + post_id).children("#post_hashtags");
    var title = post_title.text();
    var description = post_description.text();
    var hashtags = post_hashtags.text();
    $("#label" + post_id).attr({ "for": "profileImageFile" });
    $("#row" + post_id).children("#post_title").empty();
    $("#row" + post_id).children("#post_description").empty();
    $("#row" + post_id).children("#post_hashtags").empty();
    $("#row" + post_id).children("td").css("background", "rgb(206, 66, 66)")
    $("#row" + post_id).children("#post_title").append($("<textarea id='post_title'></textarea>").val(title));
    $("#row" + post_id).children("#post_description").append($("<textarea id='post_description'></textarea>").val(description));
    $("#row" + post_id).children("#post_hashtags").append($("<textarea id='post_hashtags'></textarea>").val(hashtags));
}

function delete_post(post_id) {
    mod = null;
    $.ajax({
        url: "/ADMIN_delete_post",
        type: "get",
        data: {
            post_id: post_id
        },
        success: function (response) {
            $("#result").html(response);
        },
        error: function (xhr) { }
    });
}

function modify_users(user_id) {
    if (mod != user_id && mod != null) { //Do not modify
        return 0;
    } else if (mod == user_id) { //save modifications
        $("form").children("#profileImageFile").remove();
        $("#profileImageFile").clone().appendTo("#form");
        $("#name").val($("#row" + user_id).children("#user_name").children("textarea").val());
        $("#lastname").val($("#row" + user_id).children("#user_lastname").children("textarea").val());
        $("#username").val($("#row" + user_id).children("#user_username").children("textarea").val());
        $("#email").val($("#row" + user_id).children("#user_email").children("textarea").val());
        $("#id_user").val(user_id);
        $("#submitBtn").click();
        return 1;
    }
    $("#edit" + user_id).css("visibility", "hidden");
    $("#save" + user_id).css("visibility", "visible");
    $("#undo" + user_id).css("visibility", "visible");
    mod = user_id;
    var user_name = $("#row" + user_id).children("#user_name");
    var user_lastname = $("#row" + user_id).children("#user_lastname");
    var user_username = $("#row" + user_id).children("#user_username");
    var user_email = $("#row" + user_id).children("#user_email");
    var name = user_name.text();
    var lastname = user_lastname.text();
    var username = user_username.text();
    var email = user_email.text();
    $("#label" + user_id).attr({ "for": "profileImageFile" });
    $("#row" + user_id).children("#user_name").empty();
    $("#row" + user_id).children("#user_lastname").empty();
    $("#row" + user_id).children("#user_username").empty();
    $("#row" + user_id).children("#user_email").empty();
    $("#row" + user_id).children("td").css("background", "rgb(206, 66, 66)")
    $("#row" + user_id).children("#user_name").append($("<textarea id='user_name'></textarea>").val(name));
    $("#row" + user_id).children("#user_lastname").append($("<textarea id='user_lastname'></textarea>").val(lastname));
    $("#row" + user_id).children("#user_username").append($("<textarea id='user_username'></textarea>").val(username));
    $("#row" + user_id).children("#user_email").append($("<textarea id='user_email'></textarea>").val(email));
}

function delete_user(user_id) {
    mod = null;
    $.ajax({
        url: "/ADMIN_delete_user",
        type: "get",
        data: {
            user_id: user_id
        },
        success: function (response) {
            $("#result").html(response);
        },
        error: function (xhr) { }
    });
}

function loadDB(db) {
    mod = null;
    $.ajax({
        url: "/selectDB_component",
        type: "get",
        data: {
            jsdata: db
        },
        success: function (response) {
            $("#result").html(response);
        },
        error: function (xhr) { }
    });
}