socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
notify = io.connect('http://' + document.domain + ':' + location.port + '/notify');

notify.on('connect', function () {
    socket.emit('joined', {
        room: id_receiver
    });
})

socket.on('connect', function () {
    socket.emit('joined', {
        room: id_chat
    });
    $(document).keypress(function (e) {
        if ($("#messageBox").is(":focus")) {
            if (e.keyCode == 13) {
                $("#sendButton").click();
            }
        }
    });
    $('#sendButton').click(function (e) {
        $('#sendButton').prop("disabled", true);
        e.preventDefault()
        data = encodeURIComponent($('#messageBox').val());
        if ($('#messageBox').val() != "") {
            socket.emit('send_msg', {
                room: id_chat,
                id_chat: id_chat,
                data: data
            });
            notify.emit('send_notify', {
                room: id_receiver,
                data: data
            });
        }
        $("#messageBox").val('')
        $('#sendButton').prop("disabled", false);
    })
})

var lastDate = "";
socket.on('receive', function (data) {
    for (var msg in data) {
        if (data.hasOwnProperty(msg)) {
            if (data[msg]["id_chat"] == id_chat && data[msg]["msg"] != "" && data[msg]["date"] != lastDate) {
                var text = data[msg]["msg"];
                var date = data[msg]["date"].split(" ")[1].split(".")[0].split(":");
                var messageDiv = document.createElement("div");
                var textDiv = document.createElement("div");
                var timeDiv = document.createElement("div");
                var pTimeDiv = document.createElement("p");
                textDiv.className = "text";
                timeDiv.className = "time";
                pTimeDiv.innerText = date[0] + ":" + date[1];
                textDiv.innerText = text;
                if (id_user == data[msg]["id_sender"]) {
                    messageDiv.className = "message mine";
                } else {
                    messageDiv.className = "message";
                }
                timeDiv.appendChild(pTimeDiv);
                messageDiv.appendChild(timeDiv);
                messageDiv.appendChild(textDiv);
                document.getElementById("chat").appendChild(messageDiv);
                lastDate = data[msg]["date"];
            }
        }
    }
    $("#chat").scrollTop($("#chat")[0].scrollHeight);
});

function disconnect_chat() {
    socket.disconnect();
    notify.disconnect();
}