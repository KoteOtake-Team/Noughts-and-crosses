# coding: utf-8
# author: become-iron (https://github.com/become-iron)
# author: Alex1166 (https://github.com/Alex1166)

import random

field = []  # поле игры
# Фигуры
empty = ' '
nought = 'o'
cross = 'x'
h = True

userFig = ''  # фигура игрока
compFig = ''  # фигура компьютера
line = [0, 1]  # хранение очередности ходов

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


# ВЫВОД ПОЛЯ НА ЭКРАН
def show():
    print('[{0}][{1}][{2}]\n[{3}][{4}][{5}]\n[{6}][{7}][{8}]'
          .format(field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7], field[8]))


# ВЫБОР ФИГУРЫ
def choosing():
    global userFig, compFig
    if line[0] == 0:  # если первым ходит игрок
        choice_fig()
    else:  # рандомный если первым ходит компьютер
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
    global h
    if line[0] == 0:  # если первым должен ходить игрок
        user_move()
        h = False
        show()
    else:
        if h is True:
            comp_move_random()
            h = False
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
# рандомный ход компьютера
def comp_move_random():
    m = random.choice(range(len(field)))
    print('Ход компьютера: ', m)
    field[m] = compFig


# ход компьютера, мешает игроку
def comp_move_def():
    global g
    if len(figures_def) != 0:
        # print('индикатор начала защиты')
        m = random.choice(figures_def)
        print('Ход компьютера: ', m)
        field[m] = compFig
        g = False
    else:
        pass


# ход компьютера, заполнение своих ячеек
def comp_move_atk():
    global g, figures_def
    g = True
    figures_atk_third = []  # атака только на те клетки, где компьютер близок к победе
    figures_atk_second = []  # атака только на ближайшие клетки, где уже стоит фигура компьютера
    for i in rules:
        count = 0
        collect = []   # тут хранятся индексы двух знаятых ячеек
        for j in i:
            if field[j] == compFig:
                count += 1
                collect.append(j)
        # если найден ряд с двумя символами, ставит третий и побеждает
        if count == 2:
            figures_atk_third += i
            for k in collect:
                figures_atk_third.remove(k)
            figures_atk_third = list(set(figures_atk_third).intersection(set(figures_atk)))
            try:
                m = random.choice(figures_atk_third)
                figures_def = []
                break
            except IndexError:
                pass
        # если рядов с двумя символами нет ставит второй символ в тот же ряд
        elif count == 1:
            for j in i:
                if field[j] == compFig:
                    figures_atk_second += i
                    for k in figures_atk_second:
                        if field[k] == userFig:
                            for n in i:
                                figures_atk_second.remove(n)
            # пересечение со списком всех доступных клеток, убирает все занятые клетки
            figures_atk_second = list(set(figures_atk_second).intersection(set(figures_atk)))
            try:
                m = random.choice(figures_atk_second)
            except IndexError:
                pass
        # первый ход компьютера после самого первого хода игрока
        elif count == 0:
            try:
                try:
                    m = random.choice(figures_atk_second)
                except IndexError:
                    raise IndexError
            except IndexError:
                m = random.choice(figures_atk)
    # пытается защититься. Если защищать нечего, атакует ранее выбранную клетку
    comp_move_def()
    if g is True:
        try:
            print('Ход компьютера: ', m)
        except UnboundLocalError:
            # если осталась единственная свободная клетка, но ни одно из условий не подошло
            for i in range(len(field)):
                if field[i] == empty:
                    m = i
                    print('Ход компьютера: ', m)
        field[m] = compFig
    if g is False:
        pass


def comp_move():
    global figures_atk, figures_def
    # выбор нужных позиций для хода
    figures_atk = []   # здесь хранятся значения всех клеток для атаки
    figures_def = []   # здесь хранятся значения всех клеток для защиты

    # создает списки с доступными вариантами хода
    for i in rules:
        count = 0
        for j in i:
            if field[j] == userFig:
                count += 1
        if count == 2:
            figures_def += i
        elif count < 2:
            figures_atk += i
            count = 0
    # убирает из вариантов для атаки занятые клетки
    for i in range(len(figures_atk)):
        for j in range(len(field)):
            if field[j] != empty:
                try:
                    figures_atk.remove(j)
                except ValueError:
                    pass
    # убирает из вариантов для защиты занятые клетки
    for i in range(len(figures_def)):
        for j in range(len(field)):
            if field[j] != empty:
                try:
                    figures_def.remove(j)
                except ValueError:
                    pass
    comp_move_atk()


# ПРОВЕРКА ВЫИГРЫША
def check():
    """
    Проверка партии на наличие выигрышной ситуации
    Возвращает:
    0 - в случае победы игрока;
    1 - в случае победы компьютера;
    2 - в случае ничьи
    """
    for i in range(len(rules)):
        if field[rules[i][0]] == field[rules[i][1]] == field[rules[i][2]] in (userFig, compFig):
            return 0 if field[rules[i][0]] == userFig else 1
    if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
        return 2


# ПАРТИЯ ИГРЫ
def main():
    global field, line
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
        line[0], line[1] = line[1], line[0]

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
    if input('Сыграем? (д)').lower() in ('д', 'y'):
        main()
    else:
        input('Выходим')
        exit()
