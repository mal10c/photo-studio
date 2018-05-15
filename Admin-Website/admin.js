document.addEventListener("DOMContentLoaded", function(event) {

    control = document.getElementById("control");
    control.style.display = "none";

    var cmd_startSession = document.getElementById("cmd_startSession");
    cmd_startSession.addEventListener("click", function() {
        control.src = "http://132.250.60.1:5010/session?state=active";
    });

    var cmd_endSession = document.getElementById("cmd_endSession");
    cmd_endSession.addEventListener("click", function() {
        control.src = "http://132.250.60.1:5010/session?state=inactive";
    });

});