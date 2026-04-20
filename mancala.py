class MancalaBoard:
    def __init__(self):
        # 12 pits + 2 stores
        # pits[0..5] = Player 1, pits[6..11] = Player 2
        # store[0] = Player 1 store, store[1] = Player 2 store
        self.pits = [4] * 12
        self.stores = [0, 0]
        self.current_player = 0  # 0 = Player 1, 1 = Player 2

    def display(self):
        print("\n     Player 2 (AI)")
        print("  ", self.pits[11:5:-1])
        print(f"[{self.stores[1]}]                  [{self.stores[0]}]")
        print("  ", self.pits[0:6])
        print("     Player 1 (Human)\n")


#test board diplay
if __name__ == "__main__":
    board = MancalaBoard()
    board.display()