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
            pos += 1
            # wrap around after player 2 store (pos 13)
            if pos > 13:
                pos = 0
            # skip opponent's store
            if new_state.current_player == 0 and pos == 13:
                continue
            if new_state.current_player == 1 and pos == 6:
                continue
            # place in player 1 store
            if pos == 6:
                new_state.stores[0] += 1
            # place in player 2 store
            elif pos == 13:
                new_state.stores[1] += 1
            # place in pit
            elif 0 <= pos <= 11:
                new_state.pits[pos] += 1
            stones -= 1

        # check extra turn
        if new_state.current_player == 0 and pos == 6:
            pass
        elif new_state.current_player == 1 and pos == 13:
            pass
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

def minimax(state, depth, alpha, beta, is_maximizing):
    if state.terminal_test() or depth == 0:
        return state.evaluate()

    if is_maximizing:
        best_val = float('-inf')
        for action in state.get_actions():
            child = state.result(action)
            val = minimax(child, depth - 1, alpha, beta, False)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val

    else:
        best_val = float('inf')
        for action in state.get_actions():
            child = state.result(action)
            val = minimax(child, depth - 1, alpha, beta, True)
            best_val = min(best_val, val)
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val


def get_best_move(state, max_depth):
    best_action = None
    best_val = float('-inf')
    for action in state.get_actions():
        child = state.result(action)
        val = minimax(child, max_depth - 1, float('-inf'), float('inf'), False)
        if val >= best_val:
            best_val = val
            best_action = action
    return best_action

#test board
if __name__ == "__main__":
    board = MancalaBoard()
    board.display()
    print("AI best move is pit", get_best_move(board, 6))