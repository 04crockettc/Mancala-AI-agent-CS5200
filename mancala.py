# CS 5200: AI Methods
# Project Title: An AI Agent for Mancala Adversarial Search Problem
# Project Type: Adversarial Game
# Project Contributers: Claire Crockett

# Project Summary: Mancala is a two-player board game where players take turns 
# distributing stones across pits with the goal of collecting the most stones. 
# This project aims to Implement an AI agent that selects the optimal move against 
# a human in the adversarial search problem of the game Mancala. This will act as an 
# exploration of how adversarial AI techniques perform in a fully observable and 
# deterministic environment like Mancala. The agent will use a game-tree search 
# algorithm such as mini-max and heuristic search functions.

import random

class MancalaBoard:
    def __init__(self):
        # 12 pits + 2 stores
        # pits[0..5] = Player 1, pits[6..11] = Player 2
        # store[0] = Player 1 store, store[1] = Player 2 store
        self.pits = [4] * 12
        self.stores = [0, 0]
        self.current_player = random.getrandbits(1)  # 0 = Player 1, 1 = Player 2

    # FUCNTION: display the board
    def display(self):
        print("\n     AI Player")
        print("  ", self.pits[11:5:-1])
        print(f"[{self.stores[1]}]                  [{self.stores[0]}]")
        print("  ", self.pits[0:6])
        print("     You\n")

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
            pos = (pos + 1) % 14  # positions 0–13

            # skip opponent's store
            if new_state.current_player == 0 and pos == 13:
                continue
            if new_state.current_player == 1 and pos == 6:
                continue

            # place stone in correct location
            if pos == 6:
                # Player 1 store
                new_state.stores[0] += 1

            elif pos == 13:
                # Player 2 store
                new_state.stores[1] += 1

            elif 0 <= pos <= 5:
                # Player 1 pits
                new_state.pits[pos] += 1

            elif 7 <= pos <= 12:
                # Player 2 pits (shift index!)
                new_state.pits[pos - 1] += 1

            stones -= 1

        # check extra turn
        if new_state.current_player == 0 and pos == 6:
            pass
        elif new_state.current_player == 1 and pos == 13:
            pass
        # check capture
        elif new_state.current_player == 0 and 0 <= pos <= 5 and new_state.pits[pos] == 1 and new_state.pits[11 - pos] != 0:
            opposite = 11 - pos
            new_state.stores[0] += new_state.pits[opposite] + 1
            new_state.pits[opposite] = 0
            new_state.pits[pos] = 0
            new_state.current_player = 1
        elif new_state.current_player == 1 and 6 <= pos <= 11 and new_state.pits[pos] == 1 and new_state.pits[11 - pos] != 0:
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
        score = (self.stores[1] - self.stores[0]) * 2  
        # Evaluation of the AI's move
        for i in range(6, 12):
            # extra turn setup bonus
            if self.pits[i] == (13 - i):
                score += 3
            # capture opportunity bonus
            if self.pits[i] == 0 and self.pits[11 - i] > 0:
                score -= 3
            # stone count advantage
            score += self.pits[i] * 0.5

        # Evaluation of the human's move
        for i in range(0, 6):
            # extra turn setup for human 
            if self.pits[i] == (6 - i):
                score -= 3
            # human capture opportunity 
            if self.pits[i] == 0 and self.pits[11 - i] > 0:
                score += 3
            # human stone count
            score -= self.pits[i] * 0.5

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
        val = minimax(child, max_depth - 1, float('-inf'), float('inf'), True)
        if val >= best_val:
            best_val = val
            best_action = action
    return best_action

# FUNCTION: Simulation to test AI by playing 100 game against randomly selected moves. 
def run_simulation(num_games=100):
    ai_wins = 0
    human_wins = 0
    draws = 0
    total_margin = 0

    for game in range(num_games):
        board = MancalaBoard()
        board.current_player = game % 2  # alternate who goes first

        while not board.terminal_test():
            if board.current_player == 1:
                # AI turn
                action = get_best_move(board, 8)
            else:
                # Random player turn
                action = random.choice(board.get_actions())
            board = board.result(action)

        # transfer remaining stones
        for i in range(0, 6):
            board.stores[0] += board.pits[i]
            board.pits[i] = 0
        for i in range(6, 12):
            board.stores[1] += board.pits[i]
            board.pits[i] = 0

        margin = board.stores[1] - board.stores[0]
        total_margin += margin

        if board.stores[1] > board.stores[0]:
            ai_wins += 1
        elif board.stores[0] > board.stores[1]:
            human_wins += 1
        else:
            draws += 1

        print(f"Game {game + 1}/{num_games} complete | AI: {board.stores[1]} Human: {board.stores[0]}")

    print("\n========== SIMULATION RESULTS ==========")
    print(f"Total Games:           {num_games}")
    print(f"AI Wins:               {ai_wins}")
    print(f"Random Player Wins:    {human_wins}")
    print(f"Draws:                 {draws}")
    print(f"AI Win Rate:           {ai_wins / num_games * 100:.1f}%")
    print(f"Average Margin:        {total_margin / num_games:.1f} stones")
    print("========================================")

#FUNCTION: main function that perform the game loop for player
def main():
    board = MancalaBoard()
    print("Welcome to Mancala!")
    print("The first player is randomly chosen at the start of each game. You are bottom row. Pits are numbered 1-6 left to right.")

    if board.current_player == 0:
        print("\n You Go First \n" )
    else:
        print("AI Player Goes First \n" )

    print("Starting Game Board: ")
    board.display()

    # perform game loop
    while not board.terminal_test():
        if board.current_player == 0:
            # Human turn
            legal = board.get_actions()
            print(f"Your legal moves: {[i + 1 for i in legal]}")
            while True:
                try:
                    action = int(input("Pick a pit (1-6): ")) - 1
                    if action in legal:
                        break
                    else:
                        print("Invalid move, pick from your legal moves.")
                except ValueError:
                    print("Please enter a number.")
            board = board.result(action)
            print("\nYou picked pit", action + 1)
            board.display()
        else:
            # AI turn
            action = get_best_move(board, 8) #change depth 
            board = board.result(action)
            print(f"AI picked pit {action + 1}")
            board.display()

    # Game over: transfer remaining stones
    for i in range(0, 6):
        board.stores[0] += board.pits[i]
        board.pits[i] = 0
    for i in range(6, 12):
        board.stores[1] += board.pits[i]
        board.pits[i] = 0

    print("Game Over!")
    board.display()
    print(f"Player 1 (You): {board.stores[0]} stones")
    print(f"Player 2 (AI):  {board.stores[1]} stones")
    # display winner
    if board.stores[0] > board.stores[1]:
        print("You win!")
    elif board.stores[1] > board.stores[0]:
        print("AI wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
        run_simulation()