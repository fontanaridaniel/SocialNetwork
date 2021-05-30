socket = io.connect('http://' + document.domain + ':' + location.port + '/notify');

socket.on('connect', function () {
    socket.emit('joined', {
        room: id_user
    });
})

socket.on('notify', function (data) {
    $("#notifyMessage").text(data["msg"].replaceAll("%20", " "));
    $("#notifyNameLastname").text(data["user"]["name"] + " " + data["user"]["lastname"]);
    $("#notifyImage").attr("src","/app/users/" + data["user"]["username"] + "/imageUser.jpg")
    $("#notifyLoadProfile").attr("onclick", "javascript: openChat('" + data["user"]["username"] + "')");
    spawnNotification();
})

function spawnNotification(){
    $(".notification").css("top","16px");
    setTimeout(function(){
        $(".notification").css("top","-400px");
      }, 4000);
}


function closeNotification(){
    $(".notification").css("top","-400px");
}