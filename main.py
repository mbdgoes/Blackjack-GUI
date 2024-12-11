import tkinter as tk
from gui import BlackjackGUI

def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()