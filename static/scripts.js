function initSocketIO(serverUrl){
  ioClient = io.connect(serverUrl);
  ioClient.on("connect", socket => {
    console.log("connected to server " + serverUrl);
    ioClient.emit("message", {data: "connected"});
    ioClient.on("message", function(msg) {
        console.log(msg);
        if(msg.hasOwnProperty("status_blink") && msg.status_blink){
            document.getElementById(`block-${msg.id}`).classList.add("blink");
        } else {
            document.getElementById(`block-${msg.id}`).classList.remove("blink");
        }
        var fields = [
            'type', 'model', 'number', 'product', 'pressform', 'cnt_sockets_extra',
            'status', 'mqtt_label', 'cycle_active_time', 'cycle_active_time'
        ];
        if(msg.hasOwnProperty("status_color")){
            document.getElementById(`block-${msg.id}`).style.backgroundColor = msg.status_color;
        }
        for(var i = 0; i < fields.length; i++){
            if(msg.hasOwnProperty(fields[i]) && document.getElementById(`value-${fields[i]}-${msg.id}`)){
                document.getElementById(`value-${fields[i]}-${msg.id}`).innerText = msg[fields[i]];
            }
        }
    });
  });
}

