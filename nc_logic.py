# coding: utf-8
"""
Логическая составляющя клиента
КОД ПОЛНОСТЬЮ НЕРАБОЧИЙ. СМОТРЕТЬ НА НЕГО СМЫСЛА НЕТ,
ТАК ОН БУДЕТ ПОЛНОСТЬЮ ПЕРЕПИСАН
"""
# На сервере: определение очередности ходов


import random

field = []  # поле игры
# Фигуры
empty = ' '
nought = 'o'
cross = 'x'

firstPlayer = ''  # фигура первого игрока
secondPlayer = ''  # фигура второго игрока
sequence = []  # хранение очередности ходов

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


def start_game():
    '''
    ПОДГОТОВКА ПАРТИИ
    start_game(list) -> None

    Ф
    1) создает пустое поле
    2) создает список для определения очередности ходов
        [0, 1] - ходит первый юзер, затем - второй
        [1, 0] - ходит второй юзер, затем - первый
    '''
    global field, sequence
    field = [empty]*9  # создание пустого поля или его очистка
    sequence = gSequence
    return
    # choosing()
    #
    # sequence[0], sequence[1] = sequence[1], sequence[0]

def choosing():
    '''
    ВЫБОР ФИГУРЫ

    '''
    global firstPlayer, secondPlayer
    if sequence[0] == 0:  # если первым ходит игрок
        choice_fig()
    else:  # рандомный если первым ходит компьютер
        x = [cross, nought]
        random.shuffle(x)
        firstPlayer, secondPlayer = x
# ВЫБОР ФИГУРЫ ИГРОКОМ
def choice_fig():
    global firstPlayer, secondPlayer
    x = input('Крестики или нолики? (к/н)')
    if x in ('к', 'c'):  # (к)рестик, (c)ross
        firstPlayer = cross
        secondPlayer = nought
    elif x in ('н', 'n'):  # (н)олик, (n)ought
        firstPlayer = nought
        secondPlayer = cross
    else:
        print('Неверная команда. Повторите выбор')
        choice_fig()
# ХОД
def moving():
    user_move()
# ХОД ПОЛЬЗОВАТЕЛЯ
def user_move():
    cell = input('Ваш ход: ')
    if cell not in ('0', '1', '2', '3', '4', '5', '6', '7', '8'):
        print('Неверная команда. Повторите выбор')
        user_move()
    else:
        if field[int(cell)] != empty:
            print('Ячейка уже заполнена. Повторите ввод')
            user_move()
        else:
            field[int(cell)] = firstPlayer
# ПРОВЕРКА ВЫИГРЫША
def check():
    """
    check() -> int
    Проверка партии на наличие выигрышной ситуации
    Возвращает:
    0 - в случае победы игрока;
    1 - в случае победы компьютера;
    2 - в случае ничьи
    """
    for i in range(len(rules)):
        if field[rules[i][0]] == field[rules[i][1]] == field[rules[i][2]] in (firstPlayer, secondPlayer):
            return 0 if field[rules[i][0]] == firstPlayer else 1
    if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
        return 2