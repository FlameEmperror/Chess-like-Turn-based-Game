const ws = new WebSocket("ws://localhost:8765");
let currentTurn = 'A';
let selectedCharacter = null;

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === 'game_state') {
        renderBoard(message.state);
        document.getElementById('current-turn').innerText = `Current Turn: ${currentTurn}`;
    } else if (message.type === 'invalid_move') {
        alert('Invalid move! Try again.');
    } else if (message.type === 'game_over') {
        alert(`Game Over! Player ${message.winner} wins!`);
        resetGame();
    }
};

function renderBoard(state) {
    const board = document.getElementById('board');
    board.innerHTML = ''; // Clear previous board

    for (let y = 0; y < 5; y++) {
        for (let x = 0; x < 5; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.position = `${x},${y}`;

            const key = `${x},${y}`;
            if (state[key]) {
                cell.innerText = state[key];
                cell.classList.add(state[key].split('-')[0]);
                cell.addEventListener('click', () => selectCharacter(key));
            }
            board.appendChild(cell);
        }
    }
}

function selectCharacter(position) {
    if (currentTurn === position.split('-')[0]) {
        selectedCharacter = position;
        showValidMoves(position);
    }
}

function showValidMoves(position) {
    const moveButtons = document.getElementById('move-buttons');
    moveButtons.innerHTML = ''; // Clear previous move buttons

    const [x, y] = position.split(',').map(Number);
    const directions = currentTurn === 'A' ? [-1, 1] : [1, -1];

    directions.forEach(d => {
        const button = document.createElement('button');
        button.innerText = `Move to ${x + d},${y + d}`;
        button.addEventListener('click', () => makeMove([x + d, y + d]));
        moveButtons.appendChild(button);
    });
}

function makeMove(newPosition) {
    if (selectedCharacter) {
        const [charType, position] = selectedCharacter.split(':');
        const [x, y] = newPosition;
        const moveData = {
            type: 'move',
            owner: currentTurn,
            character: charType,
            position: [x, y]
        };
        ws.send(JSON.stringify(moveData));
    }
}

document.getElementById('new-game').addEventListener('click', () => {
    const playerA = ['P', 'H1', 'H2', 'P', 'H1'];
    const playerB = ['H1', 'P', 'H2', 'P', 'H1'];
    ws.send(JSON.stringify({
        type: 'init',
        playerA,
        playerB
    }));
    currentTurn = 'A';
    selectedCharacter = null;
});

function resetGame() {
    const board = document.getElementById('board');
    board.innerHTML = ''; // Clear the board
    const moveButtons = document.getElementById('move-buttons');
    moveButtons.innerHTML = ''; // Clear the move buttons
    document.getElementById('current-turn').innerText = 'Game Over';
}
