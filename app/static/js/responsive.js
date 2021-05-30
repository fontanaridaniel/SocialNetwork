var oldCenterWidth = -1;
function responsiveCenter() {
    var centerWidth = $(".center").width();
    oldCenterWidth = centerWidth;

    if (centerWidth <= 250) {
        $(".home").hide();
    }
    else {
        $(".home").show();
    }

    /* TOP BAR */
    if (centerWidth <= 450) {
        $(".addPostBtnLong").hide();
        $(".addPostBtnShort").show();
    }
    else {
        $(".addPostBtnLong").show();
        $(".addPostBtnShort").hide();
    }

    /* TOP 3 */
    if (centerWidth <= 650) {
        $(".top3").css("overflow-x", "auto");
    } else {
        $(".top3").removeAttr('style');
    }


    /* POST */
    if (centerWidth <= 650) {
        $(".post").css({
            "display": "grid",
            "grid-template-columns": "1fr",
            "grid-template-rows": "repeat(3, max-content)",
            "width": "100%",
            "overflow": "hidden"
        });

        $(".post .postImage").css({
            "grid-column": "1/2",
            "grid-row": "2/3",
            "width": "100%",
            "height": "auto"
        });

        $(".post .postHeader").css({
            "grid-column": "1/2",
            "grid-row": "1/2",
            "display": "grid",
            "grid-template-columns": "max-content 1fr max-content"
        });

        $(".post .postBody").css({
            "grid-column": "1/2",
            "grid-row": "3/4"
        });

        $(".post .postBody .postDescription").css({
            "width": "100%"
        });
    } else {
        $(".post").removeAttr('style');
        $(".post .postImage").removeAttr('style');
        $(".post .postHeader").removeAttr('style');
        $(".post .postBody").removeAttr('style');
        $(".post .postBody .postDescription").removeAttr('style');
    }
}

var loopResponsiveCenter = self.setInterval(function () { responsiveCenter() }, 100);