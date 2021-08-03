import asyncio
import signal
from gmqtt import Client as MQTTClient


import config_local

import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
STOP = asyncio.Event()


def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe(config_local.MQTT_TOPIC + '/#', qos=0)


def on_message(client, topic, payload, qos, properties):
    print('RECV MSG:', payload)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')


def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')


def ask_exit(*args):
    STOP.set()


async def main():
    client = MQTTClient("viz")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    client.set_auth_credentials(username=config_local.MQTT_USERNAME, password=config_local.MQTT_PASSWORD)
    await client.connect(
        config_local.MQTT_BROKER_URL,
        port=config_local.MQTT_BROKER_PORT,
        keepalive=config_local.MQTT_KEEPALIVE
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    await main()

    loop.run_until_complete()