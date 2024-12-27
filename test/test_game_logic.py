import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from game import BlackjackGame, Card, Deck, PlayerStats

# verificar a funcionalidade de apostas, incluindo valores válidos e inválidos
def test_place_bet():
    game = BlackjackGame()
    initial_chips = game.get_player_chips()

    bet_amount = 500
    result = game.place_bet(bet_amount)

    assert result == f"Bet placed: {bet_amount}"
    assert game.current_bet == bet_amount
    assert game.get_player_chips() == initial_chips - bet_amount

    result_invalid = game.place_bet(initial_chips + 1000)
    assert result_invalid == "Invalid bet amount."

# Representação textual de uma carta
def test_card_representation():
    card = Card("Hearts", "Ace", 11)
    assert repr(card) == "Ace of Hearts"

# Confere se a geração do nome do arquivo está correta
def test_card_image_filename():
    card = Card("Diamonds", "Queen", 10)
    assert card.get_image_filename() == "Queen of Diamonds.png"

# Inicialização do baralho
def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52

# Checar embaralhamento
def test_deck_shuffle():
    deck1 = Deck()
    deck2 = Deck()
    assert deck1.cards != deck2.cards

# Verificar se uma carta é removida do baralho ao ser comprada
def test_draw_card():
    deck = Deck()
    card = deck.draw_card()
    assert card is not None
    assert len(deck.cards) == 51

# Calcular o valor da mão com Áses -> verifica se vale 11 ou 1
def test_calculate_hand_value_with_aces():
    game = BlackjackGame()
    hand = [Card("Hearts", "Ace", 11), Card("Spades", "Ace", 11)]
    assert game.calculate_hand_value(hand) == 12

# Valor de uma mão sem Áses
def test_calculate_hand_value_no_aces():
    game = BlackjackGame()
    hand = [Card("Hearts", "Ten", 10), Card("Diamonds", "Nine", 9)]
    assert game.calculate_hand_value(hand) == 19

# Valor de uma mão com múltiplos Áses
def test_calculate_hand_value_multiple_aces():
    game = BlackjackGame()
    hand = [Card("Hearts", "Ace", 11), Card("Spades", "Ace", 11), Card("Clubs", "Nine", 9)]
    assert game.calculate_hand_value(hand) == 21

# Checar apostas com valores inválidos
def test_place_bet_invalid_amount():
    game = BlackjackGame()
    result = game.place_bet(-100)
    assert result == "Invalid bet amount."

# Verificar a inicialização do jogo
def test_blackjack_game_initialization():
    game = BlackjackGame()
    assert len(game.deck.cards) == 52
    assert game.player_chips == 5000
    assert game.current_bet == 0
    assert not game.game_over

# Verificar as mãos iniciais dos jogadores
def test_start_game_initial_hands():
    game = BlackjackGame()
    game.start_game()
    assert len(game.player_hand) == 2
    assert len(game.dealer_hand) == 2

# Verifica Blackjack imediato para o dealer indica derrota imediata
def test_start_game_blackjack():
    game = BlackjackGame()
    game.deck.cards = [
        Card("Hearts", "Ace", 11),
        Card("Spades", "Jack", 10),
        Card("Diamonds", "Nine", 9),
        Card("Clubs", "Eight", 8),
    ]
    result = game.start_game()
    assert result == "Dealer has Blackjack! You lose."
    assert game.game_over

# Verificar se uma carta é adicionada corretamente ao dar "Hit"
def test_hit_adds_card():
    game = BlackjackGame()
    game.start_game()
    initial_hand_size = len(game.player_hand)
    game.hit(game.player_hand)
    assert len(game.player_hand) == initial_hand_size + 1

# Confere se valor total da mão cresce após o Hit
def test_hand_value_after_hit():
    game = BlackjackGame()
    game.start_game()
    initial_value = game.calculate_hand_value(game.player_hand)
    game.hit(game.player_hand)
    new_value = game.calculate_hand_value(game.player_hand)
    assert new_value >= initial_value

