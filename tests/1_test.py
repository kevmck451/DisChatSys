import asyncio
import websockets

async def client_simulation(room_id, message):
    uri = f"ws://localhost:6789/{room_id}"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        print(await websocket.recv())

async def test_message_broker():
    # Simulate two clients connecting to the same room
    await asyncio.gather(
        client_simulation("room1", "Hello from Client 1"),
        client_simulation("room1", "Hello from Client 2")
    )

if __name__ == "__main__":
    asyncio.run(test_message_broker())
