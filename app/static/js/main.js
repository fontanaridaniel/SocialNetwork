/* Check if is on mobile and if profile is open */
$(window).resize(function () {
    if ($(window).width() <= 650) {
        if (isProfileOpen) {
            $(".right").show();
        }
        else {
            $(".right").hide();
        }
    }
    else {
        $(".right").show();
    }
});


/* Scroll to top button */
$(".scrollToTopBtn").click(function () {
    $(".center").animate({
        scrollTop: 0
    }, "fast");
    return false;
});
function updtateScrollToTopBtnPosition() {
    if ($(window).width() <= 650)
        $(".scrollToTopBtn").css("right", "");
    else
        $(".scrollToTopBtn").css("right", $(".right").width() + 72);

    if ($(window).width() <= 715 && isProfileOpen)
        $(".scrollToTopBtn").hide();
    else
        if ($(".center").scrollTop() > 600)
            $(".scrollToTopBtn").show();
        else
            $(".scrollToTopBtn").hide();
}
$(".center").on('scroll', function () {
    updtateScrollToTopBtnPosition();
});
$(window).resize(function () {
    updtateScrollToTopBtnPosition();
});


/* Display Search user*/
$(document).ready(function () {
    $("#myUL").css("width", $("#myInput").width() + 32);
});
$(window).resize(function () {
    $("#myUL").css("width", $("#myInput").width() + 32);
});
$(".center").scroll(function () {
    $("#myUL").hide();
});
$("#myInput").focusout(function () {
    $("#myUL").hide();
});
$("#myInput").focus(function () {
    $("#myUL").show();
});

function openChat(username) {
    location.href = '/chat/' + username;
}

/* Load all posts */
function loadPosts(username) {
    $.ajax({
        url: "/home_top_component",
        type: "get",
        success: function (response) {
            $(".top3").html(response);
        },
        error: function (xhr) { }
    });
    $.ajax({
        url: "/post_component",
        type: "get",
        success: function (response) {
            $("#posts").html(response);
        },
        error: function (xhr) { }
    });
    $('a[name="' + username + '"]').show();
    $('div[name="' + username + '"]').show();
}

/* Load profile in right container */
var isProfileOpen = false;
function loadProfile(username) {
    isProfileOpen = true;
    $("#myInput").val("");
    $("#myUL").hide();
    $.ajax({
        url: "/profile_component",
        type: "get",
        data: {
            jsdata: username
        },
        success: function (response) {
            $(".right").html(response);
            $(".right").show();
            updtateScrollToTopBtnPosition();
        },
        error: function (xhr) { }
    });
}

/* Close profile on the right container */
function closeProfile() {
    isProfileOpen = false;
    $(".right").html("");
    if ($(window).width() <= 650) { $(".right").hide(); }
    updtateScrollToTopBtnPosition();
}


/* Follow / Unfollow profile */
function toggleFollow(username) {
    $.ajax({
        url: "/toggle_follow",
        type: "get",
        data: {
            jsdata: username
        },
        success: function (response) { 
            if (document.getElementById("buttonFollow").innerText == "Non seguire") { //Unfollow
                document.getElementById("profileFollowers").innerText = parseInt(document.getElementById("profileFollowers").innerText) - 1;
                document.getElementById("buttonFollow").innerText = "Segui";
                $('div[name="' + username + '"]').hide();
                $('a[name="' + username + '"]').hide();
            } else {  //Follow
                document.getElementById("profileFollowers").innerText = parseInt(document.getElementById("profileFollowers").innerText) + 1;
                document.getElementById("buttonFollow").innerText = "Non seguire";
                $('a[name="' + username + '"]').show();
                if ($('div[name="' + username + '"]').show().length == 0) {
                    loadPosts(username);
                }
            }
        },
        error: function (xhr) { }
    });
}

/* Like / Remove like to post */
function toggleLike(id) {
    var icon = $('i[name="' + id + '"]');
    var span = $('span[name="' + id + '"]');
    var like = parseInt(span.first().text());
    if (icon.hasClass('fas')) { //unLike
        span.text(like - 1);
        icon.attr('class', 'far fa-heart');
    } else { //Like
        span.text(like + 1);
        icon.attr('class', 'fas fa-heart');
    }
    $.ajax({
        url: "/toggle_like",
        type: "get",
        data: {
            jsdata: id
        },
        success: function (response) { },
        error: function (xhr) { }
    });
}

/* Search profile in the top search bar */
function searchPeople() {
    var text = $("#myInput").val();
    $.ajax({
        url: "/search_component",
        type: "get",
        data: {
            jsdata: text
        },
        success: function (response) {
            $("#myUL").show();
            $("#myUL").html(response);
        },
        error: function (xhr) { }
    });
}

function searchCategory() {
    var text = $("#myInput").val();
    $.ajax({
        url: "/search_category_component",
        type: "get",
        data: {
            jsdata: text
        },
        success: function (response) {
            $("#allPosts").html(response);
        },
        error: function (xhr) { }
    });
}

/* Comments */
function openAddCommentInput() {
    $(".insertComment").css('display', 'grid');
    $(".commentTextInput").focus();
}

function loadPostProfile(post_id, isInLikes = false) {
    $.ajax({
        url: "/profile_post_component",
        type: "get",
        data: {
            post_id: post_id
        },
        success: function (response) {
            $(".right").html(response);
            if (isInLikes) {
                $(".back").hide();
            }
            else {
                $(".close").hide();
            }
            $(".right").show();
        },
        error: function (xhr) { }
    });
}

var isInHomeGlobal = true;
function loadPostComments(post_id, isInHome = false) {
    $.ajax({
        url: "/profile_comments_component",
        type: "get",
        data: {
            post_id: post_id
        },
        success: function (response) {
            $(".right").html(response);
            if (isInHome) {
                $(".back").hide();
                isInHomeGlobal = true;
            }
            else {
                $(".close").hide();
                isInHomeGlobal = false;
            }
            $(".right").show();
        },
        error: function (xhr) { }
    });
}

function sendComment(post_id) {
    var commentText = $(".commentTextInput").val();
    if (commentText == '') {
        return;
    }
    $(".insertComment").hide();
    $.ajax({
        url: "/add_comment",
        type: "get",
        data: {
            post_id: post_id,
            text: commentText
        },
        success: function (response) {
            $(".right").html(response);
            if (isInHomeGlobal) {
                $(".back").hide();
            }
            else {
                $(".close").hide();
            }
        },
        error: function (xhr) { }
    });
}