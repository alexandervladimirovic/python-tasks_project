import os
import uuid
from datetime import datetime, timedelta
import logging

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers= [
        logging.FileHandler('logs/task.log')
        # logging.StreamHandler()
    ]
)

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
    def __init__(self, title: str, description: str, category: str, due_date: int):

        if not title or not isinstance(title, str):
            logger.error("Введена пустая задача")
            raise ValueError("Задача не может быть пустой и должна быть строкой")

        if not description or not isinstance(description, str):
            logger.error("Введено пустое описание")
            raise ValueError("Описание задачи не может быть пустым и должно быть строкой")

        if not category or not isinstance(category, str):
            logger.error("Введена пустая категория")
            raise ValueError("Категория задачи не может быть пустой и должна быть строкой")

        if not isinstance(due_date, int):
            logger.error("Введен пустой срок выполнения")
            raise ValueError("Срок выполнения задачи не может быть пустой и должен быть числом")

        self.id = str(uuid.uuid4())
        self.priority = "средний"
        self.due_date = datetime.now() + timedelta(days=due_date)
        self.status = "не выполнено"


        self.title = title
        self.description = description
        self.category = category

        logger.info("Создана задача: %s (ID: %s, срок выполнения до: %s)", self.title, self.id, self.due_date.strftime('%d.%m.%Y'))

    def __repr__(self):
        """
        Возвращает строковое представление объекта
        """
        return f"Задача: {self.title}, Описание: {self.description}, Категория:{self.category}, Срок выполнения до: {self.due_date.strftime('%d.%m.%Y')}, Приоритет: {self.priority}, Статус: {self.status}"
    
    def __eq__(self, other):
        """
        Проверяет равенство объектов
        """
        if isinstance(other, Task):
            return self.id == other.id

        return False

    def to_dict(self):
        """
        Преобразует объект книги в словарь
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }