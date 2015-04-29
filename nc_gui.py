# -*- coding: utf-8 -*-
"""
Графический интерфейс клиента на PyQT
"""

# В ЭТОЙ ВЕРСИИ НЕКОРРЕКТНО РАБОТАЕТ ОЧЕРЕДНОСТЬ ХОДОВ! ТРЕБУЕТСЯ ЛОГИЧЕСКАЯ СОСТАВЛЯЮЩАЯ

import random
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

from nc_logic import start_game, moving

field = []  # поле игры
# Фигуры
empty = ' '
nought = '〇'
cross = '✖'
compWinCount = 0
userWinCount = 0
userFirstWinCount = 0
userSecondWinCount = 0

# правила для определения выигрыша
rules = ((0, 1, 2), (3, 4, 5), (6, 7, 8),  # по горизонтали
         (0, 3, 6), (1, 4, 7), (2, 5, 8),  # по вертикали
         (0, 4, 8), (2, 4, 6))  # по диагонали


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        global main_container, main_widget, file, exitGame
        QtGui.QMainWindow.__init__(self)

        # создание главного виджета
        main_widget = QtGui.QWidget()
        self.setCentralWidget(main_widget)

        # создание сетки, в которую помещаются остальные виджеты
        main_container = QtGui.QGridLayout()
        main_widget.setLayout(main_container)

        # название окна
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

        # отображение меню
        self.menu()

    # функция для подгонки размера окна
    def resize_window(self):
        # выравнивание размера окна
        main_widget.adjustSize()
        self.adjustSize()
        MainWindow.adjustSize(self)

    # отображает меню
    def menu(self):
        global main_container, main_widget, file, menu_panel, menu_image_label
        try:
            # удаление всех рамок, очистка сетки
            for i in reversed(range(main_container.count())):
                main_container.itemAt(i).widget().deleteLater()
                main_container.itemAt(i).widget().setParent(None)
        except NameError:
            pass
        except AttributeError:
            pass
        except RuntimeError:
            pass

        # удаление кнопки выхода в меню
        try:
            file.removeAction(menuGame)
        except NameError:
            pass

        # создание рамки для меню
        menu_panel = QtGui.QGroupBox('Меню')

        # добавление рамки в сетку
        main_container.addWidget(menu_panel, 0, 0, 1, 1)

        # создание контейнера для кнопок меню
        menu_container = QtGui.QVBoxLayout(menu_panel)

        # создание кнопки игры с компьютером
        comp_game_button = QtGui.QPushButton(u"Синглплеер", menu_panel)
        # comp_game_button.clicked.connect(self.new_game_with_comp)
        comp_game_button.setMinimumSize(125, 50)

        # создание кнопки игры с другим игроком
        player_game_button = QtGui.QPushButton(u"Мультиплеер", menu_panel)
        player_game_button.clicked.connect(self.start_multiplayer)
        player_game_button.setMinimumSize(125, 50)

        # создание кнопки выхода
        quit_game_button = QtGui.QPushButton(u"Выход", menu_panel)
        self.connect(quit_game_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        quit_game_button.setMinimumSize(125, 50)

        # добавление кнопок
        menu_container.addWidget(comp_game_button)
        menu_container.addWidget(player_game_button)
        menu_container.addWidget(quit_game_button)

        # установка оптимального размера рамки
        menu_panel.setMinimumSize(menu_panel.sizeHint())

        # создание изображения для меню
        image = QtGui.QImage('1_3.png')
        # создание контейнера для изображения
        menu_image_label = QtGui.QLabel()
        # добавление изображения
        menu_image_label.setPixmap(QtGui.QPixmap.fromImage(image))
        menu_image_label.setAlignment(QtCore.Qt.AlignCenter)

        # установка оптимального размера картинки
        menu_image_label.setMinimumSize(menu_image_label.sizeHint())

        # добавление изображения в сетку
        main_container.addWidget(menu_image_label, 0, 1, 1, 1)

        self.resize_window()

    # подготовка к сетевой игре
    def start_multiplayer(self):
        global file, exitGame, menuGame, menu_panel, turn, userFig

        # создание новой кнопки выхода в меню
        menuGame = QtGui.QAction(QtGui.QIcon('1_3.png'), 'Вернуться в меню', self)
        menuGame.setShortcut('Ctrl+M')
        menuGame.setStatusTip('Вернуться в главное меню игры')
        self.connect(menuGame, QtCore.SIGNAL('triggered()'), self.menu)

        # добавление кнопки перед кнопкой выхода
        file.insertAction(exitGame, menuGame)

        try:
            # удаление всех рамок, очистка сетки
            for i in reversed(range(main_container.count())):
                main_container.itemAt(i).widget().deleteLater()
                main_container.itemAt(i).widget().setParent(None)
        except NameError:
            pass
        except AttributeError:
            pass
        except RuntimeError:
            pass

        # гифка ожидания
        movie_screen = QtGui.QLabel()
        main_container.addWidget(movie_screen, 0, 0)
        movie = QtGui.QMovie('1_4.gif', QtCore.QByteArray())

        movie.setCacheMode(QtGui.QMovie.CacheAll)
        movie.setSpeed(100)
        movie_screen.setMovie(movie)
        movie.start()

        self.resize_window()

        """
        Здесь клиент вызывает функцию из логики и получает данные о партии
        В зависимости от значения, определяется очередность ходов
        """

        # вызывает функцию из логики, создает очередность ходов, выдает фигуру
        if start_game(1) == 2:
            turn = False
            self.choosing()
        elif start_game(1) == 3:
            turn = True
            userFig = nought
            self.multiplayer()
        elif start_game(1) == 4:
            turn = True
            userFig = cross
            self.multiplayer()
        else:
            self.menu()

    # если кнопку не нажимали
    def choose_button_clicked(self, button):
        global userFig, compFig, choosing_button_group
        print('da')
        if choosing_button_group.id(button) == 0:
            userFig = cross
            compFig = nought
        elif choosing_button_group.id(button) == 1:
            userFig = nought
            compFig = cross

    # окно выбора фигуры
    def choosing(self):
        global choosing_panel, main_container, score_panel, log_panel, choosing_button_group

        choosing_button_group = QtGui.QButtonGroup(main_widget)

        try:
            # удаление всех рамок, очистка сетки
            for i in reversed(range(main_container.count())):
                main_container.itemAt(i).widget().deleteLater()
                main_container.itemAt(i).widget().setParent(None)
        except NameError:
            pass
        except AttributeError:
            pass
        except RuntimeError:
            pass

        # создание новой рамки с выбором фигуры
        choosing_panel = QtGui.QGroupBox('Выберите фигуру')
        main_container.addWidget(choosing_panel, 0, 1, 2, 1)

        # создание контейнера с приветствием
        choosing_container = QtGui.QVBoxLayout(choosing_panel)

        # создание приветствия
        label = QtGui.QLabel(u"""<center>Привет!</center>""", choosing_panel)
        # создание кнопок выбора фигуры
        cross_choose_button = QtGui.QRadioButton(u"Крестики", choosing_panel)
        nought_choose_button = QtGui.QRadioButton(u"Нолики", choosing_panel)
        # добавление кнопок выбора фигуры
        choosing_button_group.addButton(cross_choose_button)
        choosing_button_group.addButton(nought_choose_button)
        # присвоение идентификаторов
        choosing_button_group.setId(cross_choose_button, 0)
        choosing_button_group.setId(nought_choose_button, 1)

        # если игрок ничего не нажимал, но крестики всё ещё выделены
        cross_choose_button.setChecked(True)
        if cross_choose_button.isChecked() is True:
            self.choose_button_clicked(cross_choose_button)

        # сслыки на функции
        choosing_button_group.buttonClicked[QtGui.QAbstractButton].connect(self.choose_button_clicked)

        # создание кнопки
        multiplayer_button = QtGui.QPushButton(u"Играть", choosing_panel)
        multiplayer_button.clicked.connect(self.multiplayer)

        # добавление виджетов
        choosing_container.addWidget(label)
        choosing_container.addWidget(cross_choose_button)
        choosing_container.addWidget(nought_choose_button)
        choosing_container.addWidget(multiplayer_button)

    def multiplayer(self):
        global file, exitGame, menuGame, menu_panel, result, game_result, field, win_counter, score

        field = [empty]*9
        game_result = None
        result = False  # индикатор окончания игры True - игра окончена
        self.print_field()
        self.print_chat()

        # строка со счетом
        win_counter = 'Игрок ' + str(userFirstWinCount) + ' - ' + str(userSecondWinCount) + ' Компьютер'

        # строка с отображением фигуры
        fig_display = 'Вы играете за ' + userFig

        # занесение информации в окно счета
        score = QtGui.QLabel(win_counter, score_panel)
        figure = QtGui.QLabel(fig_display, score_panel)
        score_container.addWidget(score)
        score_container.addWidget(figure)

        self.show_field()

    # выводит рамки с полем, счетом и логом
    def print_field(self):
        global main_container   # главная сетка
        global field_panel, field_container     # игровое поле
        global score_panel, score_container  # счет
        global log_panel, text_log    # лог

        try:
            # удаление всех рамок, очистка сетки
            for i in reversed(range(main_container.count())):
                main_container.itemAt(i).widget().deleteLater()
                main_container.itemAt(i).widget().setParent(None)
        except NameError:
            pass
        except AttributeError:
            pass
        except RuntimeError:
            pass

        # создание новой рамки с полем
        field_panel = QtGui.QGroupBox('Игровое поле')

        # добавление рамки с полем в сетку
        main_container.addWidget(field_panel, 0, 1, 2, 1)

        # создание контейнера для поля
        field_container = QtGui.QGridLayout(field_panel)

        # создание новой рамки со счетом
        score_panel = QtGui.QGroupBox('Счёт')

        # добавление рамки со счетом в сетку
        main_container.addWidget(score_panel, 0, 0, 1, 1)

        # создание контейнера для счета
        score_container = QtGui.QVBoxLayout(score_panel)

        # создание новой рамки с логом
        log_panel = QtGui.QGroupBox('Лог')

        # добавление рамки с логом в сетку
        main_container.addWidget(log_panel, 1, 0, 1, 1)

        # создание контейнера с логом
        log_container = QtGui.QVBoxLayout(log_panel)

        # создание лога
        text_log = QtGui.QTextEdit()
        text_log.setReadOnly(True)
        log_container.addWidget(text_log)

    # выводит чат (только для мультиплеера)
    def print_chat(self):
        global chat_panel, main_container
        try:
            # удаление рамки с чатом
            chat_panel.deleteLater()
            chat_panel = None
        except NameError:
            pass
        except AttributeError:
            pass
        except RuntimeError:
            pass

        # создание новой рамки с чатом
        chat_panel = QtGui.QGroupBox('Чат')

        # добавление рамки с чатом в сетку
        main_container.addWidget(chat_panel, 0, 2, 2, 1)

        # создание контейнера с чатом
        chat_container = QtGui.QGridLayout(chat_panel)

        # создание истории чата
        text_chat = QtGui.QTextEdit()
        text_chat.setReadOnly(True)
        chat_container.addWidget(text_chat, 0, 0, 1, 2)

        # создание поля ввода сообщения
        input_chat = QtGui.QTextEdit()
        input_chat.setFixedHeight(25)
        input_chat.setMinimumWidth(200)
        chat_container.addWidget(input_chat, 1, 0, 1, 1)

        # создание поля ввода сообщения
        send_chat = QtGui.QPushButton('Send')
        send_chat.setFixedSize(75, 25)
        chat_container.addWidget(send_chat, 1, 1, 1, 1)

    # отображение поля
    def show_field(self):
        global field_panel, field_container, field_button_group     # игровое поле
        global result   # параметры выигрыша
        print(field)
        j = 0
        # индексы позиций в сетке поля
        pos = [(0, 0), (0, 1), (0, 2),
               (1, 0), (1, 1), (1, 2),
               (2, 0), (2, 1), (2, 2)]

        # создается группа кнопок
        field_button_group = QtGui.QButtonGroup()

        # создание и настройка каждой кнопки
        for k in range(len(field)):

            # создается кнопка
            button = QtGui.QPushButton(field[k], self)

            # размер и стиль кнопки
            button.setMinimumSize(50, 50)
            button.setStyleSheet('color: black; font-size: 30pt;')

            # если игра окончена, окрашивает в красный победную строку
            if result is True:
                try:
                    for p in finish_row:
                        if k == p:
                            button.setStyleSheet('color: red; font-size: 30pt;')
                except NameError:
                    pass
            else:
                button.setStyleSheet('color: black; font-size: 30pt;')

            # кнопка добавляется в группу
            field_button_group.addButton(button)
            # присвоение идентификатора
            field_button_group.setId(button, k)

            # добавление кнопки в сетку поля
            field_container.addWidget(button, pos[j][0], pos[j][1])
            j += 1

        field_button_group.buttonClicked[QtGui.QAbstractButton].connect(self.user_move)

        # отображает поле
        field_panel.setLayout(field_container)

    # ход игрока
    # принимается нажатая кнопка
    def user_move(self, button):
        global field_button_group, userFig, turn, index_string_to_log, text_log, cell
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

    def moving(self):
        global userFirstWinCount, userSecondWinCount, win_counter, score, score_container
        global result, turn
        # запускает проверку
        self.check()

        # запускает функцию, соответствующую результату
        if game_result is not None:
            if game_result == 0:
                print('ВЫ ПОБЕДИЛИ')
                userFirstWinCount += 1
            elif game_result == 1:
                print('ПОБЕДИЛ Второй игрок')
                userSecondWinCount += 1
            elif game_result == 2:
                print('НИЧЬЯ')

            # создание новой строки со счетеом
            win_counter = 'Игрок ' + str(userFirstWinCount) + ' - ' + str(userSecondWinCount) + ' Компьютер'

            # удаление старого счета
            score.deleteLater()
            score = None

            # создание нового счета
            score = QtGui.QLabel(win_counter, score_panel)
            score_container.insertWidget(0, score)

            # отображение статуса о результате игры
            self.status_message_show()
            # индикатор окончания игры
            result = True
            # запрет дальнейшего хода
            turn = True

        """
        Здесь начинается самое веселье. Данный игрок ходить уже не может и ему нужно отправить информацию о своём ходе
        на сервер, войти в режим ожидания и получить информацию о ходе противника
        Когда информация о ходе противника получена 'turn' становится 'False' и игрок снова может ходить

        Этот клиент должен получить номер клетки 'cell', в которую походил противник
        """
        turn = False
        # if moving(cell) is True:
        #     turn = True
        # else:
        #     turn = False

        self.show_field()

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

        if len(list(filter(lambda x: x == empty, field))) == 0:  # если нет больше пустых клеток
            game_result = 2

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


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
