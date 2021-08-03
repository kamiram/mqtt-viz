import asyncio
import json
from datetime import datetime
from aiohttp import web
import socketio
from asyncio_mqtt import Client

import config_local as conf

loop = asyncio.get_event_loop()

app = web.Application()
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')

last_active_time = dict()


async def emit_update_socket(data):
    await sio.emit('sensor_update', dict(data))


async def update_socket(request):
    data = await request.post()
    loop.create_task(emit_update_socket(data))
    return web.Response(text="Try to emit update")


app.add_routes([web.post('/update_sensor', update_socket)])


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
