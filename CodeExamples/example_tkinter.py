import tkinter as tk

# 1. Create the main application window
root = tk.Tk()
root.title("Hello World App")
root.geometry("300x150") # Set the window size

# 2. Add a label widget
label = tk.Label(root, text="Hello, world!")
label.pack(pady=20) # Position the label in the window with padding

# 3. Start the event loop
root.mainloop()
