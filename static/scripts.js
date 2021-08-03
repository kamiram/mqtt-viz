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
      var fields = ['number', 'pressform', 'model', 'product', 'cnt_sockets', 'active_sockets', 'cycle_time'];
      for(var i=0; i < data.length; i++){
        for(var j=0; j < fields.length; j++){
             $(`#block-${data[i].id} .value-${fields[j]}`).html(data[i][fields[j]]);
        }
        $(`#block-${data[i].id}`).attr('class', `block status-${data[i].status_color}`);
      }
    });
}

function initSystem(socketServerUrl, httpServerUrl){
  loadData(httpServerUrl);
  ioClient = io.connect(socketServerUrl);
  ioClient.on("connect", socket => {
    console.log("connected to server " + socketServerUrl);
    ioClient.emit("message", {data: "connected"});
    ioClient.on("active_time_update", function(msg) {
        $(`#block-${msg.id}`).attr('class', `block`);
        var cycle_time = parseFloat($(`#block-${msg.id} .value-cycle_time`).html());
        $(`#block-${msg.id} .value-cycle_active_time`).html(Math.round(msg.cycle_active_time*100)/100);
        var statusColor = "";

        if(msg.cycle_active_time <= cycle_time*1.2){
            statusColor = 'green';
        }else if(msg.cycle_active_time <= cycle_time*2){
            statusColor = 'yellow';
        }else{
            statusColor = 'yellow status-blink';
        }
        $(`#block-${msg.id}`).addClass(`status-${statusColor}`)
    });
  });
}

