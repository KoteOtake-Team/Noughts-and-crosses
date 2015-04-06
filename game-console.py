import random

# TODO: комменты
'''
ПОЛЕ ИГРЫ
Одномерный список, хранящий состояние каждой ячейки
Порядок ячеек:
    [0][1][2]
    [3][4][5]
    [6][7][8]
Состояния ячеек:
    [ ] - пустая ячейка
    [o] - "нолик"
    [x] - "крестик"
'''
# Фигуры
empty = ' '
nought = 'o'
cross = 'x'

ch = ''  # фигура игрока
c_ch = ''  # фигура компьютера
# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали
field = []  # поле игры


# ВЫВОД ПОЛЯ НА ЭКРАН
def show():
    print('[{0}][{1}][{2}]\n[{3}][{4}][{5}]\n[{6}][{7}][{8}]'
          .format(field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8]))
# ВЫБОР ФИГУРЫ
def choice_fig():
    global ch, c_ch
    ch = input('Крестики или нолики? (к/н)')
    if ch == 'к':
        ch = cross
        c_ch = nought
    elif ch == 'н':
        ch = nought
        c_ch = cross
    else:
        print('Неверная команда. Повтори выбор')
        choice_fig()
# ПРОВЕРКА ВЫИГРЫША
def check():
    for i in range(len(field)):
        if field[i] == empty:
            return False
    if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
        return False
    for i in range(len(rules)):
        if field[rules[i][0]] == field[rules[i][1]] == field[rules[i][2]] in (ch, c_ch):  # TODO: возможна неопределённость
            return True
# ХОД ПОЛЬЗОВАТЕЛЯ
def user_move():
    cell = input('Ваш ход: ')
    if cell not in ('0', '1', '2', '3', '4', '5', '6', '7', '8'):
        print('Неверная команда. Повтори выбор')
        user_move()
    else:
        if field[int(cell)] != empty:
            print('Ячейка уже заполнена. Повторите ввод')
            user_move()
        else:
            field[int(cell)] = ch
# ХОД КОМПЬЮТЕРА
def comp_move():
    # составление списка с пустыми ячейками
    x = []
    for i in range(len(field)):
        if field[i] == empty:
            x += [i]
    m = random.choice(x)
    print('Ход компьютера: ', m)
    field[m] = c_ch
# ПАРТИЯ ИГРЫ
def main():
    global field
    field = [empty]*9
    # TODO: реализовать рандомный выбор первого хода (придется изменить main())
    # if random.choice((0,1)) == 1:
    #     pass
    # else:
    #     pass
    choice_fig()
    print('Вы играете за крестики: ', cross) if ch == cross else print('Вы играете за нолики: ', nought)
    show()
    for i in range(len(field)):
        user_move()
        show()
        if check() is True:
            print('Вы победили')
            break
        elif check() is False:
            print('Ничья')
            break
        comp_move()
        show()
        if check() is True:
            print('Победил компьютер')
            break
        elif check() is False:
            print('Ничья')
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
    if input('Сыграем? (д)') == 'д':
        main()
    else:
        input('Выходим')
        exit()
