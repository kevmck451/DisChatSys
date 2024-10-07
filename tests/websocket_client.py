

import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        await websocket.send("General")  # Join the "General" room
        await websocket.send("Hello from client!")
        response = await websocket.recv()
        print(f"Received from server: {response}")

asyncio.get_event_loop().run_until_complete(send_message())
