# Mancala-AI-agent-CS5200

How to Run:
-run the mancala.py file
-take turns by entering a number 1-6 into the terminal

Project statement:
Mancala is a two-player board game where players take turns distributing stones across pits with the goal of collecting the most stones. This project aims to Implement an AI agent that selects the optimal move against a human in the adversarial search problem of the game Mancala. This will act as an exploration of how adversarial AI techniques perform in a fully observable and deterministic environment like Mancala. The agent will use a game-tree search algorithm such as mini-max and heuristic search functions.

Turn Structure: 
The board is set up by having 12 pits in the center of the board, divided into two rows of 6. The row of 6 closest to you becomes your play arena. In addition, each player has a capture pit on the right side of the row. Before the game starts, 4 stones are placed in each of the 12 center pits. 
On a player’s turn, they pick up all of the stones from one of the 6 pits on their side. Then they “sow” the stone by dropping one seed into each pit as they move counterclockwise around the board. If the payer passes a personal store while sowing seeds, they drop one seed into it as they pass. So you must be careful to avoid placing seeds in the adversarial’s store. If the last seed in your hand ends inside your store, you get to take another turn. If the last seed you sow ends in an empty pit on your side, then you get to place all the seeds in the pit across from you on the opponent’s side, and your last seed, into or store.  
 
Winning Condition / Goal State: 
The game ends when one of the players' rows of pits is completely empty. The winner is the player with the most seeds in their store.  
