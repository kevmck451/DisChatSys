

class MessageBroker:
    def __init__(self):
        self.rooms = {}

    def create_room(self, room_name):
        if room_name not in self.rooms:
            self.rooms[room_name] = []
            print(f"Room '{room_name}' created.")
        else:
            print(f"Room '{room_name}' already exists.")

    def send_message(self, room_name, message):
        if room_name in self.rooms:
            self.rooms[room_name].append(message)
            print(f"Message sent to room '{room_name}': {message}")
        else:
            print(f"Room '{room_name}' does not exist.")

    def get_messages(self, room_name):
        if room_name in self.rooms:
            return self.rooms[room_name]
        else:
            return []

# Example usage:
if __name__ == "__main__":
    broker = MessageBroker()
    broker.create_room("General")
    broker.send_message("General", "Hello World!")
    print(broker.get_messages("General"))
