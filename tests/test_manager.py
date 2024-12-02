import os
import json
import uuid
from datetime import datetime, timedelta

import pytest

from tasks.task_manager import TaskManager


class TestAddTask:

    @pytest.fixture
    def setup_manager(self):

        temp_file = "test.json"
        manager = TaskManager(temp_file)

        return manager

    def test_add_valid_with_datetime_due_date(self, setup_manager):

        manager = setup_manager
        due_date = datetime.now() + timedelta(days=7)
        manager.add_task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=due_date,
            priority="средний",
            status="не выполнено"
        )

        assert len(manager.tasks) == 1

        task_id = next(iter(manager.tasks))
        task = manager.tasks[task_id]

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.category == "Test Category"
        assert task.due_date == due_date
        assert task.priority == "средний"
        assert task.status == "не выполнено"

    def test_add_valid_with_int_due_date(self, setup_manager):

        manager = setup_manager

        manager.add_task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )

        assert len(manager.tasks) == 1

        task_id = next(iter(manager.tasks))
        task = manager.tasks[task_id]

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.category == "Test Category"
        assert task.due_date.date() == (datetime.now() + timedelta(days=7)).date()
        assert task.priority == "средний"
        assert task.status == "не выполнено"

    def test_add_invalid_due_date(self, setup_manager):

        manager = setup_manager

        with pytest.raises(TypeError, match="Срок выполнения задачи должен иметь тип datetime или int"):
            manager.add_task(
                title="Test Task",
                description="Test Description",
                category="Test Category",
                due_date="invalid",
                priority="средний",
                status="не выполнено"
            )

        assert len(manager.tasks) == 0

class TestDeleteTask:

    @pytest.fixture
    def setup_manager(self, tmp_path):
        
        temp_file = "test.json"
        manager = TaskManager(temp_file)
    
        return manager
    
    def test_delete_by_id(self, setup_manager):

        manager = setup_manager

        manager.add_task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )

        task_id = next(iter(manager.tasks))

        manager.delete_task_by_id(task_id)

        assert task_id not in manager.tasks

    def test_delete_by_id_invalid(self, setup_manager):

        manager = setup_manager
        invalid_id = str(uuid.uuid4())

        with pytest.raises(ValueError, match=f"Удаление задачи не удалось: задача с id {invalid_id} отсутствует в списке."):
            manager.delete_task_by_id(invalid_id)

    def test_delete_by_category(self, setup_manager):

        manager = setup_manager

        manager.add_task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )

        manager.delete_task_by_category("Test Category")

        assert len(manager.tasks) == 0

    def test_delete_by_category_invalid(self, setup_manager):

        manager = setup_manager

        with pytest.raises(ValueError, match="Удаление задачи не удалось: задачи с категорией Test Category не найдены"):
            manager.delete_task_by_category("Test Category")

class TestSearchTask:
    @pytest.fixture
    def setup_manager(self):

        temp_file = "test.json"
        manager = TaskManager(filename=temp_file)

        manager.add_task(
            title="Задача 1",
            description="Описание задачи 1",
            category="Работа",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )
        manager.add_task(
            title="Задача 2",
            description="Описание задачи 2",
            category="Личное",
            due_date=3,
            priority="высокий",
            status="не выполнено"
        )
        manager.add_task(
            title="Задача 3",
            description="Описание задачи 3",
            category="Спорт",
            due_date=1,
            priority="высокий",
            status="выполнено"
        )
        return manager

    def test_search_by_title(self, setup_manager):

        manager = setup_manager

        result = manager.search_task(title="Задача 1")

        assert len(result) == 1
        assert result[0].title == "Задача 1"

    def test_search_many(self, setup_manager):

        manager = setup_manager

        result = manager.search_task(title="Задача 1", category="Работа", priority="средний")

        assert len(result) == 1
        assert result[0].title == "Задача 1"
        assert result[0].category == "Работа"

    def test_search_no_results(self, setup_manager):

        manager = setup_manager

        result = manager.search_task(title="Задача 4")

        assert result == []

    def test_search_no_params(self, setup_manager):

        manager = setup_manager

        result = manager.search_task()

        assert result == []

    def test_search_invalid_params(self, setup_manager):

        manager = setup_manager

        with pytest.raises(TypeError, match="Title должен иметь строковый тип"):
            manager.search_task(title=1)

class TestUpdateTask:
    
    @pytest.fixture
    def setup_manager(self):

        temp_file = "test.json"
        manager = TaskManager(filename=temp_file)

        manager.add_task(
            title="Задача 1",
            description="Описание задачи 1",
            category="Работа",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )

        manager.add_task(
            title="Задача 2",
            description="Описание задачи 2",
            category="Личное",
            due_date=3,
            priority="высокий",
            status="не выполнено"
        )

        return manager

    def test_update(self, setup_manager):

        manager = setup_manager

        task_id = next(iter(manager.tasks))

        updated_task = manager.update_task(
            task_id=task_id,
            title="Обновленная задача",
            description="Обновленное описание задачи",
            category="Обновленная категория",
            due_date=14,
            priority="высокий",
            status="выполнено"
        )

        assert updated_task.title == "Обновленная задача"
        assert updated_task.description == "Обновленное описание задачи"
        assert updated_task.category == "Обновленная категория"
        assert updated_task.due_date.date() == (datetime.now() + timedelta(days=14)).date()
        assert updated_task.priority == "высокий"
        assert updated_task.status == "выполнено"

    def test_update_one_params(self, setup_manager):

        manager = setup_manager

        task_id = next(iter(manager.tasks))

        updated_task = manager.update_task(
            task_id=task_id,
            title="Обновленная задача"
        )

        assert updated_task.title == "Обновленная задача"
        assert updated_task.description == "Описание задачи 1"
        assert updated_task.category == "Работа"
        assert updated_task.due_date.date() == (datetime.now() + timedelta(days=7)).date()
        assert updated_task.priority == "средний"
        assert updated_task.status == "не выполнено"

    def test_update_no_exist_id(self, setup_manager):

        manager = setup_manager

        task_id = str(uuid.uuid4())

        with pytest.raises(KeyError, match=f"Задача с ID '{task_id}' не найдена."):
            manager.update_task(
                task_id=task_id,
                title="Обновленная задача"
            )
    
    def test_update_invalid_due_date(self, setup_manager):

        manager = setup_manager

        task_id = next(iter(manager.tasks))

        with pytest.raises(ValueError):
            manager.update_task(
                task_id=task_id,
                due_date="invalid"
            )

class TestSaveJson:
    
    @pytest.fixture
    def setup_manager(self):

        temp_file = "test_json.json"
        manager = TaskManager(filename=temp_file)

        manager.add_task(
            title="Задача 1",
            description="Описание задачи 1",
            category="Работа",
            due_date=7,
            priority="средний",
            status="не выполнено"
        )

        manager.add_task(
            title="Задача 2",
            description="Описание задачи 2",
            category="Личное",
            due_date=3,
            priority="высокий",
            status="не выполнено"
        )

        return manager

    def test_save_json(self, setup_manager):

        manager = setup_manager

        manager.save_json()

        assert os.path.exists("test_json.json")

        with open("test_json.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        assert len(data) == len(manager.tasks)

        for task_id, task in manager.tasks.items():

            assert data[task_id] == task.to_dict()

class TestLoadJson:
    @pytest.fixture
    def temp_json_file(self):
        
        temp_file = "tasks_load.json"
        return temp_file

    def test_load_create_empty(self, temp_json_file):
        
        manager = TaskManager(filename=str(temp_json_file))

        manager.load_json()

        assert manager.tasks == {}  # Список задач должен быть пустым

    