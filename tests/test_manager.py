import pytest

from tasks.task_manager import TaskManager

class TestAddTask:
    
    @pytest.fixture
    def task_manager(self):

        manager = TaskManager()
        manager.tasks = {}

        return manager
    
    def test_add_task(self, task_manager, mocker):

        mock_logger = mocker.patch("tasks.task_manager.logger")

        task_manager.add_tasks("Задача", "Описание задачи", "Категория", 1)

        assert len(task_manager.tasks) == 1

        added_task = next(iter(task_manager.tasks.values()))

        assert added_task.title == "Задача"
        assert added_task.description == "Описание задачи"
        assert added_task.category == "Категория"

        mock_logger.info.assert_called_with(
            "Добавлена задача: %s (Приоритет: %s, до %s)",
            added_task.title,
            added_task.priority,
            added_task.due_date.strftime('%d.%m.%Y')
        )

    def test_add_value_error(self, task_manager, mocker):

        mock_logger = mocker.patch("tasks.task_manager.logger")

        with pytest.raises(ValueError):
            task_manager.add_tasks("", "Описание задачи", "Категория", 1)

        assert len(task_manager.tasks) == 0

        mock_logger.error.assert_called()

    def test_add_unknown_error(self, task_manager, mocker):

        mock_logger = mocker.patch("tasks.task_manager.logger")

        mocker.patch("tasks.task_manager.Task", side_effect=Exception("Неизвестная ошибка"))

        with pytest.raises(Exception):
            task_manager.add_tasks("Задача", "Описание задачи", "Категория", 1)

        assert len(task_manager.tasks) == 0

        mock_logger.error.assert_called_with("Неизвестная ошибка при добавлении задачи: %s", mocker.ANY)
                                            