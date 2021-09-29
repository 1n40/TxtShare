// Function for HTTP GET 
function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

// Function to throw the suggestion 
function suggest() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/suggest", false); // false for synchronous request
    xmlHttp.send(num + "&" + document.getElementById("edit").value);
    // return xmlHttp.responseText;
}

// Prompt function to confirm the sign
function sign() {
    ans = prompt("Do you want to sign this?\nYES/NO\n" + document.getElementById("shared").innerHTML)
    if (ans == "YES") {
        confirm()
    }
}

// Confirmation sent to API
function confirm() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/lock", false);
    xmlHttp.send(num);
}

// Function to see the document
function seedoc() {
    location.replace("http://127.0.0.1:5000/read")
}

// Time loop to update the document dynamically
var interval = setInterval(function () {
    document.getElementById("shared").innerHTML = httpGet("http://127.0.0.1:5000/read")
}, 5000);
