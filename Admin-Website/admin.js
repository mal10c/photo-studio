document.addEventListener("DOMContentLoaded", function(event) {

    control = document.getElementById("control");
    control.style.display = "none";
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    var url = "http://172.16.0.1:5010"

    // Div tags
    var sessionControls = document.getElementById("sessionControls");
    var countStatus = document.getElementById("countStatus");

    // Buttons
    var cmd_endSession = document.getElementById("cmd_endSession");
    var cmd_takePhoto = document.getElementById("cmd_takePhoto");

    // Lists
    var photosToTakeCt = document.getElementById("photosToTakeCt");
    var countdownTime = document.getElementById("countdownTime");

    photosToTakeCt.addEventListener("change", function() {
        photoCt = photosToTakeCt.value;
        ctDownTime = countdownTime.value;
        console.log("Writing: " + photoCt + ", " + ctDownTime);
        console.log("http://172.16.0.1:5010/adminInfo?photoCtToTake=" + photoCt + "&countdownTime=" + ctDownTime);
        control.src = "http://172.16.0.1:5010/adminInfo?photoCtToTake=" + photoCt + "&countdownTime=" + ctDownTime;
    });

    countdownTime.addEventListener("change", function() {
        photoCt = photosToTakeCt.value;
        ctDownTime = countdownTime.value;
        console.log("Writing: " + photoCt + ", " + ctDownTime);
        console.log("http://172.16.0.1:5010/adminInfo?photoCtToTake=" + photoCt + "&countdownTime=" + ctDownTime);
        control.src = "http://172.16.0.1:5010/adminInfo?photoCtToTake=" + photoCt + "&countdownTime=" + ctDownTime;
    });

    // Button click events
    cmd_endSession.addEventListener("click", function() {
        control.src = "http://172.16.0.1:5010/session?state=inactive";
    });

    // Button that starts the countdown to take photo(s)
    cmd_takePhoto.addEventListener("click", function() {
        console.log("Sending request to countdown-service");
        control.src = "http://172.16.0.1:5010/takePhoto";
    });

    // Callback when iframe contents are loaded
    iframeLoaded = function() {
        iframe.contentWindow.postMessage('sessionState', url);
    };

    handleResponse = function(e) { 
        if(e.origin == url) 
        {
            // Params:
            //  0: state
            //  1: token
            //  2: photo countdown (Yes|No)
            //  3: time left
            params = e.data.split("|");
            if (params[0] == "active")
            {
                console.log("Token: " + params[1]);
                if (params[2] == "Yes")
                {
                    console.log("Photos are ready to view!");
                    countStatus.innerHTML = params[3];
                }
                
                sessionControls.style.display = "block";
            }
            else
            {
                sessionControls.style.display = "none";
            }
        }

        setTimeout(function() {
            iframe.src = url;
        }, 200);
    } 
    window.addEventListener('message', handleResponse, false);

    // Register iframe load callback
    iframe.addEventListener("load", iframeLoaded, false);
    console.log("URL Request: " + url);
    iframe.src = url;

});