# coding: utf-8
# author: become-iron (https://github.com/become-iron)

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
    # print('индикатор начала атаки')
    figures_atk_third = []  # атака только на те клетки, где компьютер близок к победе
    figures_atk_second = []  # атака только на ближайшие клетки, где уже стоит фигура компьютера
    figures_atk_second_except = []  # клетки, занятые игроком
    for i in rules:
        count = 0
        collect = []   # тут хранятся индексы двух знаятых ячеек
        for j in i:
            if field[j] == compFig:
                count += 1
                collect.append(j)
        # print('счетчик просмотра, проход по ', i, ': ', count)
        if count == 2:
            figures_atk_third += i
            for k in collect:
                figures_atk_third.remove(k)
            figures_atk_third = list(set(figures_atk_third).intersection(set(figures_atk)))
            # print('индикатор третьей атаки', figures_atk_third)
            try:
                m = random.choice(figures_atk_third)
                figures_def = []
                break
            except IndexError:
                pass
        elif count == 1:
            for j in i:
                if field[j] == compFig:
                    figures_atk_second += i
                    for k in figures_atk_second:
                        if field[k] == userFig:
                            for n in i:
                                figures_atk_second.remove(n)

                    # TODO: эту хуйню нужно допилить, чтобы сделать бота умнее, чтобы он впоследствии захватил мир
                    # # этот цикл находит пересечение нескольких рядов, в которых находятся символы компьютера
                    # for b in rules:
                    #     for k in b:
                    #         if field[k] == compFig:
                    #             if len(set(i).intersection(set(b))) == 1:
                    #                 print('kek 1', figures_atk_second_except)
                    #                 # пересечение двух рядов, в каждый из которых входит символ компьютера
                    #                 figures_atk_second_except = list(set(i).intersection(set(b)))
                    #                 print('kek 2', figures_atk_second_except)
                    #                 # исключение занятых клеток
                    #                 figures_atk_second_except = list(set(figures_atk_second_except).intersection(set(figures_atk)))
                    #                 # если пересечение нашлось, то но становится решением
                    #                 print('kek 3', figures_atk_second_except)
                    #                 print('индикатор до второй атаки', figures_atk_second)
                    #                 for p in figures_atk_second:
                    #                     if field[p] == userFig:
                    #                         for n in i:
                    #                             figures_atk_second_except.remove(n)
                    #                 print('kek 4', figures_atk_second_except)
                    #                 if len(figures_atk_second_except) != 0:
                    #                     figures_atk_second = figures_atk_second_except

            # пересечение со списком всех доступных клеток, убирает все занятые клетки
            figures_atk_second = list(set(figures_atk_second).intersection(set(figures_atk)))
            # print('индикатор второй атаки', figures_atk_second)
            try:
                m = random.choice(figures_atk_second)
            except IndexError:
                pass
        elif count == 0:
            # print('индикатор первой атаки', figures_atk)
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
            for i in range(len(field)):
                if field[i] == empty:
                    m = i
                    print('Ход компьютера: ', m)
        field[m] = compFig
    if g is False:
        pass


def comp_move():
    global figures_atk, figures_def
    # global field
    # field = []   # здесь хранятся значения всех клеток
    # for i in range(len(field)):
    #     # составление списка со всеми значениями
    #     field += [field[i]]
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
    # убирает из вариантов занятые клетки
    for i in range(len(figures_atk)):
        for j in range(len(field)):
            if field[j] != empty:
                try:
                    figures_atk.remove(j)
                except ValueError:
                    pass
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
