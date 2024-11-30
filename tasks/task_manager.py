import os
import logging

from tasks.task import Task

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers= [logging.FileHandler('logs/task_manager.log'),
               # logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self):
        
        self.tasks = {}

    def add_tasks(self, title: str, description: str, category: str, due_date: int):
        """
        Добавляет задачу в список задач
        """
        try:
            new_tasks = Task(title, description, category, due_date)
            self.tasks[new_tasks.id] = new_tasks
            logger.info("Добавлена задача: %s (Приоритет: %s, до %s)", title, new_tasks.priority, new_tasks.due_date.strftime('%d.%m.%Y'))

        except TypeError as e:
            logger.error("Ошибка при добавлении задачи: %s", e)
            raise
        except Exception as e:
            logger.error("Неизвестная ошибка при добавлении задачи: %s", e)
            raise

