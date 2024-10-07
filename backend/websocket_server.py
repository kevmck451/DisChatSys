


from message_broker import MessageBroker

import asyncio
import websockets


broker = MessageBroker()


async def handler(websocket, path):
    room_name = await websocket.recv()  # Receive the room name first
    broker.create_room(room_name)

    try:
        while True:
            message = await websocket.recv()
            broker.send_message(room_name, message)
            await websocket.send(f"Message '{message}' delivered to {room_name}")
    except websockets.ConnectionClosed:
        print(f"Connection to room {room_name} closed.")


start_server = websockets.serve(handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
