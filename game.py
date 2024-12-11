import random

class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_image_filename(self):
        return f"{self.rank} of {self.suit}.png"

class Deck:
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = [
            ('Two', 2), ('Three', 3), ('Four', 4), ('Five', 5), ('Six', 6), ('Seven', 7),
            ('Eight', 8), ('Nine', 9), ('Ten', 10), ('Jack', 10), ('Queen', 10),
            ('King', 10), ('Ace', 11)
        ]
        for suit in suits:
            for rank, value in ranks:
                self.cards.append(Card(suit, rank, value))
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_chips = 5000
        self.current_bet = 0
        self.game_over = False

    def start_game(self):
        self.player_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.game_over = False

        if self.calculate_hand_value(self.dealer_hand) == 21:
            self.game_over = True
            return "Dealer has Blackjack! You lose."

    def calculate_hand_value(self, hand):
        value = sum(card.value for card in hand)
        ace_count = sum(1 for card in hand if card.rank == 'Ace')
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        return value

    def hit(self, hand):
        hand.append(self.deck.draw_card())

    def stand(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.hit(self.dealer_hand)
        self.game_over = True

    def check_winner(self):
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)

        if player_value > 21:
            return "Dealer wins! Player busted."
        if dealer_value > 21:
            return "Player wins! Dealer busted."
        if player_value > dealer_value:
            return "Player wins!"
        if player_value < dealer_value:
            return "Dealer wins!"
        return "It's a tie!"
    
    def reset_chips(self):
        self.player_chips = 5000


    def place_bet(self, amount):
        if amount <= 0 or amount > self.player_chips:
            return "Invalid bet amount."
        self.current_bet = amount
        self.player_chips -= amount
        return f"Bet placed: {amount}"

    def settle_bet(self, message):
        if "Player wins" in message:
            self.player_chips += self.current_bet * 2
        elif "It's a tie" in message:
            self.player_chips += self.current_bet

    def get_player_chips(self):
        return self.player_chips