from enum import Enum

class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = "Полученный код состояния не равен ожидаемому"
    BASKED_SUMMARY_INFO = "Сводная информация о заказе не соответствует списку товаров в корзине"