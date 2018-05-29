document.addEventListener("DOMContentLoaded", function(event) {

    activeStuff = document.getElementById("active");
    inactiveStuff = document.getElementById("inactive");
    var url = "http://172.16.0.1:5010"
    var photoURL = "";
    iframe = document.getElementById("sessionState")
    iframe.style.display = "none";
    control = document.getElementById("control");
    control.style.display = "none";
    firstName = document.getElementById("firstName");
    lastName = document.getElementById("lastName");
    email = document.getElementById("email");
    countStatus = document.getElementById("countStatus");
    albumFrame = document.getElementById("albumFrame");
    albumFrame.style.display = "none";
    album = document.getElementById("album");
    data = "";
    token = "";
    cmd_sendEmail = document.getElementById("cmd_sendEmail");

    albumFrame.addEventListener("load", function() {
        iframe.contentWindow.postMessage('getPhotos', url);
    });

    handleResponse = function(e) {
        if(e.origin == url) 
        { 
            if (data != e.data)
            {
                data = e.data.split("|");
                console.log(data);
                if (data[0] == "active")
                {
                    if (data[2] == "Yes")
                    {
                        countStatus.innerHTML = data[3];
                        if (data[4] != "")
                        {
                            album.innerHTML = data[4];
                        }
                    }
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
        token = firstName.value + "_" + lastName.value + "_"
        var d = new Date();
        dtStamp = d.getFullYear() + ""
            + d.getMonth() + ""
            + d.getDay() + ""
            + d.getHours() + ""
            + d.getMinutes()

        token += dtStamp;
        control.src = "http://172.16.0.1:5010/session?state=active&token=" + token + "&email=" + encodeURI(email.value) + "&fname=" + encodeURI(firstName.value) + "&lname=" + encodeURI(lastName.value);
    });

    cmd_sendEmail.addEventListener("click", function() {
        alert("Iterate through email addresses, attach photos, make pretty with html stuff (if you have time), and INCLUDE FLAG THAT PHOTO WAS SENT... in case internet connection isnt available");
        alert("Oh, and find a way to include external storage");
        alert("Mount everything to wood or something");
    });

});