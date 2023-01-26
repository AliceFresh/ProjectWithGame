from random import shuffle
from tkinter import Canvas, Tk

BOARD_SIZE = 4  # кол-во квадратов в стороне
SQUARE_SIZE = 80  # размер окна, где располагается игра
EMPTY_SQUARE = BOARD_SIZE ** 2  # создается набор квадратов с цифрами, их количество

root = Tk()  # создано окно в Tkinter
root.title("Пятнашки")  # заголовок

c = Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE, bg="#805080")  # размер и код цвета
c.pack()  # упаковщик, который "проявляет" поле, отвечает за расположение на нем объектов


def get_inv_count():  # get_inversion_count
    inversions = 0  # перестановка цифр
    inversion_board = board[:]  # перестановка цифр в списке, которые представляют доску
    inversion_board.remove(EMPTY_SQUARE)
    for i in range(len(inversion_board)):  # перемешивать, если цифры рядом стоят в верном порядке
        first_item = inversion_board[i]
        for j in range(i + 1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions  # показать конечный результат перестановок


def is_solvable():  # разрешимый
    """Функция определяющая имеет ли головоломка решение"""
    # перебираем возможные случаи
    num_inversions = get_inv_count()
    if BOARD_SIZE % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = BOARD_SIZE - (board.index(EMPTY_SQUARE) // BOARD_SIZE)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_neighbor(index):
    empty_index = board.index(EMPTY_SQUARE)  # получаем индекс пустой клетки в списке
    abs_value = abs(empty_index - index)  # узнаем расстояние от пустой клетки до клетки по которой кликнули
    """ Если пустая клетка над или под клеткой на которую кликнули, возвращаем индекс пустой клетки"""
    if abs_value == BOARD_SIZE:    # абсолютное значение (модуль значения расстояния)
        return empty_index
    # если пустая клетка слева или справа
    elif abs_value == 1:      # расстояние = 1
        # проверяем, чтобы блоки были в одном ряду
        max_index = max(index, empty_index)
        if max_index % BOARD_SIZE != 0:
            return empty_index
        # рядом с блоком не было пустого поля
    return index


def draw_board():  # продолжить
    # убираем все, что нарисовано на холсте
    c.delete('all')
    # наша задача сгруппировать пятнашки из списка в квадрат
    # со сторонами BOARD_SIZE x BOARD_SIZE
    # i и j будут координатами для каждой отдельной пятнашки
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # получаем значение, которое мы должны будем нарисовать на квадрате
            index = str(board[BOARD_SIZE * i + j])
            # если это не клетка, которую мы хотим оставить пустой
            if index != str(EMPTY_SQUARE):
                # рисуем квадрат по заданным координатам
                c.create_rectangle(j * SQUARE_SIZE, i * SQUARE_SIZE, j * SQUARE_SIZE + SQUARE_SIZE,
                                   i * SQUARE_SIZE + SQUARE_SIZE, fill='#43ABC9', outline='#FFFFFF')
                # пишем число в центре квадрата
                c.create_text(j * SQUARE_SIZE + SQUARE_SIZE / 2, i * SQUARE_SIZE + SQUARE_SIZE / 2, text=index,
                              font="Arial {} italic".format(int(SQUARE_SIZE / 4)), fill='#FFFFFF')


def click(event):
    # Получаем координаты клика
    x, y = event.x, event.y
    # Конвертируем координаты из пикселей в клеточки
    x = x // SQUARE_SIZE
    y = y // SQUARE_SIZE
    # Получаем индекс в списке объекта, по которому мы нажали
    board_index = x + (y * BOARD_SIZE)
    # получаем индекс пустой клетки в списке
    empty_index = get_empty_neighbor(board_index)
    # меняем местами пустую клетку и клетку, по которой кликнули
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    # перерисовываем игровое поле
    draw_board()
    # если текущее состояние доски соответствует правильному - рисуем сообщение о победе
    if board == correct_board:
        show_victory_plate()


def show_victory_plate():
    # рисуем черный квадрат по центру поля
    c.create_rectangle(SQUARE_SIZE / 5, SQUARE_SIZE * BOARD_SIZE / 2 - 10 * BOARD_SIZE,
                       BOARD_SIZE * SQUARE_SIZE - SQUARE_SIZE / 5, SQUARE_SIZE * BOARD_SIZE / 2 + 10 * BOARD_SIZE,
                       fill='#000000', outline='#FFFFFF')
    # пишем красным текст "Победа"
    c.create_text(SQUARE_SIZE * BOARD_SIZE / 2, SQUARE_SIZE * BOARD_SIZE / 1.9, text="ПОБЕДА!",
                  font="Helvetica {} bold".format(int(10 * BOARD_SIZE)), fill='#DC143C')


c.bind('<Button-1>', click)      # связывает нажатие на клетку с кликом, чтобы клетка "реагировала" на клик
c.pack()     # упаковщик

board = list(range(1, EMPTY_SQUARE + 1))  # создаем список пятнашек от 1 до 15 (переменной просто пишем +1)
correct_board = board[:]  # присваиваем список
shuffle(board)  # случайное расположение, в самом начале мы подключили рандом

while not is_solvable():
    shuffle(board)  # располагаем случайно в нашем квадрате пятнашки

draw_board()   # вызывает рисование поля
root.mainloop()      # запускает все действия
