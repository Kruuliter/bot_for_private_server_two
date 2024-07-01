from configparser import ConfigParser
from pathlib import Path



def configs(filename='config.ini', section='mysql'):
    """
    Чтение файла формата ini для получение настроек для дискорд бота
    :param section: название секции в файле ini
    :param filename: название файла настроек
    :return: возвращает список типа ключ - значение (dict)
    """
    HERE = Path(__file__).parent.resolve() # получаем расположение текущего файла
    CONFIG_PATH = HERE / filename # соединяем расположение и название файла для получения полного путя к файлу
    parser = ConfigParser() # создаем экземпляр парсера конфигурации
    parser.read(CONFIG_PATH) # читаем весь файл ini

    bibles = {}

    if parser.has_section(section): # проверяет, существует ли определённая секция в файле ini, обозначается внутри []
        items = parser.items(section) # получение все пары ключ - значение

        # цикл можно улучшить, но оставлю так
        for item in items: # перемещаем из одного массива пары ключ - значение в другой
            bibles[item[0]] = item[1]
    else:
        raise Exception(f"{section} not found in the {CONFIG_PATH} file") # вызывает ошибку

    return bibles # возвращаем заполненный массив