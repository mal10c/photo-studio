document.addEventListener("DOMContentLoaded", function(event) {

    activeStuff = document.getElementById("active");
    inactiveStuff = document.getElementById("inactive");
    var url = "http://132.250.60.1:5010"
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";

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
    iframe.src = url;

    setInterval(function() {

        iframe.src = url;
        iframe.contentWindow.postMessage('sessionState', url);

    }, 100);

});