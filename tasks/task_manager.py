import os
import json
import logging
from datetime import datetime, timedelta

import yaml
import tabulate
from colorama import Fore, Style

from .task import Task

if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logging(config_path="logs/logging_config.yaml"):
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

setup_logging()

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, filename="tasks.json"):

        self.filename = filename
        self.tasks = {}
        self.load_json()

    def add_task(self, title: str, description: str, category: str, due_date: int | datetime, priority: str = "средний", status: str = "не выполнено"):
        """
        Добавляет задачу в список задач
        """
            
        try:
            new_tasks = Task(title, description, category, due_date, priority, status)
            self.tasks[new_tasks.id] = new_tasks

            logger.info("Добавлена задача: %s (Приоритет: %s, до %s)", title, new_tasks.priority, new_tasks.due_date.strftime('%d.%m.%Y'))

        except TypeError as e:
            logger.error("Ошибка при добавлении задачи: %s", e)
            raise
        except Exception as e:
            logger.error("Неизвестная ошибка при добавлении задачи: %s", e)
            raise

    def delete_task_by_id(self, task_id: str):
        """
        Удаляет задачу из списка задач по её id
        """
        task_delete = self.tasks.get(task_id)

        if task_delete:
            del self.tasks[task_id]
            logger.info("Задача с id %s удалена", task_id)
            print(f"Задача с id {task_id} удалена")
            # self.save_json()
        else:
            logger.error("Удаление задачи не удалось: задача с id %s отсутствует в списке.", task_id)
            print(f"Задача с id {task_id} отсутствует.")
            raise ValueError(f"Удаление задачи не удалось: задача с id {task_id} отсутствует в списке.")

    def delete_task_by_category(self, category: str):
        """
        Удаляет задачу по категории
        """
        tasks_category = [task for task in self.tasks.values() if task.category == category]

        if len(tasks_category) == 1:
            
            selected_task = tasks_category[0]
            del self.tasks[selected_task.id]
            logger.info("Задача с ID '%s' удалена.", selected_task.id)
            print(f"Задача '{selected_task.title}' удалена.")
            # self.save_json()
            return

        if not tasks_category:
            logger.warning("Задачи с категорией '%s' не найдены", category)
            raise ValueError (f"Удаление задачи не удалось: задачи с категорией {category} не найдены")

        print(f"Задачи с категорией {category}:")

        for i, task in enumerate(tasks_category, start=1):
            print(f"{i}. {task.title} (ID: {task.id[:10]}) - {task.description}")

        try:

            choice = int(input(f"Введите номер задачи для удаления (1-{len(tasks_category)}), для отмены введите '0': "))

            if choice == 0:
                print("Отмена удаления задачи.")
                return

            if not 1 <= choice <= len(tasks_category):
                raise ValueError("Неверный номер задачи")

            selected_task = tasks_category[choice - 1]
            self.delete_task_by_id(selected_task.id)

            logger.info("Задача с ID '%s' удалена.", selected_task.id)
            self.save_json()
            print(f"Задача '{selected_task.title}' удалена.")

        except ValueError as e:
            logger.error("Ошибка ввода, неправильные параметры ввода: %s", e)
            print("Неправильные параметры ввода, повторите попытку снова.")

        except Exception as e:
            logger.error("Неизвестная ошибка при удалении задачи: %s", e)
            print("Произошла неизвестная ошибка при удалении задачи.")

    def view_tasks(self, tasks, category=None) -> str:
        """
        Выводит список задач с визуальной подсветкой задач с высоким приоритетом.
        """
        filter_task = [task for task in tasks.values() if category is None or task.category == category]

        if not filter_task:
            logger.warning("Задачи не найдены")
            return f"Нет задач с категорией '{category}'" if category else "Нет задач"

        table = []
        for task in filter_task:
            priority_color = (
                Fore.RED if task.priority == "высокий" else
                Fore.YELLOW if task.priority == "средний" else
                Fore.GREEN
            )

            status_color = (
                Fore.GREEN if task.status == "выполнено" else
                Fore.RED
            )
            table.append([
                task.id[:10],
                task.title,
                task.description,
                task.category,
                task.due_date.strftime('%d.%m.%Y'),
                f"{priority_color}{task.priority}{Style.RESET_ALL}",
                f"{status_color}{task.status}{Style.RESET_ALL}"
            ])

        headers = ["ID", "Задача", "Описание", "Категория", "Срок выполнения (до)", "Приоритет", "Статус"]

        return tabulate.tabulate(table, headers=headers, tablefmt="grid")

    def search_task(self, **kwargs):
        """
        Ищет задачи по переданным параметрам (title, description, category, priority, status).
        
        Параметры поиска передаются через ключевые аргументы (kwargs).
        """
        if not self.tasks:
            logger.warning("Неудачный поиск. Библиотека пуста")
            return []
        
        if not kwargs:
            logger.warning("Неудачный поиск. Не указаны параметры поиска")
            return []

        sup_keys = {"title", "description", "category", "priority", "status"}
        search = {key: value for key, value in kwargs.items() if key in sup_keys}

        def validate_type(key, value):
            if value and not isinstance(value, str):
                logger.error("Неверный тип данных для %s", key)
                raise TypeError(f"{key.capitalize()} должен иметь строковый тип")

        for key, value in search.items():
            validate_type(key, value)

        result = [
            task for task in self.tasks.values() if
            all(
                getattr(task, key).lower() == value.lower() 
                for key, value in search.items() 
                if value is not None
            )
        ]

        if result:
            logger.info("Найдены задачи: %s", [task.to_dict() for task in result])
        else:
            logger.warning("Задачи по заданным критериям не найдены: %s", search)
            return []
        
        return result

    def update_task(self, task_id: str, title: str = None, description: str = None, category: str = None, due_date: int | datetime = None, priority: str = None, status: str = None):

        task = self.tasks.get(task_id)

        if not task:
            logger.error("Задача с ID '%s' не найдена.", task_id)
            raise KeyError(f"Задача с ID '{task_id}' не найдена.")
        
        if title:
            task.title = title

        if description:
            task.description = description

        if category:
            task.category = category

        if due_date:
            task.due_date = self.validate_due_date(due_date)

        if priority:
            task.priority = self.validate_priority(priority)

        if status:
            task.status = self.validate_status(status)

        logging.info("Задача обновлена: %s (ID: %s)", task.title, task.id)
        return task

    @staticmethod
    def validate_due_date(due_date):
        """
        Проверяет и преобразует срок выполнения задачи.
        Принимает:
        - int: Количество дней от текущей даты.
        - datetime: Объект даты.
        - str: Строка в формате 'YYYY-MM-DD' или 'DD.MM.YYYY'.
        """
        if isinstance(due_date, int):
            return datetime.now() + timedelta(days=due_date)
        elif isinstance(due_date, datetime):
            return due_date

        raise ValueError("Неверный формат даты. Допустимые типы: int, datetime, str (формат 'YYYY-MM-DD' или 'DD.MM.YYYY').")

    @staticmethod
    def validate_priority(priority):

        if priority not in {"низкий", "средний", "высокий"}:
            logger.error("Неверный тип данных для приоритета задачи")
            raise ValueError("Приоритет задачи должен быть 'низкий', 'средний' или 'высокий'")
        
        return priority

    @staticmethod
    def validate_status(status):

        if status not in {"выполнено", "не выполнено"}:
            logger.error("Неверный тип данных для статуса задачи")
            raise ValueError("Статус задачи должен быть 'выполнено' или 'не выполнено'")
        return status   

    def save_json(self):
        """
        Сохраняет задачи в JSON-файл.
        """

        try:
            tasks_dict = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
            
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(tasks_dict, file, indent=4, ensure_ascii=False)

            logger.info("Задачи сохранены в %s", self.filename)
            print(f"Задачи сохранены в {self.filename}")

        except Exception as e:
            logger.error("Не удалось сохранить задачи: %s", e)
            print("Произошла ошибка при сохранении задач:", e)

    def load_json(self):
        """
        Загружает задачи из JSON-файла.
        """
        if not os.path.exists(self.filename):
            logging.warning("Файл %s не найден. Создана пустая библиотека.", self.filename)
            self.tasks = {}
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                tasks_data = json.load(file)

            if not tasks_data:
                self.tasks = {}
                logger.info("Файл %s пуст. Создана пустая библиотека.", self.filename)
                return

            self.tasks = {}

            for task_id, data in tasks_data.items():
    
                data["due_date"] = datetime.strptime(data["due_date"], "%d.%m.%Y")
  
                task = Task(
                    title=data["title"],
                    description=data["description"],
                    category=data["category"],
                    due_date=data["due_date"],
                    priority=data["priority"],
                    status=data["status"]
                )
                
                task.id = task_id
                self.tasks[task_id] = task

            logger.info("Задачи загружены из %s", self.filename)

        except json.JSONDecodeError as e:
            logger.error("Ошибка при преобразовании данных в формат JSON: %s. Создана пустая библиотека.", e)
            self.tasks = {}

        except Exception as e:
            logger.error("Ошибка при загрузке задач: %s", e)
            self.tasks = {}