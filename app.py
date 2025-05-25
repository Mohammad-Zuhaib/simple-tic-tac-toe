import streamlit as st
import random

def initialize_game():
    # Reset only game-related state, not settings
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def check_winner(board):
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combos:
        a, b, c = combo
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def minimax(board, depth, is_maximizing):
    # ... keep minimax implementation same as before ... 

def computer_move():
    # ... keep computer_move implementation same as before ...

def handle_click(index):
    # ... keep handle_click implementation same as before ...

# Initialize game state
if 'board' not in st.session_state:
    initialize_game()

# Game interface
st.title("Tic Tac Toe")

# Game mode selection with session state management
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "Player vs Player"

def update_game_mode():
    st.session_state.game_mode = st.session_state.game_mode_widget
    initialize_game()

game_mode = st.selectbox(
    "Game Mode",
    ["Player vs Player", "Player vs Computer"],
    key="game_mode_widget",
    on_change=update_game_mode
)

# Difficulty selection with session state management
if st.session_state.game_mode == "Player vs Computer":
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "Easy"
    
    def update_difficulty():
        st.session_state.difficulty = st.session_state.difficulty_widget
        initialize_game()
    
    difficulty = st.selectbox(
        "Computer Difficulty",
        ["Easy", "Medium", "Hard"],
        key="difficulty_widget",
        on_change=update_difficulty
    )
