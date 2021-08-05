#!/usr/bin/env python
import asyncio
import json
from datetime import datetime
import socketio
from aiohttp.web_middlewares import middleware
from aiohttp_wsgi import WSGIHandler
from asyncio_mqtt import Client
from aiohttp import web
from wsgi import flask_wsgi

import config_local as conf

loop = asyncio.get_event_loop()

app = web.Application()
sio = socketio.AsyncServer(async_mode='aiohttp')
wsgi_handler = WSGIHandler(flask_wsgi)

last_active_time = dict()


async def emit_update_socket(data):
    await sio.emit('sensor_update', json.loads(data))


@web.middleware
async def socketio_emit_middleware(request, handler):
    response = await handler(request)
    if 'X-SocketIO-Emit-SensorUpdate' in response.headers:
        loop.create_task(emit_update_socket(response.headers['X-SocketIO-Emit-SensorUpdate']))
    return response


app.middlewares.append(socketio_emit_middleware)

app.router.add_static('/static/', path='./static/', name='static')
app.router.add_route('*', '/{path_info:admin/.*}',  wsgi_handler)
app.router.add_route('*', '/{path_info:$}',  wsgi_handler)
app.router.add_route('*', '/{path_info:data.json}',  wsgi_handler)


async def mqtt_worker():
    async with Client(
                hostname=conf.MQTT_BROKER_HOST,
                port=conf.MQTT_BROKER_PORT,
                username=conf.MQTT_USERNAME,
                password=conf.MQTT_PASSWORD,
                keepalive=conf.MQTT_KEEPALIVE
            ) as client:
        async with client.unfiltered_messages() as messages:
            await client.subscribe(f'{conf.MQTT_TOPIC}/#')
            async for message in messages:
                message = json.loads(message.payload.decode())
                # print(json.dumps(message, indent=4))
                if message['value'] != 'OFF':
                    continue
                port = message['port']
                if port in last_active_time:
                    active_time = datetime.now().timestamp() - last_active_time[port]
                    data = {
                        'id': port,
                        'cycle_active_time': active_time,
                    }
                    await sio.emit('active_time_update', data)
                last_active_time[port] = datetime.now().timestamp()


if __name__ == '__main__':
    sio.attach(app)

    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, host='0.0.0.0', port=conf.SOCKET_SERVER_PORT)

    loop.create_task(site.start())
    loop.create_task(mqtt_worker())
    loop.run_forever()
