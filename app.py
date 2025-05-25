import streamlit as st
import random

# --- Game Logic Functions ---
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

def minimax(board, is_maximizing):
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
                score = minimax(board, False)
                board[i] = ' '
                best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ' '
                best = min(score, best)
        return best

def computer_move(board, difficulty):
    empty = [i for i, c in enumerate(board) if c == ' ']
    move = None
    if difficulty == "Easy":
        move = random.choice(empty)
    elif difficulty == "Medium":
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
        best_score = -float('inf')
        for i in empty:
            temp = board.copy()
            temp[i] = 'O'
            score = minimax(temp, False)
            if score > best_score:
                best_score = score
                move = i
    return move

def new_game():
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.waiting_for_computer = False

# --- UI and Session State ---
if 'board' not in st.session_state:
    new_game()

st.title("Tic Tac Toe")

# Game mode and difficulty
def set_mode():
    new_game()
st.selectbox(
    "Game Mode", ["Player vs Player", "Player vs Computer"],
    key="game_mode", on_change=set_mode
)
if st.session_state.game_mode == "Player vs Computer":
    def set_difficulty():
        new_game()
    st.selectbox(
        "Difficulty", ["Easy", "Medium", "Hard"],
        key="difficulty", on_change=set_difficulty
    )
else:
    st.session_state.difficulty = "Easy"

# --- Main Board UI ---
def get_symbol(cell):
    if cell == 'X':
        return '❌'
    if cell == 'O':
        return '⭕'
    return ' '

def handle_click(idx):
    if st.session_state.game_over:
        return
    if st.session_state.board[idx] != ' ':
        return
    if st.session_state.game_mode == "Player vs Computer" and st.session_state.current_player == 'O':
        return
    st.session_state.board[idx] = st.session_state.current_player
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    elif ' ' not in st.session_state.board:
        st.session_state.winner = 'Draw'
        st.session_state.game_over = True
    else:
        # Switch player
        if st.session_state.current_player == 'X':
            st.session_state.current_player = 'O'
            # Trigger computer move if PvC and not game over
            if (st.session_state.game_mode == "Player vs Computer" and not st.session_state.game_over):
                st.session_state.waiting_for_computer = True
        else:
            st.session_state.current_player = 'X'

# Draw board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        with cols[col]:
            st.button(
                get_symbol(st.session_state.board[idx]) or ' ',
                key=f"cell_{idx}",
                on_click=handle_click,
                args=(idx,),
                disabled=(
                    st.session_state.board[idx] != ' ' or
                    st.session_state.game_over or
                    (st.session_state.game_mode == "Player vs Computer" and st.session_state.current_player == 'O')
                )
            )

# --- Computer Move (automatic, no rerun) ---
if (
    st.session_state.game_mode == "Player vs Computer"
    and not st.session_state.game_over
    and st.session_state.current_player == 'O'
    and st.session_state.waiting_for_computer
):
    idx = computer_move(st.session_state.board, st.session_state.difficulty)
    st.session_state.board[idx] = 'O'
    winner = check_winner(st.session_state.board)
    if winner:
        st.session_state.winner = winner
        st.session_state.game_over = True
    elif ' ' not in st.session_state.board:
        st.session_state.winner = 'Draw'
        st.session_state.game_over = True
    else:
        st.session_state.current_player = 'X'
    st.session_state.waiting_for_computer = False

# --- Status and Reset ---
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.success("It's a draw! 🤝")
    else:
        st.success(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.info(f"Current player: {st.session_state.current_player}")

if st.button("Reset Game"):
    new_game()
