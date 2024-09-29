import tkinter as tk
from tkinter import messagebox

# Минимакс алгоритм для нахождения наилучшего хода
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if check_draw(board):
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

# Поиск наилучшего хода для компьютера
def computer_move():
    global board
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    board[move] = 'O'
    buttons[move].config(text='O', state="disabled")
    if check_winner(board, 'O'):
        messagebox.showinfo("Крестики-нолики", "Компьютер выиграл!")
        reset_game()
    elif check_draw(board):
        messagebox.showinfo("Крестики-нолики", "Ничья!")
        reset_game()

# Проверка на наличие победителя
def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

# Проверка на ничью
def check_draw(board):
    return ' ' not in board

# Ход игрока
def player_move(i):
    global turn
    if board[i] == ' ':
        if current_mode == 'friend':
            mark = 'X' if turn % 2 == 0 else 'O'
            board[i] = mark
            buttons[i].config(text=mark, state="disabled")
            if check_winner(board, mark):
                messagebox.showinfo("Крестики-нолики", f"Игрок {mark} выиграл!")
                reset_game()
            elif check_draw(board):
                messagebox.showinfo("Крестики-нолики", "Ничья!")
                reset_game()
            turn += 1
        else:  # Режим игры с ботом
            board[i] = 'X'
            buttons[i].config(text='X', state="disabled")
            if check_winner(board, 'X'):
                messagebox.showinfo("Крестики-нолики", "Вы выиграли!")
                reset_game()
            elif check_draw(board):
                messagebox.showinfo("Крестики-нолики", "Ничья!")
                reset_game()
            else:
                computer_move()

# Начать новую игру
def reset_game():
    global board, turn
    board = [' ' for _ in range(9)]
    turn = 0
    for button in buttons:
        button.config(text=' ', state="normal")

# Начало игры с выбором режима
def start_game(mode, first_turn=None):
    global current_mode
    current_mode = mode
    start_frame.pack_forget()
    mode_frame.pack_forget()
    bot_mode_frame.pack_forget()

    # Инициализируем игровое поле
    game_frame.pack()

    reset_game()

    if mode == 'bot' and first_turn == 'computer':
        computer_move()

# Создание начального экрана
def open_start_screen():
    mode_frame.pack_forget()
    bot_mode_frame.pack_forget()
    game_frame.pack_forget()
    start_frame.pack()

# Создание окна для выбора режима игры (с ботом или с другом)
def open_mode_selection():
    start_frame.pack_forget()
    mode_frame.pack()

# Создание окна для выбора, кто ходит первым (в режиме с ботом)
def open_bot_mode_selection():
    mode_frame.pack_forget()
    bot_mode_frame.pack()

# Кнопка для возврата на предыдущий экран
def back_to_mode_selection():
    game_frame.pack_forget()
    mode_frame.pack()

# Создание окна приложения
root = tk.Tk()
root.title("Крестики-нолики")

# Создаем фреймы для разных экранов
start_frame = tk.Frame(root)
mode_frame = tk.Frame(root)
bot_mode_frame = tk.Frame(root)
game_frame = tk.Frame(root)

# Создаем начальный экран
tk.Label(start_frame, text="Добро пожаловать в Крестики-нолики!", font=('normal', 20)).pack(pady=20)

play_button = tk.Button(start_frame, text="Играть", font=('normal', 15), command=open_mode_selection)
play_button.pack(pady=10)

# Экран выбора режима игры (с ботом или с другом)
tk.Label(mode_frame, text="Выберите режим игры", font=('normal', 20)).pack(pady=20)

tk.Button(mode_frame, text="Играть с другом", font=('normal', 15),
          command=lambda: start_game('friend')).pack(pady=10)

tk.Button(mode_frame, text="Играть с ботом", font=('normal', 15),
          command=open_bot_mode_selection).pack(pady=10)

# Экран выбора первого хода (если выбрали игру с ботом)
tk.Label(bot_mode_frame, text="Кто будет ходить первым?", font=('normal', 20)).pack(pady=20)

tk.Button(bot_mode_frame, text="Игрок", font=('normal', 15),
          command=lambda: start_game('bot', 'player')).pack(pady=10)

tk.Button(bot_mode_frame, text="Компьютер", font=('normal', 15),
          command=lambda: start_game('bot', 'computer')).pack(pady=10)

# Кнопка "Назад" для возврата к выбору режима
tk.Button(bot_mode_frame, text="Назад", font=('normal', 15), command=back_to_mode_selection).pack(pady=10)

# Игровое поле (кнопки 3x3)
board = [' ' for _ in range(9)]
buttons = []
turn = 0
current_mode = None

for i in range(9):
    button = tk.Button(game_frame, text=' ', font=('normal', 40), width=5, height=2,
                       command=lambda i=i: player_move(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Добавляем кнопку "Назад" на игровое поле
back_button = tk.Button(game_frame, text="Назад", font=('normal', 15), command=back_to_mode_selection)
back_button.grid(row=3, column=0, columnspan=3)

# Убедимся, что начальный экран отображается при запуске
open_start_screen()

# Запуск основного цикла
root.mainloop()
