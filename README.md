# Chess-like Turn-based Game

## Overview
This is a turn-based chess-like game developed using Python for the server-side logic and a simple web client for interaction. The game uses WebSocket for real-time communication between the server and clients.

## Features
- Turn-based gameplay on a 5x5 grid
- Real-time WebSocket communication
- Game state synchronization across clients
- Dynamic player movement and combat mechanics

## Installation

### Server
1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the WebSocket server:
    ```bash
    python server/websocket_server.py
    ```

### Client
1. Open `client/index.html` in your browser.

## Game Rules
- The game is played between two players on a 5x5 grid.
- Each player has 5 characters: Pawns, Hero1, and Hero2.
- Players take turns moving their characters.
- The game ends when one player eliminates all of the opponent's characters.

## Controls
- Select a character by clicking on it.
- Valid moves for the selected character will be shown as buttons.
- Click on a move button to make the move.

## Technical Details
- The game state is managed on the server.
- Clients connect to the server via WebSocket.
- The game is rendered dynamically on the client-side.

## Future Improvements
- Add more character types and move patterns.
- Implement a dynamic team composition feature.
- Add spectator mode and chat features.
