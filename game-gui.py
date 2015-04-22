# -*- coding: utf-8 -*-

import random
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

field = []  # поле игры
# Фигуры
empty = ' '
nought = '〇'
cross = '✖'
userFig = cross
compFig = nought
compWinCount = 0
userWinCount = 0
userFirstWinCount = 0
userSecondWinCount = 0
field = [empty]*9
h = True  # индикатор первого хода. True - ещё никто не походил, компьютер ставит случайно. False - первй ход сделан

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        global main_box, file, exitGame, main_frame

        # создание фона окна
        main_frame = QtGui.QWidget()
        self.setCentralWidget(main_frame)

        # создание таблицы(2 столбца)(всё окно)
        main_box = QtGui.QGridLayout()
        main_frame.setLayout(main_box)

        # отображается меню
        self.start_menu()

        # настройки окна
        self.setWindowTitle('Крестики-нолики')

        # создается строка статуса
        self.statusBar()

        # создание кнопки выхода для панели инструментов
        exitGame = QtGui.QAction(QtGui.QIcon('1_3.png'), 'Выйти', self)
        exitGame.setShortcut('Ctrl+Q')
        exitGame.setStatusTip('Выйти из игры')
        self.connect(exitGame, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        # создание панели инструментов
        menu_bar = self.menuBar()
        # создание кнопки файл
        file = menu_bar.addMenu('&Игра')
        # добавление кнопки выхода в меню "файл"
        file.addAction(exitGame)

    # Стартовое меню
    def start_menu(self):
        global box_for_field, frame_for_field, main_box, frame_for_score, frame_for_log, frame_for_chat

        try:
            # удаление рамки с приветствием/полем
            frame_for_field.deleteLater()
            frame_for_field = None
        except NameError:
            pass
        except AttributeError:
            pass

        try:
            # удаление рамки со счетом
            frame_for_score.deleteLater()
            frame_for_score = None

            # удаление рамки с логом
            frame_for_log.deleteLater()
            frame_for_log = None
        except NameError:
            pass
        except AttributeError:
            pass

        try:
            # удаление рамки с чатом
            frame_for_chat.deleteLater()
            frame_for_chat = None
        except NameError:
            pass
        except AttributeError:
            pass

        # создание рамки для приветствия
        frame_for_field = QtGui.QGroupBox('Приветствие')
        frame_for_field.setFixedSize(182, 195)

        # добавление рамки таблицы в коробку
        main_box.addWidget(frame_for_field, 0, 1, 2, 1)

        # создание контейнера с приветствием
        box_for_field = QtGui.QVBoxLayout(frame_for_field)

        # создание приветствия
        label = QtGui.QLabel(u"""<center>Привет!</center>""", frame_for_field)
        # создание кнопки начала игры
        new_game_with_comp_button = QtGui.QPushButton(u"Синглплеер", frame_for_field)
        new_game_with_comp_button.clicked.connect(self.new_game_with_comp)
        new_game_with_player_button = QtGui.QPushButton(u"Мультиплеер", frame_for_field)
        new_game_with_player_button.clicked.connect(self.game_with_player)

        # добавление виджетов
        box_for_field.addWidget(label)
        box_for_field.addWidget(new_game_with_comp_button)
        box_for_field.addWidget(new_game_with_player_button)

    # начало игры с компьютером
    def new_game_with_comp(self):
        global turn, userFig, compFig, frame_for_field, file, exitGame, menuGame
        # рандомизация очередности ходов
        turn = bool(random.getrandbits(1))  # индикатор хода False - игрок не походил, True - игрок сделал ход
        # False - игрок ходит первым, True - компьютер

        # print('очередь', turn)

        try:
            # удаление кнопки выхода в меню
            file.removeAction(menuGame)
        except NameError:
            pass

        # создание новой кнопки выхода в меню
        menuGame = QtGui.QAction(QtGui.QIcon('1_3.png'), 'Вернуться в меню', self)
        menuGame.setShortcut('Ctrl+M')
        menuGame.setStatusTip('Вернуться в главное меню игры')
        self.connect(menuGame, QtCore.SIGNAL('triggered()'), self.start_menu)

        # добавление кнопки перед кнопкой выхода
        file.insertAction(exitGame, menuGame)

        # если первым ходит игрок, он выбирает фигуру
        if turn is False:
            self.choosing()
        else:
            # перемешивание фигур
            x = [cross, nought]
            random.shuffle(x)
            userFig, compFig = x
            self.game_with_comp()

    def nought_choose_button_clicked(self, enabled):
        global userFig, compFig
        if enabled:
            userFig = nought
            compFig = cross
            # print('da')

    def cross_choose_button_clicked(self, enabled):
        global userFig, compFig
        if enabled:
            userFig = cross
            compFig = nought
            # print('da')

    # Выбор фигуры
    def choosing(self):
        global frame_for_field, main_box, frame_for_score, frame_for_log

        # удаление рамки с приветствием/полем
        frame_for_field.deleteLater()
        frame_for_field = None

        # создание новой рамки с выбором фигуры
        frame_for_field = QtGui.QGroupBox('Выберите фигуру')
        frame_for_field.setFixedSize(182, 195)
        main_box.addWidget(frame_for_field, 0, 1, 2, 1)

        # создание контейнера с приветствием
        startbox = QtGui.QVBoxLayout(frame_for_field)

        # создание приветствия
        label = QtGui.QLabel(u"""<center>Привет!</center>""", frame_for_field)
        # создание кнопки начала игры
        cross_choose_button = QtGui.QRadioButton(u"Крестики", frame_for_field)
        nought_choose_button = QtGui.QRadioButton(u"Нолики", frame_for_field)

        # если игрок ничего не нажимал, но крестики всё ещё выделены
        cross_choose_button.setChecked(True)
        if cross_choose_button.isChecked() is True:
            self.cross_choose_button_clicked(True)

        # сслыки на функции
        cross_choose_button.toggled.connect(self.cross_choose_button_clicked)
        nought_choose_button.toggled.connect(self.nought_choose_button_clicked)

        # создание кнопки
        game_with_comp_button = QtGui.QPushButton(u"Играть", frame_for_field)
        game_with_comp_button.clicked.connect(self.game_with_comp)

        # добавление виджетов
        startbox.addWidget(label)
        startbox.addWidget(cross_choose_button)
        startbox.addWidget(nought_choose_button)
        startbox.addWidget(game_with_comp_button)

    # Выводит рамки со счетом и логом
    def print_log_and_score(self):
        global frame_for_field, main_box, frame_for_score, container_for_score, frame_for_log, grid_for_field, text_log

        # удаление рамки с приветствием/полем
        frame_for_field.deleteLater()
        frame_for_field = None
        try:
            # удаление рамки со счетом
            frame_for_score.deleteLater()
            frame_for_score = None

            # удаление рамки с логом
            frame_for_log.deleteLater()
            frame_for_log = None
        except NameError:
            pass
        except AttributeError:
            pass

        # создание новой рамки с полем
        frame_for_field = QtGui.QGroupBox('Игровое поле')
        frame_for_field.setFixedSize(182, 195)
        main_box.addWidget(frame_for_field, 0, 1, 2, 1)
        # создание таблицы с полем
        grid_for_field = QtGui.QGridLayout(frame_for_field)

        # создание рамки для счета
        frame_for_score = QtGui.QGroupBox('Счёт')
        frame_for_score.setFixedSize(200, 65)
        # создание рамки для лога
        frame_for_log = QtGui.QGroupBox('Лог')
        frame_for_log.setFixedSize(200, 125)

        # добавление рамки счета в коробку
        main_box.addWidget(frame_for_score, 0, 0, 1, 1)
        # добавление рамки лога в коробку
        main_box.addWidget(frame_for_log, 1, 0, 1, 1)

        # создание контейнера для счета
        container_for_score = QtGui.QVBoxLayout(frame_for_score)
        # создание контейнера с логом
        container_for_log = QtGui.QVBoxLayout(frame_for_log)

        # создание лога
        text_log = QtGui.QTextEdit()
        text_log.setReadOnly(True)
        container_for_log.addWidget(text_log)

    # Начало игры с другим игроком (пока что работает некорректно)
    def game_with_player(self):
        global field, main_box, grid_for_field, frame_for_field, box_for_field, turn, result, winCount, userWinCount, \
            compWinCount, frame_for_score, container_for_score, score, userFig, compFig, figure, NewGame, file, \
            exitGame, frame_for_chat, userFirstWinCount, userSecondWinCount

        # удаление кнопки новой игры из панели инструментов
        try:
            file.removeAction(NewGame)
        except NameError:
            pass

        NewGame = QtGui.QAction(QtGui.QIcon('1_3.png'), 'Новая игра', self)
        NewGame.setShortcut('Ctrl+N')
        NewGame.setStatusTip('Начать новую игру')
        # self.connect(NewGame, QtCore.SIGNAL('triggered()'), self.start_game_with_player)

        file.insertAction(exitGame, NewGame)

        # создание счета и лога
        self.print_log_and_score()

        # строка со счетом
        winCount = 'Игрок 1 ' + str(userFirstWinCount) + ' - ' + str(userSecondWinCount) + ' Игрок 2'

        print(winCount)
        result = False  # индикатор окончания игры True - игра окончена
        turn = bool(random.getrandbits(1))  # индикатор хода False - игрок не походил, True - игрок сделал ход
        # False - игрок ходит первым, True - компьютер
        # перемешивание фигур
        x = [cross, nought]
        random.shuffle(x)
        userFig, compFig = x
        # строка с отображением фигуры
        fig_display = 'Вы играете за ' + userFig
        print('очередь', turn)
        # try:
        #     figure.deleteLater()
        #     figure = None
        #     score.deleteLater()
        #     score = None
        # except NameError:
        #     pass
        score = QtGui.QLabel(winCount, frame_for_score)
        figure = QtGui.QLabel(fig_display, frame_for_score)
        container_for_score.addWidget(score)
        container_for_score.addWidget(figure)

        # создание рамки для чата
        frame_for_chat = QtGui.QGroupBox('Чат')
        frame_for_chat.setFixedSize(300, 195)
        main_box.addWidget(frame_for_chat, 0, 2, 2, 1)
        # создание контейнера с чатом
        container_for_chat = QtGui.QGridLayout(frame_for_chat)
        text_chat = QtGui.QTextBrowser()
        text_input = QtGui.QTextEdit()
        text_input.setFixedSize(200, 25)
        send_button = QtGui.QPushButton('Отправить')
        send_button.setFixedSize(75, 25)
        container_for_chat.addWidget(text_chat, 0, 0, 1, 2)
        container_for_chat.addWidget(text_input, 1, 0, 1, 1)
        container_for_chat.addWidget(send_button, 1, 1, 1, 1)

        field = [empty]*9
        self.show_field()

    # Отображение чистого поля
    def game_with_comp(self):
        global field, main_box, grid_for_field, frame_for_field, box_for_field, turn, result, winCount, userWinCount, \
            compWinCount, frame_for_score, container_for_score, score, userFig, compFig, figure, index_string_to_log, \
            game_result, finish_row, NewGame, file, exitGame

        # удаление кнопки новой игры из панели инструментов
        try:
            file.removeAction(NewGame)
        except NameError:
            pass

        # создание новой кнопки новой игры из панели инструментов
        NewGame = QtGui.QAction(QtGui.QIcon('1_3.png'), 'Новая игра', self)
        NewGame.setShortcut('Ctrl+N')
        NewGame.setStatusTip('Начать новую игру')
        self.connect(NewGame, QtCore.SIGNAL('triggered()'), self.new_game_with_comp)

        # добавление кнопки перед кнопкой меню
        file.insertAction(menuGame, NewGame)

        # создание счета и лога
        self.print_log_and_score()

        # строка со счетом
        winCount = 'Игрок ' + str(userWinCount) + ' - ' + str(compWinCount) + ' Компьютер'

        game_result = None    # результат игры, вычисляемый check()
        index_string_to_log = 0   # номер клетки, который заносится в лог
        finish_row = []  # список с победной строкой, которая выделится красным

        # print(winCount)
        result = False  # индикатор окончания игры True - игра окончена

        # строка с отображением фигуры
        fig_display = 'Вы играете за ' + userFig

        # занесение информации в окно счета
        score = QtGui.QLabel(winCount, frame_for_score)
        figure = QtGui.QLabel(fig_display, frame_for_score)
        container_for_score.addWidget(score)
        container_for_score.addWidget(figure)

        # обнуление поля
        field = [empty]*9
        # отображение поля
        self.show_field()
        # запуск алгоритма игры
        self.moving()

    # при победе игрока
    def if_winner(self):
        global turn, result, userWinCount, frame_for_field
        userWinCount += 1
        result = True
        turn = False

    # при победе компьютера
    def if_loser(self):
        global turn, result, compWinCount, frame_for_field
        compWinCount += 1
        result = True
        turn = False

    # при ничьей
    def if_draw(self):
        global turn, result, frame_for_field
        result = True
        turn = False

    # ВЫВОД ПОЛЯ НА ЭКРАН
    def show_field(self):
        global frame_for_field, grid_for_field, result, finish_row, main_frame, field_button_group
        print(field)
        j = 0
        # индексы позиций в сетке поля
        pos = [(0, 0), (0, 1), (0, 2),
               (1, 0), (1, 1), (1, 2),
               (2, 0), (2, 1), (2, 2)]

        field_button_group = QtGui.QButtonGroup(main_frame)
        # Создание каждой кнопки и связь с функцией
        one = QtGui.QPushButton(field[0], self)

        two = QtGui.QPushButton(field[1], self)

        three = QtGui.QPushButton(field[2], self)

        four = QtGui.QPushButton(field[3], self)

        five = QtGui.QPushButton(field[4], self)

        six = QtGui.QPushButton(field[5], self)

        seven = QtGui.QPushButton(field[6], self)

        eight = QtGui.QPushButton(field[7], self)

        nine = QtGui.QPushButton(field[8], self)

        # Список с кнопками
        nums = [one, two, three, four, five, six, seven, eight, nine]

        # Расстановка кнопок по клетками в таблице
        for k in range(len(nums)):
            # размер и стиль кнопки
            nums[k].setFixedSize(50, 50)
            nums[k].setStyleSheet('color: black; font-size: 30pt;')
            # если игра окончена, окрашивает в красный победную строку
            if result is True:
                try:
                    for p in finish_row:
                        if k == p:
                            nums[k].setStyleSheet('color: red; font-size: 30pt;')
                except NameError:
                    pass
            else:
                nums[k].setStyleSheet('color: black; font-size: 30pt;')
            field_button_group.addButton(nums[k])
            field_button_group.setId(nums[k], k)
            # добавление кнопки в сетку
            grid_for_field.addWidget(nums[k], pos[j][0], pos[j][1])
            j += 1
        print('rezultat', result)

        field_button_group.buttonClicked[QtGui.QAbstractButton].connect(self.user_move)

        # рисует сетку
        frame_for_field.setLayout(grid_for_field)

    # ХОД КОМПЬЮТЕРА
    # рандомный ход компьютера
    def comp_move_random(self):
        global turn, index_string_to_log
        m = random.choice(range(len(field)))
        print('Ход компьютера: ', m)
        field[m] = compFig
        index_string_to_log = str(m + 1)
        turn = not turn

    # ход компьютера, мешает игроку
    def comp_move_def(self):
        global g, index_string_to_log
        if len(figures_def) != 0:
            # print('индикатор начала защиты')
            m = random.choice(figures_def)
            print('Ход компьютера: ', m)
            field[m] = compFig
            index_string_to_log = str(m + 1)
            g = False
        else:
            pass

    # ход компьютера, заполнение своих ячеек
    def comp_move_atk(self):
        global g, figures_def, index_string_to_log
        g = True  # индикатор защиты. False - ход защиты сделан
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
        self.comp_move_def()
        if g is True:
            try:
                field[m] = compFig
            except UnboundLocalError:
                # если осталась единственная свободная клетка, но ни одно из условий не подошло
                for i in range(len(field)):
                    if field[i] == empty:
                        m = i
            try:
                print('Ход компьютера: ', m)
                field[m] = compFig
                index_string_to_log = str(m + 1)
            except UnboundLocalError:
                pass
        if g is False:
            pass

    # Ход компьютера, основа
    def comp_move(self):
        global figures_atk, figures_def, turn
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
        self.comp_move_atk()
        turn = not turn
        self.moving()

    # Ход игрока
    def user_move(self, button):
        global field_button_group, userFig, turn, index_string_to_log, text_log
        print('нажата кнопка', field_button_group.id(button))
        cell = field_button_group.id(button)
        if turn is False:
            if field[cell] != empty:
                turn = False
                self.statusBar().showMessage('Ячейка занята')
            else:
                field[cell] = userFig
                turn = not turn
                index_string_to_log = str(int(cell)+1)
                text_log.append(time.strftime('%H:%M:%S') + ' Игрок - ' + index_string_to_log)
                self.statusBar().clearMessage()
            self.show_field()
            self.moving()
        else:
            self.status_message_show()

    # Сообщение в статусе по окончании игры
    def status_message_show(self):
        global game_result
        # проверяет результат функции check() и записывает в статус результат игры
        if game_result == 0:
            self.statusBar().showMessage('Игра окончена: Вы выиграли')
        elif game_result == 1:
            self.statusBar().showMessage('Игра окончена: компьютер выиграл')
        elif game_result == 2:
            self.statusBar().showMessage('Игра окончена: ничья')

    # ХОД
    def moving(self):
        global h, turn, result, text_log, index_string_to_log, finish_row, game_result
        print(turn)
        # запускает проверку
        self.check()

        # запускает функцию, соответствующую результату
        if game_result == 0:
            print('ВЫ ПОБЕДИЛИ')
            self.statusBar().showMessage('Вы выиграли')
            self.if_winner()
            print('победа', turn)
        elif game_result == 1:
            print('ПОБЕДИЛ КОМПЬЮТЕР')
            self.statusBar().showMessage('Компьютер выиграл')
            self.if_loser()
            print('поражение', turn)
        elif game_result == 2:
            print('НИЧЬЯ')
            self.statusBar().showMessage('Ничья')
            self.if_draw()
            print('ничья', turn)

        print('rez', result)
        # если матч не окончен, игра продолжается
        if result is False:
            if turn is False:  # если первым должен ходить игрок
                h = False
            else:
                print('h', h)
                if h is True:
                    # если ни одного хода ещё не сделано, компьютер ходит рандомно
                    self.comp_move_random()
                    h = False
                else:
                    # иначе проходит по всему алгоритму
                    self.comp_move()

                # если существует информация о ходе
                if index_string_to_log != 0:
                    text_log.append(time.strftime('%H:%M:%S') + ' Компьютер - ' + index_string_to_log)
                else:
                    pass
            self.show_field()
        # если матч окончен
        else:
            # фигуры окрашиваются
            self.show_field()
            # меняет очередность ходов
            turn = not turn
            # появляется сообщение в статусе
            self.status_message_show()

    # ПРОВЕРКА ВЫИГРЫША
    def check(self):
        global finish_row, game_result
        """
        Проверка партии на наличие выигрышной ситуации
        Возвращает:
        0 - в случае победы игрока;
        1 - в случае победы компьютера;
        2 - в случае ничьи
        """

        # проходит по всем возможным победным строкам
        for i in rules:
            # если значения каждого из трех индексов равны (строка реально победная)
            if field[i[0]] == field[i[1]] == field[i[2]] in (userFig, compFig):
                # если победа за игроком
                if field[i[0]] == userFig:
                    game_result = 0
                # если победа за компьютером
                else:
                    game_result = 1
                # сюда вносится эта строка
                finish_row = list(i)
                print(finish_row)

        if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
            game_result = 2

if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
