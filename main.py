from tkinter import *
import math

def is_moves_left():
    return any(buttons[row][column]['text'] == "" for row in range(3) for column in range(3))

def evaluate():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            return 10 if buttons[row][0]['text'] == 'X' else -10
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            return 10 if buttons[0][column]['text'] == 'X' else -10
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return 10 if buttons[0][0]['text'] == 'X' else -10
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return 10 if buttons[0][2]['text'] == 'X' else -10
    return 0

def minimax(depth, is_max):
    score = evaluate()
    if score == 10 or score == -10:
        return score
    if not is_moves_left():
        return 0
    
    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if buttons[i][j]['text'] == "":
                    buttons[i][j]['text'] = 'X'
                    best = max(best, minimax(depth + 1, False))
                    buttons[i][j]['text'] = ""
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if buttons[i][j]['text'] == "":
                    buttons[i][j]['text'] = 'O'
                    best = min(best, minimax(depth + 1, True))
                    buttons[i][j]['text'] = ""
        return best

def find_best_move():
    best_val = -math.inf
    best_move = (-1, -1)
    
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = 'X'
                move_val = minimax(0, False)
                buttons[i][j]['text'] = ""
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == "" and check_winner() is False:
        buttons[row][column]['text'] = player
        if check_winner() is False:
            player = players[1]
            label.config(text=("AI's turn"))
            window.after(500, ai_move)
        elif check_winner() is True:
            label.config(text=(players[0] + " wins"))
        elif check_winner() == "Tie":
            label.config(text=("Tie!"))

def ai_move():
    if check_winner() is False and is_moves_left():
        row, column = find_best_move()
        buttons[row][column]['text'] = players[1]
        if check_winner() is False:
            global player
            player = players[0]
            label.config(text=(players[0] + " turn"))
        elif check_winner() is True:
            label.config(text=(players[1] + " wins"))
        elif check_winner() == "Tie":
            label.config(text=("Tie!"))

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            return True
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        return True
    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        return True
    elif is_moves_left() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        return "Tie"
    else:
        return False

def new_game():
    global player
    player = players[0]
    label.config(text=player + " turn")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#F0F0F0")

window = Tk()
window.title("Tic-Tac-Toe (Player vs AI)")

players = ["X", "O"]
player = players[0]

buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

label = Label(text=player + " turn", font=('consolas', 40))
label.pack(side="top")

reset_button = Button(text="Restart", font=('consolas', 20), command=new_game)
reset_button.pack(side="top")

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2,
                                      command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

window.mainloop()
