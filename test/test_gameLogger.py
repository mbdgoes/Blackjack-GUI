# GameLogger Unit Tests
from unittest.mock import Mock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import GameLogger

# Testa inicialização da classe de Log
def test_logger_initialization():
    logger = GameLogger()
    assert logger.logs == []

# Verifica se está limpando os logs
def test_clear_logs():
    logger = GameLogger()
    logger.logs = [{"test": "data"}]
    logger.clear_logs()
    assert logger.logs == []

# Integração com o sistema de arquivos
def test_save_logs_to_file():
    logger = GameLogger()
    logger.logs = [{
        "player_hand": ["Ace of Hearts", "King of Spades"],
        "dealer_hand": ["Queen of Diamonds", "Jack of Clubs"],
        "result": "Player wins!"
    }]
    
    test_filename = "test_logs.txt"
    logger.save_logs_to_file(test_filename)
    
    assert os.path.exists(test_filename)
    with open(test_filename, "r") as file:
        content = file.read()
        assert "Game 1:" in content
        assert "Player Hand:" in content
        assert "Dealer Hand:" in content
    
    os.remove(test_filename)