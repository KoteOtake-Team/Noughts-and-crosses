# coding: utf-8
# author: become-iron (https://github.com/become-iron)

import random
from copy import deepcopy

field = []  # поле игры
# Фигуры
empty = ' '
nought = 'o'
cross = 'x'

userFig = ''  # фигура игрока
compFig = ''  # фигура компьютера
line = [0, 1]  # хранение очередности ходов

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


# ВЫВОД ПОЛЯ НА ЭКРАН
def show():
    # FIXME: оптимизировать
    print('[{0}][{1}][{2}]\n[{3}][{4}][{5}]\n[{6}][{7}][{8}]'
          .format(field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8]))
# ВЫБОР ФИГУРЫ
def choosing():
    global userFig, compFig
    if line[0] == 0:  # если первым ходит игрок
        choice_fig()
    else:  # рандомный если первм ходит компьютер
        x = [cross, nought]
        random.shuffle(x)
        userFig, compFig = x
# ВЫБОР ФИГУРЫ ИГРОКОМ
def choice_fig():
    global userFig, compFig
    x = input('Крестики или нолики? (к/н)')
    if x in ('к', 'c'):  # (к)рестик, (c)ross
        userFig = cross
        compFig = nought
    elif x in ('н', 'n'):  # (н)олик, (n)ought
        userFig = nought
        compFig = cross
    else:
        print('Неверная команда. Повторите выбор')
        choice_fig()
# ХОД
def moving():
    if line_temp.pop(0) == 0:  # если первым должен ходить игрок
        user_move()
        show()
    else:
        comp_move()
        show()
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
            field[int(cell)] = userFig
# ХОД КОМПЬЮТЕРА
def comp_move():
    # составление списка с индексами пустых ячеек
    x = []
    for i in range(len(field)):
        if field[i] == empty:
            x += [i]
    # рандомный ход компьютера
    m = random.choice(x)
    print('Ход компьютера: ', m)
    field[m] = compFig
# ПРОВЕРКА ВЫИГРЫША
def check():
    '''
    Функция проверяет партию на наличие выигрышной ситуации
    Возвращает:
    0 - в случае победы игрока;
    1 - в случае победы компьютера;
    2 - в случае ничьи
    '''
    for i in range(len(rules)):
        if field[rules[i][0]] == field[rules[i][1]] == field[rules[i][2]] in (userFig, compFig):
            return 0 if field[rules[i][0]] == userFig else 1
    if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
        return 2

# ПАРТИЯ ИГРЫ
def main():
    global field, line, line_temp
    field = [empty]*9  # создание пустого поля или его очистка
    print('=' * 30)
    random.shuffle(line)  # рандомно получаем очередность ходов: 0 - игрок, 1 - компьютер
    if line[0] == 0:
        print('ВЫ ХОДИТЕ ПЕРВЫМ')
    else:
        print('КОМПЬЮТЕР ХОДИТ ПЕРВЫМ')
    choosing()
    print('ВЫ ИГРАЕТЕ ЗА КРЕСТИКИ: ', cross) if userFig == cross else print('ВЫ ИГРАЕТЕ ЗА НОЛИКИ: ', nought)
    if line[0] == 0:
        show()
    for i in range(len(field)):
        # TODO: отрефакторить это безобразие (если это возможно вообще)
        line_temp = deepcopy(line)
        moving()
        check_temp = check()
        if check_temp == 0:
            print('ВЫ ПОБЕДИЛИ')
            break
        elif check_temp == 1:
            print('ПОБЕДИЛ КОМПЬЮТЕР')
            break
        elif check_temp == 2:
            print('НИЧЬЯ')
            break
        moving()
        check_temp = check()
        if check_temp == 0:
            print('ВЫ ПОБЕДИЛИ')
            break
        elif check_temp == 1:
            print('ПОБЕДИЛ КОМПЬЮТЕР')
            break
        elif check_temp == 2:
            print('НИЧЬЯ')
            break


print('''
КРАТКО ОБ ОСОБЕННОСТЯХ
Порядок ячеек:
    [0][1][2]
    [3][4][5]
    [6][7][8]
Состояния ячеек:
    [ ] - пустая ячейка
    [o] - "нолик"
    [x] - "крестик"
''')

while True:
    if input('Сыграем? (д)').lower() in ('д','y'):
        main()
    else:
        input('Выходим')
        exit()
