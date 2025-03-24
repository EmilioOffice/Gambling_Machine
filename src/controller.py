import configparser
import mysql.connector
from src.model import GamblingMachine

class GameController:
    def __init__(self):
        self.machine = GamblingMachine()
        self.current_player = None

        config = configparser.ConfigParser()
        config.read('sample_config.ini')

        self.db_config = {
            'host': config['database']['host'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'database': config['database']['database']
        }

        self.init_database()

    def init_database(self):
        """
        Creates the table in the MySQL database if it does not exist.
        Also includes the new columns for biggest_win and last_login.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_profiles (
                username VARCHAR(50) PRIMARY KEY,
                credits INT,
                total_spins INT,
                total_wins INT,
                biggest_win INT,
                last_login DATETIME
            )
        """)
        conn.commit()
        conn.close()

    def load_player(self, username):
        """
        Loads an existing player or creates a new one if not found.
        Sets the current_player and updates the machine credits.
        Updates last_login to NOW().
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        select_query = """
            SELECT username, credits, total_spins, total_wins, biggest_win, last_login
            FROM player_profiles
            WHERE username = %s
        """
        cursor.execute(select_query, (username,))
        row = cursor.fetchone()

        if row:
            self.current_player = {
                "username": row[0],
                "credits": row[1],
                "total_spins": row[2],
                "total_wins": row[3],
                "biggest_win": row[4],
                "last_login": row[5]
            }

            update_query = "UPDATE player_profiles SET last_login = NOW() WHERE username = %s"
            cursor.execute(update_query, (username,))
            conn.commit()
        else:
            self.current_player = {
                "username": username,
                "credits": 100,
                "total_spins": 0,
                "total_wins": 0,
                "biggest_win": 0,
                "last_login": None
            }
            insert_query = """
                INSERT INTO player_profiles (username, credits, total_spins, total_wins, biggest_win, last_login)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, (
                username, 
                100, 
                0, 
                0, 
                0
            ))
            conn.commit()

        conn.close()

        self.machine.set_credits(self.current_player["credits"])

    def save_player(self):
        """
        Saves the current player's data to the MySQL database, 
        including biggest_win updates if they occurred.
        """
        if not self.current_player:
            return

        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        update_query = """
            UPDATE player_profiles
            SET credits = %s,
                total_spins = %s,
                total_wins = %s,
                biggest_win = %s
            WHERE username = %s
        """
        cursor.execute(update_query, (
            self.current_player["credits"],
            self.current_player["total_spins"],
            self.current_player["total_wins"],
            self.current_player["biggest_win"],
            self.current_player["username"]
        ))
        conn.commit()
        conn.close()

    def spin_machine(self):
        """
        Performs a spin and updates player stats in the database.
        Checks if the spin's winnings exceed biggest_win and updates accordingly.
        """
        spin_result = self.machine.spin()
        if spin_result is None:
            return None

        reels, winnings = spin_result

        self.current_player["credits"] = self.machine.credits
        self.current_player["total_spins"] += 1
        if winnings > 0:
            self.current_player["total_wins"] += 1

            if winnings > self.current_player["biggest_win"]:
                self.current_player["biggest_win"] = winnings

        self.save_player()

        return reels, winnings

    def get_credits(self):
        return self.machine.credits

    def get_bet(self):
        return self.machine.bet

    def increase_bet(self):
        self.machine.bet += 5

    def decrease_bet(self):
        if self.machine.bet > 5:
            self.machine.bet -= 5
