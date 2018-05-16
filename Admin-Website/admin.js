document.addEventListener("DOMContentLoaded", function(event) {

    control = document.getElementById("control");
    control.style.display = "none";
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    var url = "http://132.250.60.1:5010"
    var cmd_endSession = document.getElementById("cmd_endSession");
    cmd_endSession.addEventListener("click", function() {
        control.src = "http://132.250.60.1:5010/session?state=inactive";
    });

    handleResponse = function(e) { 
        if(e.origin == url) 
        { 
            if (e.data == "active")
            {
                cmd_endSession.style.display = "block";
            }
            else
            {
                cmd_endSession.style.display = "none";
            }
        } 
    } 
    window.addEventListener('message', handleResponse, false);

    // Callback when iframe contents are loaded
    iframeLoaded = function() {
        console.log("Posting request");
        iframe.contentWindow.postMessage('sessionState', url);
        removeEventListener("load", iframeLoaded, true);
        iframe.src = url;
    };

    // Register iframe load callback
    iframe.addEventListener("load", iframeLoaded, false);
    iframe.src = url;

});