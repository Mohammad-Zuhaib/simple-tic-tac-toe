import streamlit as st
import random

def initialize_game():
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.awaiting_computer = False

def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in wins:
        a, b, c = line
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':
        return 1
    if winner == 'X':
        return -1
    if ' ' not in board:
        return 0
    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth+1, False)
                board[i] = ' '
                best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth+1, True)
                board[i] = ' '
                best = min(score, best)
        return best

def computer_move():
    board = st.session_state.board
    empty = [i for i, c in enumerate(board) if c == ' ']
    move = None
    if st.session_state.difficulty == "Easy":
        move = random.choice(empty)
    elif st.session_state.difficulty == "Medium":
        # Win if possible
        for i in empty:
            temp = board.copy()
            temp[i] = 'O'
            if check_winner(temp) == 'O':
                move = i
                break
        # Block if needed
        if move is None:
            for i in empty:
                temp = board.copy()
                temp[i] = 'X'
                if check_winner(temp) == 'X':
                    move = i
                    break
        # Otherwise random
        if move is None:
            move = random.choice(empty)
    else:
        # Hard: Minimax
        best_score = -float('inf')
        for i in empty:
            temp = board.copy()
            temp[i] = 'O'
            score = minimax(temp, 0, False)
            if score > best_score:
                best_score = score
                move = i
    board[move] = 'O'
    winner = check_winner(board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    elif ' ' not in board:
        st.session_state.winner = 'Draw'
        st.session_state.game_over = True
    else:
        st.session_state.current_player = 'X'

def handle_click(idx):
    if st.session_state.board[idx] == ' ' and not st.session_state.game_over:
        st.session_state.board[idx] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
        elif ' ' not in st.session_state.board:
            st.session_state.winner = 'Draw'
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            if st.session_state.game_mode == "Player vs Computer" and st.session_state.current_player == 'O':
                st.session_state.awaiting_computer = True
                # Immediately rerun so the computer can move
                st.experimental_rerun()

def get_symbol(cell):
    if cell == 'X':
        return '❌'
    elif cell == 'O':
        return '⭕'
    else:
        return '🟦'

# --- Initialize State ---
if 'board' not in st.session_state:
    initialize_game()
if 'awaiting_computer' not in st.session_state:
    st.session_state.awaiting_computer = False

st.title("Tic Tac Toe")

# --- Game Mode ---
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Player vs Player"
def update_mode():
    st.session_state.game_mode = st.session_state.game_mode_widget
    initialize_game()
game_mode = st.selectbox(
    "Game Mode",
    ["Player vs Player", "Player vs Computer"],
    key="game_mode_widget",
    on_change=update_mode
)

# --- Difficulty ---
if st.session_state.game_mode == "Player vs Computer":
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "Easy"
    def update_difficulty():
        st.session_state.difficulty = st.session_state.difficulty_widget
        initialize_game()
    st.selectbox(
        "Computer Difficulty",
        ["Easy", "Medium", "Hard"],
        key="difficulty_widget",
        on_change=update_difficulty
    )

# --- Board ---
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        idx = r*3 + c
        with cols[c]:
            st.button(
                get_symbol(st.session_state.board[idx]),
                key=f"cell_{idx}",
                on_click=handle_click,
                args=(idx,),
                disabled=(st.session_state.board[idx] != ' ' or 
                          st.session_state.game_over or
                          (game_mode == "Player vs Computer" and st.session_state.current_player == 'O'))
            )

# --- Computer move (NO rerun, just react to state flag) ---
if (st.session_state.game_mode == "Player vs Computer"
    and not st.session_state.game_over
    and st.session_state.current_player == 'O'
    and st.session_state.awaiting_computer):
    computer_move()
    st.session_state.awaiting_computer = False

# --- Status ---
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.header("It's a draw! 🤝")
    else:
        st.header(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Current player: {st.session_state.current_player}")

if st.button("Reset Game"):
    initialize_game()
