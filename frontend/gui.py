import customtkinter as ctk
import asyncio
import websockets
import json
import threading
from datetime import datetime

# Set up customtkinter appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Chat System")
        self.root.geometry("700x500")

        # Main frames with better visual separation
        left_frame = ctk.CTkFrame(root, width=200, corner_radius=10)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

        right_frame = ctk.CTkFrame(root, width=400, corner_radius=10)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Left Frame: Control Area
        ctk.CTkLabel(left_frame, text="Username:").pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(left_frame)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Room ID:").pack(pady=(10, 0))
        self.room_entry = ctk.CTkEntry(left_frame)
        self.room_entry.pack(pady=5)

        ctk.CTkButton(left_frame, text="Connect", command=self.connect).pack(pady=10)

        ctk.CTkLabel(left_frame, text="Room:").pack(pady=(10, 0))
        self.room_label = ctk.CTkLabel(left_frame, text="")
        self.room_label.pack()

        ctk.CTkLabel(left_frame, text="Active Users:").pack(pady=(20, 0))
        self.user_list_display = ctk.CTkTextbox(left_frame, height=100, width=180, state='disabled')
        self.user_list_display.pack(pady=5)

        ctk.CTkButton(left_frame, text="Leave Room", command=self.leave_room).pack(pady=10)

        # Right Frame: Chat Area
        self.chat_display = ctk.CTkTextbox(right_frame, height=300, width=380, state='disabled')
        self.chat_display.pack(pady=10, padx=10)

        self.message_entry = ctk.CTkEntry(right_frame, width=300)
        self.message_entry.pack(side="left", pady=5, padx=(10, 5))
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        ctk.CTkButton(right_frame, text="Send", command=self.send_message).pack(side="right", padx=10)

        # WebSocket and asyncio loop
        self.websocket = None
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    async def listen_to_server(self):
        async for message in self.websocket:
            self.display_message(message)

    def display_message(self, message):
        # Enable editing to make modifications
        self.chat_display.configure(state='normal')

        # Check for specific conditions to clear the chat display
        if "Room switched" in message or "Welcome to room" in message:  # Adjust conditions as per your logic
            self.chat_display.delete("1.0", "end")  # Clear existing chat history

        # Check if the message contains the user list
        if message.startswith("System: Users in room:"):
            user_list = message.split(": ")[2]  # Extract the user list portion
            self.user_list_display.configure(state='normal')
            self.user_list_display.delete("1.0", "end")  # Clear the current user list
            self.user_list_display.insert("end", user_list)  # Update the user list
            self.user_list_display.configure(state='disabled')
        elif message.startswith("System:"):
            # Display other system messages
            timestamp = datetime.now().strftime('%I:%M %p')  # 12-hour format with AM/PM
            self.chat_display.insert("end", f"[{timestamp}] {message}\n")
        else:
            # Display normal chat messages
            timestamp = datetime.now().strftime('%I:%M %p')  # 12-hour format with AM/PM
            self.chat_display.insert("end", f"[{timestamp}] {message}\n")

        # Auto-scroll to the latest message
        self.chat_display.yview("end")

        # Disable editing after inserting messages
        self.chat_display.configure(state='disabled')

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
        self.room_label.configure(text=f"Room: {self.room_entry.get()}")

        self.chat_display.configure(state='normal')  # Enable editing
        self.chat_display.delete("1.0", "end")  # Clear all text
        self.chat_display.configure(state='disabled')  # Disable editing back

        asyncio.run_coroutine_threadsafe(self.connect_to_server(), self.loop)

    def send_message(self):
        message = json.dumps({
            "action": "message",
            "username": self.username_entry.get(),
            "message": self.message_entry.get()
        })
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.send(message), self.loop)
        self.message_entry.delete(0, "end")

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
    root = ctk.CTk()
    client = ChatClient(root)
    root.mainloop()
