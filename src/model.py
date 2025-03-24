import random

class GamblingMachine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GamblingMachine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.credits = 0
        self.bet = 10
        self.reels = ["Cherry", "Lemon", "Orange", "Bell", "Bar", "Seven"]
        self.last_result = []

    def set_credits(self, amount):
        """Set the current player's credits (from the database)."""
        self.credits = amount

    def spin(self):
        """
        Performs a spin if there are enough credits.
        Returns None if not enough credits are available.
        Otherwise, returns a tuple (result_list, winnings).
        """
        if self.credits < self.bet:
            return None

        self.credits -= self.bet
        self.last_result = [random.choice(self.reels) for _ in range(3)]
        winnings = self.calculate_winnings(self.last_result)
        self.credits += winnings
        return self.last_result, winnings

    def calculate_winnings(self, result):
        """
        Calculates the winnings based on the spin result.
        Example rules:
          - Three identical symbols: 5x the bet.
          - Two identical symbols: 2x the bet.
          - Otherwise: no prize.
        """
        if result[0] == result[1] == result[2]:
            return self.bet * 5
        elif (result[0] == result[1]) or (result[1] == result[2]) or (result[0] == result[2]):
            return self.bet * 2
        else:
            return 0

    def update_bet(self, amount):
        """Updates the bet to a new value (not allowing negative or zero)."""
        if amount > 0:
            self.bet = amount
