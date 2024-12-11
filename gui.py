import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game import BlackjackGame

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.game = BlackjackGame()
        self.card_images = {}
        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="green")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Frames for hands
        self.dealer_label = tk.Label(self.frame, text="Dealer's Hand:", bg="green", fg="white", font=("Arial", 16))
        self.dealer_label.pack(pady=10)

        self.dealer_frame = tk.Frame(self.frame, bg="green")
        self.dealer_frame.pack(pady=10)

        self.player_label = tk.Label(self.frame, text="Your Hand:", bg="green", fg="white", font=("Arial", 16))
        self.player_label.pack(pady=10)

        self.player_frame = tk.Frame(self.frame, bg="green")
        self.player_frame.pack(pady=10)

        # Player chips and bets
        self.chips_label = tk.Label(self.frame, text=f"Chips: {self.game.get_player_chips()}", bg="green", fg="white", font=("Arial", 14))
        self.chips_label.pack(pady=10)

        self.bet_label = tk.Label(self.frame, text="Place your bet:", bg="green", fg="white", font=("Arial", 14))
        self.bet_label.pack(pady=10)

        # Frames for buttons
        self.bet_frame = tk.Frame(self.frame, bg="green")
        self.bet_frame.pack(pady=10)

        self.bet_button_100 = tk.Button(self.bet_frame, text="Bet 100", command=lambda: self.place_bet(100), width=10)
        self.bet_button_100.grid(row=0, column=0, padx=5)

        self.bet_button_500 = tk.Button(self.bet_frame, text="Bet 500", command=lambda: self.place_bet(500), width=10)
        self.bet_button_500.grid(row=0, column=1, padx=5)

        self.bet_button_1000 = tk.Button(self.bet_frame, text="Bet 1000", command=lambda: self.place_bet(1000), width=10)
        self.bet_button_1000.grid(row=0, column=2, padx=5)

        # Buttons for actions
        self.button_frame = tk.Frame(self.frame, bg="green")
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", command=self.hit, width=10)
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.button_frame, text="Stand", command=self.stand, width=10)
        self.stand_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_game, width=10)
        self.reset_button.grid(row=0, column=2, padx=10)

        self.load_card_images()
        self.reset_game()

    def load_card_images(self):
        # Image cache
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        for filename in os.listdir(assets_path):
            if filename.endswith(".png"):
                card_name = filename.replace(".png", "")
                image_path = os.path.join(assets_path, filename)
                image = Image.open(image_path).resize((100, 150))
                self.card_images[card_name] = ImageTk.PhotoImage(image)

    def place_bet(self, amount):
        result = self.game.place_bet(amount)
        if "Bet placed" in result:
            self.game.start_game()
            self.update_ui()
            self.bet_label.config(text=f"Bet Amount: {amount}")
            self.enable_action_buttons()
            self.disable_bet_buttons()
        else:
            messagebox.showerror("Invalid Bet", result)


    def enable_action_buttons(self):
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def disable_action_buttons(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def disable_bet_buttons(self):
        for button in [self.bet_button_100, self.bet_button_500, self.bet_button_1000]:
            button.config(state="disabled")

    def enable_bet_buttons(self):
        for button in [self.bet_button_100, self.bet_button_500, self.bet_button_1000]:
            button.config(state="normal")


    def reset_game(self):
        self.game.reset_chips()
        self.game = BlackjackGame()
        self.update_ui()
        self.enable_bet_buttons()
        self.disable_action_buttons()
        self.bet_label.config(text="Please place your bet to start the game.")
        self.chips_label.config(text=f"Chips: {self.game.get_player_chips()}")

    def hit(self):
        self.game.hit(self.game.player_hand)
        self.update_ui()
        if self.game.calculate_hand_value(self.game.player_hand) > 21:
            self.end_game("Dealer wins! Player busted.")

    def stand(self):
        self.game.stand()
        self.update_ui()
        winner = self.game.check_winner()
        self.end_game(winner)

    def update_ui(self):
        if self.game.current_bet == 0:
            self.clear_frame(self.dealer_frame)
            self.clear_frame(self.player_frame)
        else:
            self.update_hand(self.dealer_frame, self.game.dealer_hand, "Dealer")
            self.update_hand(self.player_frame, self.game.player_hand, "Player")

        self.chips_label.config(text=f"Chips: {self.game.get_player_chips()}")
    
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def update_hand(self, frame, hand, role):
        for widget in frame.winfo_children():
            widget.destroy()

        for i, card in enumerate(hand):
            if role == "Dealer" and i == 1 and not self.game.game_over:
                card_image = self.card_images.get("default", None)
            else:
                card_image = self.card_images.get(card.get_image_filename().replace(".png", ""), None)

            if card_image:
                label = tk.Label(frame, image=card_image, bg="green")
                label.pack(side=tk.LEFT, padx=5)


    def end_game(self, result):
        messagebox.showinfo("Game Over", result)
        self.game.settle_bet(result)
        self.disable_action_buttons()
        self.enable_bet_buttons()
        self.update_ui()

    def enable_buttons(self):
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")
        self.reset_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
