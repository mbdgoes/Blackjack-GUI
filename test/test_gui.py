import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk
from gui import BlackjackGUI

@pytest.fixture(autouse=True)
def gui():
    root = Tk()
    root.withdraw()  # Hide the window
    with patch('tkinter.messagebox.showinfo'), \
         patch('tkinter.messagebox.showerror'):  # Suppress all message boxes
        app = BlackjackGUI(root)
        yield app
        root.destroy()

def test_gui_initial_state(gui):
    app = gui
    assert app.game.player_chips == 5000
    assert app.game.current_bet == 0
    assert app.bet_label.cget("text") == "Please place your bet to start the game."

    
def test_place_valid_bet(gui):
    app = gui
    app.place_bet(100)
    assert app.game.current_bet == 100
    assert app.game.player_chips == 4900


def test_place_invalid_bet(gui):
    app = gui
    with patch('tkinter.messagebox.showerror') as mock_error:
        app.place_bet(6000)
        mock_error.assert_called_once()


def test_hit_button(gui):
    app = gui
    app.place_bet(100)
    initial_cards = len(app.game.player_hand)
    app.hit()
    assert len(app.game.player_hand) == initial_cards + 1


def test_stand_button(gui):
    app = gui
    app.place_bet(100)
    app.stand()
    assert app.game.game_over is True


def test_reset_game(gui):
    app = gui
    app.place_bet(100)
    app.reset_game()
    assert app.game.player_chips == 5000
    assert app.game.current_bet == 0


def test_show_stats(gui):
    app = gui
    with patch('tkinter.messagebox.showinfo') as mock_info:
        app.show_stats()
        mock_info.assert_called_once()


def test_save_logs(gui):
    app = gui
    with patch('tkinter.messagebox.showinfo') as mock_info:
        app.save_logs()
        mock_info.assert_called_once()
    os.remove("game_logs.txt")


def test_button_states_after_bet(gui):
    app = gui
    app.place_bet(100)
    assert app.hit_button['state'] == 'normal'
    assert app.stand_button['state'] == 'normal'
    assert app.bet_button_100['state'] == 'disabled'


def test_end_game_updates(gui):
    app = gui
    app.place_bet(100)
    with patch('tkinter.messagebox.showinfo'):
        app.end_game("Player wins!")
        assert app.bet_button_100['state'] == 'normal'
        assert app.hit_button['state'] == 'disabled'