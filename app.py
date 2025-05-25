import streamlit as st
import random

def initialize_game():
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.awaiting_computer = False  # <--- NEW

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
    winner = check_winner(board)
    if winner == 'O':
        return 1
    if winner == 'X':
        return -1
    if ' ' not in board:
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def computer_move():
    if st.session_state.game_over or ' ' not in st.session_state.board:
        return
    empty_cells = [i for i, cell in enumerate(st.session_state.board) if cell == ' ']
    try:
        if st.session_state.difficulty == "Easy":
            move = random.choice(empty_cells)
        elif st.session_state.difficulty == "Medium":
            move = None
            for cell in empty_cells:
                temp_board = st.session_state.board.copy()
                temp_board[cell] = 'O'
                if check_winner(temp_board) == 'O':
                    move = cell
                    break
            if move is None:
                for cell in empty_cells:
                    temp_board = st.session_state.board.copy()
                    temp_board[cell] = 'X'
                    if check_winner(temp_board) == 'X':
                        move = cell
                        break
            if move is None:
                move = random.choice(empty_cells)
        else:  # Hard
            best_score = -float('inf')
            best_move = empty_cells[0]
            for cell in empty_cells:
                temp_board = st.session_state.board.copy()
                temp_board[cell] = 'O'
                score = minimax(temp_board, 0, False)
                if score > best_score:
                    best_score = score
                    best_move = cell
            move = best_move
        st.session_state.board[move] = 'O'
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
        elif ' ' not in st.session_state.board:
            st.session_state.winner = 'Draw'
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'X'
    except Exception as e:
        st.error(f"Computer move error: {str(e)}")

def handle_click(index):
    if st.session_state.board[index] == ' ' and not st.session_state.game_over:
        st.session_state.board[index] = st.session_state.current_player
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.winner = winner
            st.session_state.game_over = True
        elif ' ' not in st.session_state.board:
            st.session_state.winner = 'Draw'
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
            # Signal that the computer should move next
            if (st.session_state.game_mode == "Player vs Computer" and st.session_state.current_player == 'O'):
                st.session_state.awaiting_computer = True

def get_symbol(cell):
    if cell == 'X':
        return '❌'
    elif cell == 'O':
        return '⭕'
    else:
        return '🟦'

if 'board' not in st.session_state:
    initialize_game()
if 'awaiting_computer' not in st.session_state:
    st.session_state.awaiting_computer = False

st.title("Tic Tac Toe")

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

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        with cols[col]:
            st.button(
                get_symbol(st.session_state.board[index]),
                key=f"cell_{index}",
                on_click=handle_click,
                args=(index,),
                disabled=st.session_state.board[index] != ' ' or 
                        st.session_state.game_over or 
                        (game_mode == "Player vs Computer" and 
                        st.session_state.current_player == 'O')
            )

# <--- KEY LOGIC: Let computer move if needed
if (
    st.session_state.game_mode == "Player vs Computer"
    and not st.session_state.game_over
    and st.session_state.current_player == 'O'
    and st.session_state.awaiting_computer
):
    computer_move()
    st.session_state.awaiting_computer = False
    st.experimental_rerun()

if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.header("It's a draw! 🤝")
    else:
        st.header(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Current player: {st.session_state.current_player}")

if st.button("Reset Game"):
    initialize_game()
