document.addEventListener("DOMContentLoaded", function(event) {

    activeStuff = document.getElementById("active");
    inactiveStuff = document.getElementById("inactive");
    var url = "http://172.16.0.1:5010"
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    control = document.getElementById("control");
    control.style.display = "none";
    firstName = document.getElementById("firstName");
    lastName = document.getElementById("lastName");
    data = "";
    token = "";

    handleResponse = function(e) {
        if(e.origin == url) 
        { 
            if (data != e.data)
            {
                data = e.data.split("|");
                if (data[0] == "active")
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

        setTimeout(function() {
            iframe.src = url;
        }, 500);
    } 
    window.addEventListener('message', handleResponse, false);
    
    // Callback when iframe contents are loaded
    iframeLoaded = function() {
        console.log("Posting request");
        iframe.contentWindow.postMessage('sessionState', url);
    };

    // Register iframe load callback
    iframe.addEventListener("load", iframeLoaded, false);
    iframe.src = url;

    cmd_startSession.addEventListener("click", function() {
        token = firstName.value + ":" + lastName.value + ":"
        token += Math.floor(Math.random() * 20);
        control.src = "http://172.16.0.1:5010/session?state=active&token=" + token;
    });

});