from game import BlackjackGame

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
