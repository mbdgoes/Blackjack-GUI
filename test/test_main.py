from unittest.mock import patch
import tkinter as tk
from main import main

def test_main_execution():
    with patch("main.tk.Tk") as mock_tk:
        mock_root = mock_tk.return_value
        with patch("main.BlackjackGUI") as mock_gui:
            main()
            mock_gui.assert_called_once_with(mock_root)
            mock_root.mainloop.assert_called_once()