# coding: utf-8
"""
Логическая составляющя клиента
"""
# НЕРАБОЧАЯ ВЕРСИЯ!

import nc_net


class WrongData(Exception):
    """
    Исключение, возникающее при передаче функциям неверных типов данных
    """
    pass


def start_game(host=-1):
    """
    СОЗДАТЬ ПАРТИЮ
    Принимает:
        host (int, необязательный, равен -1 по умолчанию) - идентификатор игрока, с которым хотелось бы сыграть
    Возвращает:
    ###Возможно, лучще возвращаемые значения заменить на однозначно интерпретируемые коды###
        tuple:
            1) boolean - успешно ли создание партии
                True - успешно
                False - провал
            2) boolean (только если создание партии успешно)- очередность ходов
                True - текущий игрок ходит первым
                False - текущий игрок ходит вторым
            3) int (только если текущий игрок ходит вторым) - фигура противника
                0 - крестики
                1 - нолики
            В случае отсутсвия возращаемого значения элемент заполняется None
            Примеры:
                (True, False, 0),
                (True, True, None),
                (False, None, None)

    Если первым ходит текущий игрок, должна быть вызвана функция выбора фигуры choosing()
    """
    if type(host) != int:
        raise WrongData

    value = nc_net.transfer() if host == -1 else nc_net.transfer(host=host)  # обмен данными с сервером

    # несогласованный пример. лишь для наглядности
    # будут вложенные условия
    if value == 1:
        return False, None, None
    elif value == 2:
        return True, True, None
    elif value == 3:
        return True, False, 0
    elif value == 4:
        return True, False, 1

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
    if figure not in (0,1):
        raise WrongData
    value = nc_net.transfer()  # обмен данными с сервером
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
        raise WrongData
    value = nc_net.transfer()
    if value is True:
        return True
    elif value is False:
        return False
