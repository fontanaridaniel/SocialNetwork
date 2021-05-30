function showPswdPopup() {
    $(".profileContent").css({
        '-webkit-filter': 'blur(5px)',
        '-moz-filter': 'blur(5px)',
        '-o-filter': 'blur(5px)',
        '-ms-filter': 'blur(5px)',
        'filter': 'blur(5px)'
    });

    $(".changePswdPopup").css("display", "grid");
    $("#error").hide();
}

function hidePswdPopup() {
    $(".profileContent").css({
        '-webkit-filter': '',
        '-moz-filter': '',
        '-o-filter': '',
        '-ms-filter': '',
        'filter': ''
    });

    $(".changePswdPopup").hide();
}

function changePswd() {
    oldPdw = $("#oldPassword").val();
    newPdw = $("#newPassword").val();
    conPdw = $("#confirmPassword").val();
    if (newPdw != conPdw) {
        $("#error").text("Le password non coincidono");
        $("#error").show();
    } else {
        $.ajax({
            url: "/change_password",
            type: "get",
            data: {
                oldPdw: oldPdw,
                newPdw: newPdw
            },
            success: function (response) {
                if (response == "errore") {
                    $("#error").text("La vecchia password è errata");
                    $("#error").show();
                } else {
                    hidePswdPopup();
                }
            },
            error: function (xhr) { }
        });
    }
}

function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function toggleEdit(btn) {
    if ($(btn).html().includes("edit")) {
        $(btn).css("background", "var(--defaultGreenBtn)");
        $(btn).html("<i class='fas fa-save'></i>");
        $("." + $(btn).attr("name")).prop("disabled", false);
    }
    else {
        val = $("[name='"+$(btn).attr("name")+"'").val().length;
        var flag = true;
        switch ($(btn).attr("name")) {
            case "name":
                if (val < 3 || val > 16) {
                    flag = false;
                }
                break;
            case "lastname":
                if (val < 3 || val > 16) {
                    flag = false;
                }
                break;
            case "username":
                if (val < 3 || val > 24) {
                    flag = false;
                }
                break;
            case "email":
                if (val < 6 || !validateEmail($("[name='"+$(btn).attr("name")+"'").val())) {
                    flag = false;
                }
                break;
            default:
                break;
        } 
        if (flag) {
                $.ajax({
                url: "/change_personal",
                type: "get",
                data: {
                    attr: $(btn).attr("name"),
                    value: $("[name='"+$(btn).attr("name")+"'").val()
                },
                success: function (response) {
                    if (response != "") {
                        alert(response);
                    } else {
                        $(btn).css("background", "var(--accentColor)");
                        $(btn).html("<i class='fas fa-edit'></i>");
                        $("." + $(btn).attr("name")).prop("disabled", true);
                    }
                },
                error: function (xhr) { }
            });
        } else {
            alert($(btn).attr("name")+" deve rispettare i criteri di lunghezza, maggiore di 3 e minore di 16");
        }
        
    }
}