import asyncio
import websockets
import json
from collections import defaultdict
import motor.motor_asyncio

class MessageBroker:
    def __init__(self):
        self.rooms = defaultdict(set)
        self.users = defaultdict(set)  # Track users by room
        self.client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["chat_db"]

    async def save_message(self, room_id, message):
        #S ave message to MongoDB
        await self.db.messages.insert_one({"room_id": room_id, "message": message})

    async def load_history(self, room_id):
        # Load message history from MongoDB
        history = []
        async for doc in self.db.messages.find({"room_id": room_id}).sort("_id", -1).limit(10):
            history.append(doc["message"])
        return history[::-1]  # Reverse to display oldest messages first

    async def connect(self, websocket, room_id, username):
        # Add a client to a room
        self.rooms[room_id].add(websocket)
        self.users[room_id].add(username)
        await self.broadcast(f"System: {username} joined the room.", room_id)
        history = await self.load_history(room_id)
        for message in history:
            await websocket.send(message)
        await self.update_user_list(room_id)


    async def disconnect(self, websocket, room_id, username):
            # Remove a client from a room
            self.rooms[room_id].discard(websocket)
            self.users[room_id].discard(username)
            await self.broadcast(f"System: {username} left the room.", room_id)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                del self.users[room_id]
            else:
                await self.update_user_list(room_id)


    async def update_user_list(self, room_id):
        user_list_message = f"Users in room: {', '.join(self.users[room_id])}"
        await self.broadcast(f"System: {user_list_message}", room_id)


    async def broadcast(self, message, room_id):
        disconnected_clients = []
        for client in self.rooms[room_id].copy():
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client)
        for client in disconnected_clients:
            if client in self.rooms[room_id]:
                self.rooms[room_id].remove(client)

    async def handle_message(self, websocket, room_id, data):
        action = data.get("action")
        username = data.get("username")
        message = data.get("message", "")

        if action == "join":
            await self.connect(websocket, room_id, username)
        elif action == "leave":
            await self.disconnect(websocket, room_id, username)
        elif action == "message":
            full_message = f"{username}: {message}"
            await self.save_message(room_id, full_message)  # Save message to history
            await self.broadcast(full_message, room_id)

    async def handler(self, websocket, path):
        room_id = path.strip("/")
        try:
            async for message in websocket:
                data = json.loads(message)
                await self.handle_message(websocket, room_id, data)
        except websockets.ConnectionClosed:
            pass
        finally:
            username = "Unknown"  # Handle disconnect without data
            if "username" in data:
                username = data["username"]
            await self.disconnect(websocket, room_id, username)


async def main():
    broker = MessageBroker()
    async with websockets.serve(broker.handler, "localhost", 6789):
        await asyncio.Future()


if __name__ == "__main__":
    print('message broker running')
    asyncio.run(main())
