// Function to send username and password to auth API and recieve a cookie based on it
function send() {
    let data = document.getElementById("usr").value + "&" + document.getElementById("passwd").value

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/auth", false); // false for synchronous request
    xmlHttp.send(data);
    let rcv = xmlHttp.responseText
    if (rcv != "false") {
        if (rcv.includes("master")) {
            rcv = rcv.substr(0, rcv.indexOf("master"))
            document.cookie = "id=" + rcv
            location.replace("http://127.0.0.1:5000/master")
        }
        else if (rcv.includes("user")) {
            rcv = rcv.substr(0, rcv.indexOf("user"))
            document.cookie = "id=" + rcv
            location.replace("http://127.0.0.1:5000/user")
        }
        else {
            location.reload()
        }

        // console.log(rcv)
    }

};