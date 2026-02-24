import tkinter as tk
from ui import RecipeManagerGUI


def main():
    # Initialize the main window (the 'Root')
    root = tk.Tk()

    # Initialize your GUI class from the ui module
    app = RecipeManagerGUI(root)

    # Start the event loop (Equivalent to iced::Result return in Rust)
    root.mainloop()

if __name__ == "__main__":
    main()
