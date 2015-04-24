# coding: utf-8
"""
Логическая составляющая клиента
"""
# НЕРАБОЧАЯ ВЕРСИЯ!

import nc_net
host = 0  # данные, необходимые для идентификации партии на сервере

class WrongDataError(Exception):
    """
    Исключение, возникающее при передаче функциям неверных типов данных
    Необходимо перехватывать в nc_gui, либо можно заменить на одно возвращаемых
    фунциями значений
    """
    pass








def start_game(host=-1):
    """
    СОЗДАТЬ ПАРТИЮ
    Принимает:
        host (int, необязательный, равен -1 по умолчанию) - идентификатор игрока, с которым хотелось бы сыграть
    Возвращает:
        int:
            0 - партия не создана, нет соединения/превышено время ожидания
            1 - партия не создана, неизвестная ошибка
            2 - партия создана, текущий игрок ходит первым, нужно выбрать фигуру
            3 - партия создана, текущий игрок ходит вторым, другой игрок выбрал крестики
            4 - партия создана, текущий игрок ходит вторым, другой игрок выбрал нолики
    """
    if type(host) != int:
        raise WrongDataError

    value = nc_net.make_party(None) if host == -1 else nc_net.make_party(None)  # обмен данными с сервером

    # несогласованный пример. лишь для наглядности
    if value == 0:
        return 0
    elif value == 1:
        return 1
    elif value == 2:
        return 2
    elif value == 3:
        return 3
    elif value == 4:
        return 4


def choosing(figure):
    """
    ВЫБОР ФИГУРЫ
    Принимает:
        int - идентификатор фигуры (крестики или нолик)
            0 - крестик
            1 - нолик
    Возвращает:
        boolean - успешен ли выбор фигуры
            True - успешен
            False - нет
    """
    if figure not in (0, 1):
        raise WrongDataError

    value = nc_net.transfer(())  # обмен данными с сервером
    if value is True:
        return True
    elif value is False:
        return False


def moving(ceil):
    """
    ХОД ИГРОКА
    Принимает:
        int - номер ячейки, выбранной игроком
            0 - крестик
            1 - нолик
    Возвращает:
        boolean - успешен ли выбор фигуры
            True - успешен
            False - нет
    """
    if ceil not in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        raise WrongDataError
    value = nc_net.transfer(None)
    if value is True:
        return True
    elif value is False:
        return False
