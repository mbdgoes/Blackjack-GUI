import tkinter as tk
from gui import BlackjackGUI

def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.geometry("1280x720")
    root.mainloop()

if __name__ == "__main__":
    main()