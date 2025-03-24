import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random
import os
from src.controller import GameController

class GamblingMachineGUI(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Gambling Machine")
        self.geometry("500x380")
        self.configure(bg="#f0f0f0")

        self.is_spinning = False

        self.symbol_images = {}
        for symbol in self.controller.machine.reels:
            img_path = os.path.join("img", f"{symbol.lower()}.png")
            if os.path.exists(img_path):
                self.symbol_images[symbol] = tk.PhotoImage(file=img_path)
            else:
                self.symbol_images[symbol] = None

        self.prompt_player_login()
        self.create_widgets()

    def prompt_player_login(self):
        """
        Simple popup to ask for the player's username.
        If user cancels or enters an empty string, we default to "Guest".
        """
        username = simpledialog.askstring("Player Login", "Enter your username:")
        if not username:
            username = "Guest"
        self.controller.load_player(username)

    def create_widgets(self):
        self.credits_label = tk.Label(
            self, 
            text=f"Credits: {self.controller.get_credits()}", 
            font=("Arial", 14), 
            bg="#f0f0f0"
        )
        self.credits_label.pack(pady=10)

        self.bet_label = tk.Label(
            self, 
            text=f"Bet: {self.controller.get_bet()}", 
            font=("Arial", 14), 
            bg="#f0f0f0"
        )
        self.bet_label.pack(pady=10)

        reels_frame = tk.Frame(self, bg="#f0f0f0")
        reels_frame.pack(pady=10)

        self.reel_labels = []
        for i in range(3):
            lbl = tk.Label(reels_frame, text="-", font=("Arial", 20), width=7, bg="white")
            lbl.pack(side=tk.LEFT, padx=5)
            self.reel_labels.append(lbl)

        self.result_label = tk.Label(self, text="", font=("Arial", 14), bg="#f0f0f0")
        self.result_label.pack(pady=10)

        self.lever_button = tk.Button(
            self, 
            text="Pull Lever", 
            font=("Arial", 12), 
            command=self.on_pull_lever
        )
        self.lever_button.pack(pady=10)

        bet_frame = tk.Frame(self, bg="#f0f0f0")
        bet_frame.pack(pady=5)

        self.increase_bet_button = tk.Button(
            bet_frame, 
            text="Increase Bet", 
            font=("Arial", 10), 
            command=self.on_increase_bet
        )
        self.increase_bet_button.grid(row=0, column=0, padx=5)

        self.decrease_bet_button = tk.Button(
            bet_frame, 
            text="Decrease Bet", 
            font=("Arial", 10), 
            command=self.on_decrease_bet
        )
        self.decrease_bet_button.grid(row=0, column=1, padx=5)

    def on_pull_lever(self):
        if self.is_spinning:
            return

        result = self.controller.spin_machine()
        if result is None:
            messagebox.showwarning("Insufficient Credits", "You do not have enough credits to place this bet.")
        else:
            self.is_spinning = True
            self.result_label.config(text="")

            final_reels, winnings = result

            self.animate_reel(
                reel_index=0,
                spin_time=3.0,
                final_symbol=final_reels[0],
                next_callback=lambda: self.animate_reel(
                    reel_index=1,
                    spin_time=1.0,
                    final_symbol=final_reels[1],
                    next_callback=lambda: self.animate_reel(
                        reel_index=2,
                        spin_time=1.0,
                        final_symbol=final_reels[2],
                        next_callback=lambda: self.on_spin_complete(final_reels, winnings)
                    )
                )
            )

    def on_spin_complete(self, final_reels, winnings):
        self.is_spinning = False
        self.credits_label.config(text=f"Credits: {self.controller.get_credits()}")
        self.bet_label.config(text=f"Bet: {self.controller.get_bet()}")

        if winnings > 0:
            self.result_label.config(text=f"You won {winnings} credits!")
        else:
            self.result_label.config(text="No prize this time...")

    def animate_reel(self, reel_index, spin_time, final_symbol, next_callback):
        start_time = time.time()

        def update():
            elapsed = time.time() - start_time
            if elapsed < spin_time:
                random_symbol = random.choice(self.controller.machine.reels)
                self.show_symbol(reel_index, random_symbol)
                self.reel_labels[reel_index].after(100, update)
            else:
                self.show_symbol(reel_index, final_symbol)
                if next_callback:
                    next_callback()

        update()

    def show_symbol(self, reel_index, symbol):
        image = self.symbol_images.get(symbol)
        if image:
            self.reel_labels[reel_index].config(image=image, text="")
            self.reel_labels[reel_index].image = image
        else:
            self.reel_labels[reel_index].config(text=symbol, image="")

    def on_increase_bet(self):
        self.controller.increase_bet()
        self.bet_label.config(text=f"Bet: {self.controller.get_bet()}")

    def on_decrease_bet(self):
        self.controller.decrease_bet()
        self.bet_label.config(text=f"Bet: {self.controller.get_bet()}")
