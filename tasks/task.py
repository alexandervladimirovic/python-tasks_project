import os
import uuid
import logging.config
from datetime import datetime, timedelta

import yaml

if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logging(config_path="logs/logging_config.yaml"):
    
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

setup_logging()

logger = logging.getLogger(__name__)


class Task:
    """
    Класс для представления задачи.

    Атрибуты:

        id: Уникальный идентификатор задачи
        title: Название задачи
        description: Подробное описание задачи
        category: Категория задачи
        due_date: Срок выполнения задачи
        priority: Приоритет задачи 
        status: Статус выполнения задачи
        """
    def __init__(self, title: str, description: str, category: str, due_date: int | datetime, priority: str = "средний", status: str = "не выполнено"):

        self.id = str(uuid.uuid4())
        self.title = self.validate_string(title, "Название задачи")
        self.description = self.validate_string(description, "Описание задачи")
        self.category = self.validate_string(category, "Категория задачи")
        self.due_date = self.validate_date(due_date)
        self.priority = self.validate_priority(priority)
        self.status = self.validate_status(status)

        logger.info("Создана задача: %s (ID: %s, срок выполнения до: %s)",
                    self.title, self.id, self.due_date.strftime('%d.%m.%Y'))

    
    @staticmethod
    def validate_string(value: str, field_name: str) -> str:

        if not value or not isinstance(value, str):
            logger.error("Неверный тип данных для %s", field_name)
            raise TypeError(f"{field_name.capitalize()} должен иметь строковый тип")
        return value
    
    @staticmethod
    def validate_date(value: int | datetime) -> datetime:

        if isinstance(value, int) and value > 0:
            return datetime.now() + timedelta(days=value)
        elif isinstance(value, datetime):
            return value
        else:
            logger.error("Неверный тип данных для срока выполнения задачи")
            raise TypeError("Срок выполнения задачи должен иметь тип datetime или int")

    @staticmethod
    def validate_priority(value: str) -> str:

        if value not in {"низкий", "средний", "высокий"}:
            logger.error("Неверный тип данных для приоритета задачи")
            raise ValueError("Приоритет задачи должен быть 'низкий', 'средний' или 'высокий'")
        
        return value
    
    @staticmethod
    def validate_status(value: str) -> str:

        if value not in {"выполнено", "не выполнено"}:
            logger.error("Неверный тип данных для статуса задачи")
            raise ValueError("Статус задачи должен быть 'выполнено' или 'не выполнено'")
        
        return value
    
    def __repr__(self):
        """
        Возвращает строковое представление объекта
        """
        return f"Задача: {self.title}, Описание: {self.description}, Категория:{self.category}, Срок выполнения до: {self.due_date.strftime('%d.%m.%Y')}, Приоритет: {self.priority}, Статус: {self.status}" 
    
    def __eq__(self, other) -> bool:
        """
        Проверяет равенство объектов
        """
        if isinstance(other, Task):
            return self.id == other.id

        return False

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.strftime('%d.%m.%Y') if isinstance(self.due_date, datetime) else self.due_date,
            "priority": self.priority,
            "status": self.status
        }