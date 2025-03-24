from src.controller import GameController
from src.view import GamblingMachineGUI

def main():
    controller = GameController()
    app = GamblingMachineGUI(controller)
    app.mainloop()

if __name__ == "__main__":
    main()
