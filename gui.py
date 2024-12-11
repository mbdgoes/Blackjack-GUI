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

        # Labels and frames for dealer's and player's hands
        self.dealer_label = tk.Label(self.frame, text="Dealer's Hand:", bg="green", fg="white", font=("Arial", 16))
        self.dealer_label.pack(pady=10)

        self.dealer_frame = tk.Frame(self.frame, bg="green")
        self.dealer_frame.pack(pady=10)

        self.player_label = tk.Label(self.frame, text="Your Hand:", bg="green", fg="white", font=("Arial", 16))
        self.player_label.pack(pady=10)

        self.player_frame = tk.Frame(self.frame, bg="green")
        self.player_frame.pack(pady=10)

        #Botões para ações
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
        """Cache para as imagens"""
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        for filename in os.listdir(assets_path):
            if filename.endswith(".png"):
                card_name = filename.replace(".png", "")
                image_path = os.path.join(assets_path, filename)
                image = Image.open(image_path).resize((100, 150))
                self.card_images[card_name] = ImageTk.PhotoImage(image)

    def reset_game(self):
        self.game.start_game()
        self.update_ui()
        self.enable_buttons()

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
        self.update_hand(self.dealer_frame, self.game.dealer_hand, "Dealer")
        self.update_hand(self.player_frame, self.game.player_hand, "Player")

    def update_hand(self, frame, hand, role):
        for widget in frame.winfo_children():
            widget.destroy()

        for card in hand:
            card_image = self.card_images.get(card.get_image_filename().replace(".png", ""), None)
            if card_image:
                label = tk.Label(frame, image=card_image, bg="green")
                label.pack(side=tk.LEFT, padx=5)
            else:
                label = tk.Label(frame, text=str(card), bg="green", fg="white", font=("Arial", 14))
                label.pack(side=tk.LEFT, padx=5)

    def end_game(self, message):
        self.disable_buttons()
        messagebox.showinfo("Game Over", message)

    def disable_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)