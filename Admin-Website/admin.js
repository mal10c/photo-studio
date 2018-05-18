document.addEventListener("DOMContentLoaded", function(event) {

    control = document.getElementById("control");
    control.style.display = "none";
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    var url = "http://172.16.0.1:5010"

    // Div tags
    var sessionControls = document.getElementById("sessionControls");

    // Buttons
    var cmd_endSession = document.getElementById("cmd_endSession");
    var cmd_takePhoto = document.getElementById("cmd_takePhoto");

    // Button click events
    cmd_endSession.addEventListener("click", function() {
        control.src = "http://172.16.0.1:5010/session?state=inactive";
    });

    cmd_takePhoto.addEventListener("click", function() {
        alert("Take photo!");
    });

    // Callback when iframe contents are loaded
    iframeLoaded = function() {
        console.log("Posting request");
        iframe.contentWindow.postMessage('sessionState', url);
    };

    handleResponse = function(e) { 
        if(e.origin == url) 
        { 
            if (e.data == "active")
            {
                sessionControls.style.display = "block";
            }
            else
            {
                sessionControls.style.display = "none";
            }
        }

        setTimeout(function() {
            iframe.src = url;
        }, 500);
    } 
    window.addEventListener('message', handleResponse, false);

    // Register iframe load callback
    iframe.addEventListener("load", iframeLoaded, false);
    iframe.src = url;

});