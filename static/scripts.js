function initSocketIO(serverUrl){
  ioClient = io.connect(serverUrl);
  ioClient.on("connect", socket => {
    console.log("connected to server " + serverUrl);
    ioClient.emit("message", {data: "connected"});
    ioClient.on("message", function(msg) {
        console.log(msg);
        document.getElementById(`block-${msg.id}`).style.backgroundColor = msg.status_color;
        if(msg.status_blink){
            document.getElementById(`block-${msg.id}`).classList.add("blink");
        } else {
            document.getElementById(`block-${msg.id}`).classList.remove("blink");
        }
        document.getElementById(`value-cycle_active_time-${msg.id}`).innerText = msg.cycle_active_time;
    });
  });
}

