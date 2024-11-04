import tkinter as tk
from tkinter import scrolledtext
import asyncio
import websockets
import json
import threading

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Chat System")

        # User entry fields
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Room ID:").pack()
        self.room_entry = tk.Entry(root)
        self.room_entry.pack()

        tk.Button(root, text="Connect", command=self.connect).pack()

        tk.Label(root, text="Room ID:").pack()
        self.room_label = tk.Label(root, text="")
        self.room_label.pack()

        tk.Label(root, text="Active Users:").pack()
        self.user_list_display = scrolledtext.ScrolledText(root, height=5, state='disabled')
        self.user_list_display.pack()

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, state='disabled')
        self.chat_display.pack()

        # Message entry
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack()
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        # Connect, Leave, and Send buttons
        tk.Button(root, text="Send", command=self.send_message).pack()
        tk.Button(root, text="Leave Room", command=self.leave_room).pack()


        # WebSocket and asyncio loop
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    async def listen_to_server(self):
        async for message in self.websocket:
            self.display_message(message)

    def display_message(self, message):
        self.chat_display.config(state='normal')

        # Check if the message contains the user list
        if message.startswith("System: Users in room:"):
            self.user_list_display.config(state='normal')
            user_list = message.split(": ")[2]  # Extracts the user list portion
            self.user_list_display.delete(1.0, tk.END)
            self.user_list_display.insert(tk.END, user_list)
            self.user_list_display.config(state='disabled')
        elif message.startswith("System:"):
            # Display other system messages
            self.chat_display.insert(tk.END, message + "\n", "system")
            self.chat_display.tag_config("system", foreground="blue")
        else:
            # Display regular chat messages
            self.chat_display.insert(tk.END, message + "\n")

        self.chat_display.yview(tk.END)
        self.chat_display.config(state='disabled')

    async def connect_to_server(self):
        uri = f"ws://localhost:6789/{self.room_entry.get()}"
        self.websocket = await websockets.connect(uri)

        # Send join message
        join_message = json.dumps({
            "action": "join",
            "username": self.username_entry.get()
        })
        await self.websocket.send(join_message)

        # Start listening in the background
        await self.listen_to_server()

    def connect(self):
        self.room_label.config(text=f"Room: {self.room_entry.get()}")
        asyncio.run_coroutine_threadsafe(self.connect_to_server(), self.loop)

    def send_message(self):
        message = json.dumps({
            "action": "message",
            "username": self.username_entry.get(),
            "message": self.message_entry.get()
        })
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.send(message), self.loop)
        self.message_entry.delete(0, tk.END)

    async def leave_room_async(self):
        # Send leave message to server
        if self.websocket:
            leave_message = json.dumps({
                "action": "leave",
                "username": self.username_entry.get()
            })
            await self.websocket.send(leave_message)
            await self.websocket.close()
            self.websocket = None
        self.display_message("System: You left the room.")

    def leave_room(self):
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.leave_room_async(), self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
