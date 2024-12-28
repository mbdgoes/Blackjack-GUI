import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk
from gui import BlackjackGUI

# Fixture para iniciar a GUI
@pytest.fixture(autouse=True)
def gui():
    root = Tk()
    root.withdraw()  # Esconde a janela
    with patch('tkinter.messagebox.showinfo'), \
         patch('tkinter.messagebox.showerror'):  # Suprime as mensagens que a GUI manda
        app = BlackjackGUI(root)
        yield app
        root.destroy() # Destrutor da janela

# Testa estado inicial da GUI
def test_gui_initial_state(gui):
    assert gui.game.player_chips == 5000
    assert gui.game.current_bet == 0
    assert gui.bet_label.cget("text") == "Please place your bet to start the game."

# Testa se a GUI apresenta uma mensagem de erro com uma aposta inválida
def test_place_invalid_bet(gui):
    with patch('tkinter.messagebox.showerror') as mock_error:
        gui.place_bet(6000)
        mock_error.assert_called_once()

# Testa o botão de hit na GUI
def test_hit_button(gui):
    gui.place_bet(100)
    initial_cards = len(gui.game.player_hand)
    gui.hit()
    assert len(gui.game.player_hand) == initial_cards + 1

# Testa o botão de stand na GUI
def test_stand_button(gui):
    gui.place_bet(100)
    gui.stand()
    assert gui.game.game_over is True

# Testa o botão de reset na GUI
def test_reset_game(gui):
    gui.place_bet(100)
    gui.reset_game()
    assert gui.game.player_chips == 5000
    assert gui.game.current_bet == 0

# Testa na GUI se os status são chamados
def test_show_stats(gui):
    with patch('tkinter.messagebox.showinfo') as mock_info:
        gui.show_stats()
        mock_info.assert_called_once()

# Testa os logs na GUI se são chamados
def test_save_logs(gui):
    with patch('tkinter.messagebox.showinfo') as mock_info:
        gui.save_logs()
        mock_info.assert_called_once()
    os.remove("game_logs.txt")

# Confere se os botões estão desabilitados dependendo do estado
def test_button_states_after_bet(gui):
    gui.place_bet(100)
    assert gui.hit_button['state'] == 'normal'
    assert gui.stand_button['state'] == 'normal'
    assert gui.bet_button_100['state'] == 'disabled'

# Confere se ao final do jogo está desabilitado os botões
def test_end_game_updates(gui):
    gui.place_bet(100)
    with patch('tkinter.messagebox.showinfo'):
        gui.end_game("Player wins!")
        assert gui.bet_button_100['state'] == 'normal'
        assert gui.hit_button['state'] == 'disabled'

# Testa múltiplas rodadas seguidas
def test_multiple_game_rounds(gui):
    initial_chips = gui.game.player_chips
    gui.place_bet(100)
    gui.end_game("Player wins!")
    assert gui.game.player_chips > initial_chips
    
    gui.place_bet(200)
    gui.end_game("Dealer wins!")
    assert gui.game.player_chips < initial_chips

# Testa se o label de fichas atualiza corretamente
def test_chips_label_updates(gui):
    gui.place_bet(500)
    assert gui.chips_label.cget("text") == "Chips: 4500"
    gui.end_game("Player wins!")
    assert gui.chips_label.cget("text") == "Chips: 5500"

# Testa se a mesa limpa após reset
def test_table_clear_after_reset(gui):
    gui.place_bet(100)
    gui.hit()
    gui.reset_game()
    assert len(gui.game.player_hand) == 0
    assert len(gui.game.dealer_hand) == 0

# Testa se a quantidade de fichas é atualizada na GUI
def test_gui_chip_display_update(gui):
    initial_text = gui.chips_label.cget("text")
    gui.bet_button_500.invoke()
    final_text = gui.chips_label.cget("text")
    assert initial_text != final_text
    assert "4500" in final_text
