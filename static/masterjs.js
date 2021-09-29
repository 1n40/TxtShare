// Function to get suggestions 
function getSug() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "http://127.0.0.1:5000/getsuggestions", false); // false for synchronous request
    xmlHttp.send(null);
    res = xmlHttp.responseText
    return res;
}

// Function to update the document 
function update() {
    document.getElementById("edit").value = document.getElementById("sug1").innerHTML
}


// Function to delete the suggestion
function delsug() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/delsug", false); // false for synchronous request
    xmlHttp.send(document.getElementById("sug1").innerHTML);
    res = xmlHttp.responseText
    return res;
}

// Function to display the document
function seedoc() {
    location.replace("http://127.0.0.1:5000/read")
}

// Function to sign the document
function confirm() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:5000/lock", false);
    xmlHttp.send(num);
}

//    function highlight(){ 
//        document.getElementById("sug1").innerHTML(document.getElementById("shared").innerText().split('').map(function(val, i){
//        return val != document.getElementById("sug1").innerText().charAt(i) ?
//        "<span class='highlight'>"+val+"</span>" : 
//        val;            
//        }).join('')); 
//    }


let counter = 0;

// Time based loop
var interval = setInterval(function () {
    if (!counter) {
        // Copy both fields
        document.getElementById("shared").innerHTML = httpGet("http://127.0.0.1:5000/read")
        document.getElementById("edit").innerHTML = httpGet("http://127.0.0.1:5000/read")
        counter++;
    }


    // Update the resource
    if (document.getElementById("shared").innerHTML != document.getElementById("edit").value) {

        httpPost("http://127.0.0.1:5000/update")
        // console.log(document.getElementById("shared").innerHTM != document.getElementById("edit").value)
        document.getElementById("shared").innerHTML = httpGet("http://127.0.0.1:5000/read")
    }

    // Suggestions from API
    document.getElementById("sug1").innerHTML = getSug()

    // highlight();

}, 5000);

