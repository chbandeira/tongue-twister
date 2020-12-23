"use strict"

let id = val => document.getElementById(val),
    ul = id("ul"),
    gUMbtn = id("gUMbtn"),
    start = id("start"),
    stop = id("stop"),
    stream,
    recorder,
    counter = 1,
    chunks,
    media,
    message = id("message");

let enableMic = function () {
    media = {
        tag: "audio",
        type: "audio/webm",
        ext: ".webm",
        gUM: { audio: true }
    };
    navigator.mediaDevices.getUserMedia(media.gUM).then(_stream => {
        stream = _stream;
        id("btns").style.display = "inherit";
        start.removeAttribute("disabled");
        recorder = new MediaRecorder(stream);
        recorder.ondataavailable = e => {
            chunks.push(e.data);
            if (recorder.state == "inactive") update();
        };
    });
}

gUMbtn.onclick = enableMic();

start.onclick = e => {
    start.disabled = true;
    message.innerText = "Listening..."
    stop.removeAttribute("disabled");
    chunks = [];
    recorder.start();
}

stop.onclick = e => {
    stop.disabled = true;
    message.innerText = "Checking..."
    recorder.stop();
    start.removeAttribute("disabled");
}

function update() {
    let blob = new Blob(chunks, { type: media.type })
        , url = URL.createObjectURL(blob)
        , li = document.createElement("li")
        , mt = document.createElement(media.tag)
        , hf = document.createElement("a")
        ;
    mt.controls = true;
    mt.src = url;
    hf.href = url;
    li.appendChild(mt);
    li.appendChild(hf);

    if (ul.children.length == 0) {
        ul.appendChild(li);
    }
    else {
        ul.replaceChild(li, ul.children.item(0));
    }

    var formData = new FormData();
    formData.append("file", blob, "audio.webm");

    var request = new XMLHttpRequest();
    request.open("POST", "/check");
    request.responseType = "json";
    request.send(formData);

    // Define what happens on successful data submission
    request.addEventListener("load", function (event) {
        document.getElementById("phrase").innerHTML = request.response["phrase"];
        document.getElementById("message").innerHTML = request.response["speech"];
        document.getElementById("score").innerText = request.response["score"];
        document.getElementById("total").innerText = request.response["total"];
        document.getElementById("next").classList.remove("disabled");
    });

    // Define what happens in case of error
    request.addEventListener("error", function (event) {
        document.getElementById("message").innerHTML = request.response["speech"];
    });
}

enableMic.call();