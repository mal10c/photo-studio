document.addEventListener("DOMContentLoaded", function(event) {

    activeStuff = document.getElementById("active");
    inactiveStuff = document.getElementById("inactive");
    var url = "http://172.16.0.1:5010"
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    control = document.getElementById("control");
    control.style.display = "none";

    handleResponse = function(e) { 
        if(e.origin == url) 
        { 
            if (e.data == "active")
            {
                activeStuff.style.display = "block";
                inactiveStuff.style.display = "none";
            }
            else
            {
                activeStuff.style.display = "none";
                inactiveStuff.style.display = "block";
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

    cmd_startSession.addEventListener("click", function() {
        control.src = "http://172.16.0.1:5010/session?state=active";
    });

});