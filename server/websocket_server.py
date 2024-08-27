import asyncio
import json
import websockets
from game_logic import GameState, Pawn, Hero1, Hero2

clients = set()
game_state = GameState()

async def notify_clients():
    if clients:
        message = json.dumps({
            'type': 'game_state',
            'state': serialize_game_state()
        })
        await asyncio.wait([client.send(message) for client in clients])

def serialize_game_state():
    state = {}
    for x in range(5):
        for y in range(5):
            if game_state.grid[x][y]:
                char = game_state.grid[x][y]
                state[(x, y)] = f"{char.owner}-{char.name}"
    return state

async def handle_client(websocket, path):
    clients.add(websocket)
    try:
        await notify_clients()
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'move':
                owner = data['owner']
                char_name = data['character']
                move_pos = tuple(data['position'])
                if game_state.turn == owner:
                    success = game_state.move_character(owner, char_name, move_pos)
                    if success:
                        await notify_clients()
                        winner = game_state.check_winner()
                        if winner:
                            await notify_game_over(winner)
                    else:
                        await websocket.send(json.dumps({'type': 'invalid_move'}))
            elif data['type'] == 'init':
                init_game(data['playerA'], data['playerB'])
                await notify_clients()
    finally:
        clients.remove(websocket)

def init_game(playerA, playerB):
    game_state.__init__()
    for idx, char in enumerate(playerA):
        if char == 'P':
            game_state.add_character(Pawn(f"P{idx+1}", 'A', (0, idx)))
        elif char == 'H1':
            game_state.add_character(Hero1(f"H1-{idx+1}", 'A', (0, idx)))
        elif char == 'H2':
            game_state.add_character(Hero2(f"H2-{idx+1}", 'A', (0, idx)))
    for idx, char in enumerate(playerB):
        if char == 'P':
            game_state.add_character(Pawn(f"P{idx+1}", 'B', (4, idx)))
        elif char == 'H1':
            game_state.add_character(Hero1(f"H1-{idx+1}", 'B', (4, idx)))
        elif char == 'H2':
            game_state.add_character(Hero2(f"H2-{idx+1}", 'B', (4, idx)))

async def notify_game_over(winner):
    message = json.dumps({'type': 'game_over', 'winner': winner})
    await asyncio.wait([client.send(message) for client in clients])

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
