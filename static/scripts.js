function loadData(httpServerUrl){
    $.ajax({
      type: "POST",
      url: "/data.json",
      data: {}
    })
    .done(function( data ) {
      var blocks = [];
      var template = $('#sensorTemlate').html();
      for(var i=0; i < data.length; i++){
        var block = template;
        block=block.replace('{sensor.id}', data[i].id)
        blocks.push(block);
      }
      $('#content').html(blocks.join(''));
      var fields = ['number', 'pressform', 'model', 'product', 'cnt_sockets', 'active_sockets'];
      for(var i=0; i < data.length; i++){
        for(var j=0; j < fields.length; j++){
             $(`#block-${data[i].id} .value-${fields[j]}`).html(data[i][fields[j]]);
        }
      }
    });
}
function initSystem(socketServerUrl, httpServerUrl){
  loadData(httpServerUrl);
  ioClient = io.connect(socketServerUrl);
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

