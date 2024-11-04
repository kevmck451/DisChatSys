# Distributed Chat System Setup and Implementation Plan

## Objective
Develop a scalable, distributed chat system with real-time communication using WebSockets, a custom message broker, and a Tkinter-based Python GUI. The system will support multiple users, chat rooms, and both horizontal and vertical scaling.

---

## Steps to Start

### 1. Setup Project Environment
- Install necessary Python libraries: `websockets`, `tkinter`, `pymongo` (or PostgreSQL library), and any other dependencies.
- Set up a project directory structure, including folders for:
  - **Server-side components**: Message broker, WebSocket handlers, user authentication.
  - **Client-side components**: Tkinter GUI, WebSocket client.
  - **Database**: MongoDB or PostgreSQL setup for user and chat data.

---

### 2. Build Custom Message Broker
- Create a basic message broker that:
  - Routes messages between users and chat rooms.
  - Supports horizontal scaling by adding more broker instances.
  - Implements a queue system (similar to RabbitMQ) for message distribution.

---

### 3. Implement WebSocket Communication
- Set up WebSocket server to handle real-time communication.
- Integrate WebSocket clients in the Tkinter GUI for users to send/receive messages.
- Ensure two-way, real-time message flow between users and chat rooms.

---

### 4. Develop Authentication System
- Build a simple user login/registration system.
- Store user credentials in the database (MongoDB or PostgreSQL).
- Implement token-based authentication to manage session persistence.

---

### 5. Create Tkinter GUI
- Design a simple chat interface with:
  - User login and registration options.
  - Chat room selection and messaging features.
  - Real-time message updates via WebSocket.

---

### 6. Test and Scale
- Start with a local single-server setup and test message flow.
- Simulate horizontal scaling by adding more server instances.
- Test performance under load to ensure scalability.

---


## Running

- open terminal and cd into database and run the start_db file
- run the message broker server
- open however many terminals and run 3_test.py to do gui
- or run main.py file


## Updates

- a list box under active users of rooms that are currently in use and then a user can click that room and switch to it that way as opposed to having to know the room number ahead of time
- when switching rooms, the chat should clear and new history loaded in
- can rooms be password projected?
- setting up user database and logging in