# Testa se o dealer dá Stand quando tem 17 
def test_dealer_stands_on_soft_17():
    game = BlackjackGame()
    game.dealer_hand = [Card("Hearts", "Ace", 11), Card("Spades", "Six", 6)]
    game.stand()
    assert game.calculate_hand_value(game.dealer_hand) == 17
    assert game.game_over

# Checa se o player perde ao ultrapassar de 21
def test_check_winner_player_busts():
    game = BlackjackGame()
    game.player_hand = [Card("Hearts", "Ten", 10), Card("Diamonds", "Nine", 9), Card("Clubs", "Five", 5)]
    result = game.check_winner()
    assert result == "Dealer wins! Player busted."

# Checa se o dealer perde ao ultrapassar de 21
def test_check_winner_dealer_busts():
    game = BlackjackGame()
    game.dealer_hand = [Card("Hearts", "Ten", 10), Card("Diamonds", "Nine", 9), Card("Clubs", "Five", 5)]
    result = game.check_winner()
    assert result == "Player wins! Dealer busted."

# Verificar o comportamento do jogo em caso de empate
def test_check_winner_tie():
    game = BlackjackGame()
    game.player_hand = [Card("Hearts", "Ten", 10), Card("Diamonds", "Nine", 9)]
    game.dealer_hand = [Card("Clubs", "Ten", 10), Card("Spades", "Nine", 9)]
    result = game.check_winner()
    assert result == "It's a tie!"

# Apostas superiores ao total de fichas devem ser inválidas
def test_place_bet_exceeding_chips():
    game = BlackjackGame()
    result = game.place_bet(6000)
    assert result == "Invalid bet amount."

# Apostas com valor zero devem ser inválidas
def test_place_bet_zero_amount():
    game = BlackjackGame()
    result = game.place_bet(0)
    assert result == "Invalid bet amount."

# Checa se a aposta é dobrada quando jogador ganha e adiciona ao valor das fichas
def test_settle_bet_player_wins():
    game = BlackjackGame()
    game.place_bet(500)
    game.settle_bet("Player wins!")
    assert game.get_player_chips() == 5500

# Lógica de empate ao ajustar as fichas do jogador
def test_settle_bet_tie():
    game = BlackjackGame()
    game.place_bet(500)
    game.settle_bet("It's a tie!")
    assert game.player_chips == 5000

# Verifica se o jogador perde as fichas ao perder
def test_settle_bet_dealer_wins():
    game = BlackjackGame()
    game.place_bet(500)
    game.settle_bet("Dealer wins!")
    assert game.player_chips == 4500

# Testa se as fichas resetam ao resetar o jogo
def test_reset_chips():
    game = BlackjackGame()
    game.player_chips = 3000
    game.reset_chips()
    assert game.player_chips == 5000

# Checa se não consegue comprar cartas de um baralho vazio
def test_draw_card_from_empty_deck():
    game = BlackjackGame()
    game.deck.cards = []
    card = game.deck.draw_card()
    assert card is None

# Testa se o dealer não recebe mais cartas após o Stand
def test_stand_dealer_logic():
    game = BlackjackGame()
    game.start_game()
    initial_dealer_hand_size = len(game.dealer_hand)
    game.stand()
    assert len(game.dealer_hand) >= initial_dealer_hand_size

# Testa se ao iniciar um novo jogo reseta a mão
def test_start_new_game_resets_state():
    game = BlackjackGame()
    game.start_game()
    game.player_hand.append(Card("Hearts", "Ace", 11))
    game.start_game()
    assert len(game.player_hand) == 2
    assert len(game.dealer_hand) == 2

# Testa se os status estão sendo mostrados corretamente
def test_display_player_stats():
    game = BlackjackGame()
    game.stats.record_win()
    stats = game.display_stats()
    assert "Wins: 1" in stats
    assert "Losses: 0" in stats

# Testa varias sessoes do jogo simultaneas
def test_multiple_game_sessions():
    stats = PlayerStats()
    stats.new_session()
    stats.new_session()
    assert stats.sessions_played == 2

# Verifica se não pode haver aposta após o fim do jogo
def test_place_bet_game_over():
    game = BlackjackGame()
    game.game_over = True
    result = game.place_bet(500)
    assert result == "Cannot place a bet; the game is over."