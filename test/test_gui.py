from unittest.mock import patch
import tkinter as tk
from gui import BlackjackGUI

def test_gui_initial_state():
    root = tk.Tk()
    app = BlackjackGUI(root)

    assert app.game.player_chips == 5000
    assert app.game.current_bet == 0
    assert app.bet_label.cget("text") == "Please place your bet to start the game."

    root.destroy()

def test_gui_place_bet():
    root = tk.Tk()
    app = BlackjackGUI(root)

    app.place_bet(100)
    assert app.game.current_bet == 100
    assert app.bet_label.cget("text") == "Bet Amount: 100"

    root.destroy()

def test_gui_reset_game():
    root = tk.Tk()
    app = BlackjackGUI(root)

    app.game.player_chips = 3000
    app.reset_game()
    assert app.game.player_chips == 5000
    assert app.bet_label.cget("text") == "Please place your bet to start the game."

    root.destroy()