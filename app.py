import streamlit as st

def initialize_game():
    st.session_state.board = [' '] * 9
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def check_winner(board):
    # Check winning combinations
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combos:
        a, b, c = combo
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

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

# Initialize game state
if 'board' not in st.session_state:
    initialize_game()

# Game title
st.title("Tic Tac Toe")

# Game board
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        with cols[col]:
            st.button(
                st.session_state.board[index],
                key=f"cell_{index}",
                on_click=handle_click,
                args=(index,),
                disabled=st.session_state.board[index] != ' ' or st.session_state.game_over
            )

# Game status
if st.session_state.game_over:
    if st.session_state.winner == 'Draw':
        st.header("It's a draw! 🤝")
    else:
        st.header(f"Player {st.session_state.winner} wins! 🎉")
else:
    st.subheader(f"Current player: {st.session_state.current_player}")

# Reset button
if st.button("Reset Game"):
    initialize_game()

# Optional styling
st.markdown("""
    <style>
    button {
        height: 80px !important;
        width: 80px !important;
        font-size: 40px !important;
    }
    </style>
""", unsafe_allow_html=True)
