import logging  # Выводим лог на консоль и в файл
from datetime import datetime  # Дата и время
from time import sleep  # Подписка на события по времени

from FinamPy import FinamPy  # Работа с сервером TRANSAQ
from FinamPy.Config import Config  # Файл конфигурации


logger = logging.getLogger('FinamPy.Stream')  # Будем вести лог


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    fp_provider = FinamPy(Config.AccessToken)  # Провайдер работает со всеми счетами по токену (из файла Config.py)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                        datefmt='%d.%m.%Y %H:%M:%S',  # Формат даты
                        level=logging.DEBUG,  # Уровень логируемых событий NOTSET/DEBUG/INFO/WARNING/ERROR/CRITICAL
                        handlers=[logging.FileHandler('Stream.log'), logging.StreamHandler()])  # Лог записываем в файл и выводим на консоль
    logging.Formatter.converter = lambda *args: datetime.now(tz=fp_provider.tz_msk).timetuple()  # В логе время указываем по МСК

    security_board = 'TQBR'  # Код режима торгов
    security_code = 'SBER'  # Тикер
    # security_board = 'FUT'  # Код режима торгов
    # security_code = 'SiH4'  # Тикер

    # Стакан
    sleep_secs = 5  # Кол-во секунд получения стакана
    logger.info(f'{sleep_secs} секунд стакана {security_board}.{security_code}')
    fp_provider.on_order_book = lambda order_book: logger.info(f'ask = {order_book.asks[0].price} bid = {order_book.bids[0].price}')  # Обработчик события прихода подписки на стакан
    request_id = 'orderbook1'  # Код подписки может быть любым
    fp_provider.subscribe_order_book(security_code, security_board, request_id)  # Подписываемся на стакан тикера
    logger.info(f'Подписка на стакан {request_id} тикера {security_board}.{security_code} создана')
    sleep(sleep_secs)  # Ждем кол-во секунд получения стакана
    logger.info(f'Подписка на стакан {request_id} тикера {security_board}.{security_code} отменена')
    fp_provider.unsubscribe_order_book(request_id, security_code, security_board)  # Отписываемся от стакана тикера

    # Котировки
    # TODO Ждем от Финама подписку на котировки

    # Выход
    fp_provider.close_channel()  # Закрываем канал перед выходом
