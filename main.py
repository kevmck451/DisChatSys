
import customtkinter as ctk
from frontend.gui import ChatClient




if __name__ == "__main__":

    root = ctk.CTk()
    client = ChatClient(root)
    root.mainloop()


