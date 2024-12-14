import pytest
from tkinter import Tk
from gui import BlackjackGUI

@pytest.fixture
def gui_app():
    # Cria um root Tkinter válido para os testes
    root = Tk()
    app = BlackjackGUI(root)
    return app, root

def test_gui_initial_state(gui_app):
    app, root = gui_app
    # Testa o estado inicial da GUI
    assert app.game.player_chips == 5000
    assert app.game.current_bet == 0
    assert app.bet_label.cget("text") == "Please place your bet to start the game."
    root.destroy()

def test_gui_place_bet(gui_app):
    app, root = gui_app
    # Simula a lógica da aposta
    app.place_bet(100)
    assert app.game.current_bet == 100
    assert app.bet_label.cget("text") == "Bet Amount: 100"
    root.destroy()

def test_gui_reset_game(gui_app):
    app, root = gui_app
    # Simula o reset do jogo
    app.game.player_chips = 3000
    app.reset_game()
    assert app.game.player_chips == 5000
    assert app.bet_label.cget("text") == "Please place your bet to start the game."
    root.destroy()
