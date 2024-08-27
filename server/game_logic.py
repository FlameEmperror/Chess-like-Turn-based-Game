class Character:
    def __init__(self, name, owner, position):
        self.name = name
        self.owner = owner
        self.position = position

    def valid_moves(self, game_state):
        pass

class Pawn(Character):
    def valid_moves(self, game_state):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d in directions:
            new_position = (self.position[0] + d[0], self.position[1] + d[1])
            if self.valid_position(new_position, game_state):
                moves.append(new_position)
        return moves

    def valid_position(self, position, game_state):
        return 0 <= position[0] < 5 and 0 <= position[1] < 5 and game_state.is_empty(position)

class Hero1(Character):
    def valid_moves(self, game_state):
        moves = []
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for d in directions:
            new_position = (self.position[0] + d[0], self.position[1] + d[1])
            if self.valid_position(new_position, game_state):
                moves.append(new_position)
        return moves

    def valid_position(self, position, game_state):
        return 0 <= position[0] < 5 and 0 <= position[1] < 5 and game_state.is_empty_or_enemy(position, self.owner)

class Hero2(Character):
    def valid_moves(self, game_state):
        moves = []
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for d in directions:
            new_position = (self.position[0] + d[0], self.position[1] + d[1])
            if self.valid_position(new_position, game_state):
                moves.append(new_position)
        return moves

    def valid_position(self, position, game_state):
        return 0 <= position[0] < 5 and 0 <= position[1] < 5 and game_state.is_empty_or_enemy(position, self.owner)

class GameState:
    def __init__(self):
        self.grid = [[None for _ in range(5)] for _ in range(5)]
        self.turn = 'A'
        self.players = {'A': [], 'B': []}

    def is_empty(self, position):
        x, y = position
        return self.grid[x][y] is None

    def is_empty_or_enemy(self, position, owner):
        x, y = position
        return self.grid[x][y] is None or self.grid[x][y].owner != owner

    def add_character(self, character):
        x, y = character.position
        self.grid[x][y] = character
        self.players[character.owner].append(character)

    def move_character(self, owner, character_name, new_position):
        character = next(c for c in self.players[owner] if c.name == character_name)
        if new_position in character.valid_moves(self):
            self.grid[character.position[0]][character.position[1]] = None
            character.position = new_position
            x, y = new_position
            if self.grid[x][y] and self.grid[x][y].owner != owner:
                self.remove_character(self.grid[x][y])
            self.grid[x][y] = character
            self.turn = 'B' if owner == 'A' else 'A'
            return True
        return False

    def remove_character(self, character):
        self.players[character.owner].remove(character)
        self.grid[character.position[0]][character.position[1]] = None

    def check_winner(self):
        if not self.players['A']:
            return 'B'
        if not self.players['B']:
            return 'A'
        return None
