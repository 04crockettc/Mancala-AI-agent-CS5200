# CS 5200: AI Methods
# Project Title: An AI Agent for Mancala Adversarial Search Problem
# Project Type: Adversarial Game

# Project Summary: Mancala is a two-player board game where players take turns 
# distributing stones across pits with the goal of collecting the most stones. 
# This project aims to Implement an AI agent that selects the optimal move against 
# a human in the adversarial search problem of the game Mancala. This will act as an 
# exploration of how adversarial AI techniques perform in a fully observable and 
# deterministic environment like Mancala. The agent will use a game-tree search 
# algorithm such as mini-max and heuristic search functions.

class MancalaBoard:
    def __init__(self):
        # 12 pits + 2 stores
        # pits[0..5] = Player 1, pits[6..11] = Player 2
        # store[0] = Player 1 store, store[1] = Player 2 store
        self.pits = [4] * 12
        self.stores = [0, 0]
        self.current_player = 0  # 0 = Player 1, 1 = Player 2

    # FUCNTION: display the board
    def display(self):
        print("\n     Player 2 (AI)")
        print("  ", self.pits[11:5:-1])
        print(f"[{self.stores[1]}]                  [{self.stores[0]}]")
        print("  ", self.pits[0:6])
        print("     Player 1 (Human)\n")

    #FUNCTION: get available moves
    def get_actions(self):
        legal_moves = []
        if self.current_player == 0:
            for i in range(0, 6):
                if self.pits[i] > 0:
                    legal_moves.append(i)
        else:
            for i in range(6, 12):
                if self.pits[i] > 0:
                    legal_moves.append(i)
        return legal_moves
    
    # FUNCTION: perform the action chosen by the player
    def result(self, action):
        import copy
        new_state = copy.deepcopy(self)
        stones = new_state.pits[action]
        new_state.pits[action] = 0
        pos = action

        # sow stones counterclockwise
        while stones > 0:
            pos = (pos + 1) % 14
            # skip opponent's store
            if new_state.current_player == 0 and pos == 13:
                continue
            if new_state.current_player == 1 and pos == 6:
                continue
            # place in store
            if pos == 6:
                new_state.stores[0] += 1
            elif pos == 13:
                new_state.stores[1] += 1
            else:
                new_state.pits[pos] += 1
            stones -= 1

        # check extra turn
        if new_state.current_player == 0 and pos == 6:
            pass  # Player 1 gets extra turn
        elif new_state.current_player == 1 and pos == 13:
            pass  # Player 2 gets extra turn
        # check capture
        elif new_state.current_player == 0 and 0 <= pos <= 5 and new_state.pits[pos] == 1:
            opposite = 11 - pos
            new_state.stores[0] += new_state.pits[opposite] + 1
            new_state.pits[opposite] = 0
            new_state.pits[pos] = 0
            new_state.current_player = 1
        elif new_state.current_player == 1 and 6 <= pos <= 11 and new_state.pits[pos] == 1:
            opposite = 11 - pos
            new_state.stores[1] += new_state.pits[opposite] + 1
            new_state.pits[opposite] = 0
            new_state.pits[pos] = 0
            new_state.current_player = 0
        else:
            new_state.current_player = 1 - new_state.current_player

        return new_state
    
    # FUNCTION: checks to see if the goal state has been reached. 
    def terminal_test(self):
        if sum(self.pits[0:6]) == 0 or sum(self.pits[6:12]) == 0:
            return True
        return False
    
    # FUNCTION: evaluates the score
    def evaluate(self):
        score = self.stores[0] - self.stores[1]
        for i in range(0, 6):
            if self.pits[i] == (6 - i):
                score += 1
        for i in range(6, 12):
            if self.pits[i] == (12 - i):
                score -= 1
        return score

#test board
if __name__ == "__main__":
    board = MancalaBoard()
    board.display()
    print("Legal moves for Player 1:", board.get_actions())
    print("Is terminal state?", board.terminal_test())
    print("Board score:", board.evaluate())