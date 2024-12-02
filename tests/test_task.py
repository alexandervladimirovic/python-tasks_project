from uuid import UUID
from datetime import datetime, timedelta

import pytest

from tasks.task import Task


class TestInitTask:

    def test_task_creation_with_int_due_data(self):

        task = Task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=7,
            priority="средний",
            status="выполнено"
        )

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.category == "Test Category"
        assert task.due_date.date() == (datetime.now() + timedelta(days=7)).date()
        assert task.priority == "средний"
        assert task.status == "выполнено"
        assert isinstance(task.id, str) and UUID(task.id)

    def test_task_creation_with_datetime_due_data(self):
        
        datetime_due_date = datetime(2024, 12, 15)

        task = Task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=datetime_due_date,
            priority="высокий",
            status="не выполнено"
        )

        assert task.due_date == datetime_due_date
        assert task.priority == "высокий"
        assert task.status == "не выполнено"

    def test_invalid_due_date(self):

        with pytest.raises(TypeError, match="Срок выполнения задачи должен иметь тип datetime или int"):
            Task(
                title="Test Task",
                description="Test Description",
                category="Test Category",
                due_date="invalid",
                priority="средний",
                status="выполнено"
            )
    
    def test_invalid_priority(self):

        with pytest.raises(ValueError, match="Приоритет задачи должен быть 'низкий', 'средний' или 'высокий'"):
            Task(
                title="Test Task",
                description="Test Description",
                category="Test Category",
                due_date=7,
                priority="invalid",
                status="выполнено"
            )

    def test_invalid_status(self):

        with pytest.raises(ValueError, match="Статус задачи должен быть 'выполнено' или 'не выполнено'"):
            Task(
                title="Test Task",
                description="Test Description",
                category="Test Category",
                due_date=7,
                priority="средний",
                status="invalid"
            )

class TestToDictTask:

    def test_to_dict_with_int_due_date(self):

        task = Task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=7,
            priority="средний",
            status="выполнено"
        )

        task_dict = task.to_dict()

        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["category"] == "Test Category"
        assert task_dict["due_date"] == (datetime.now() + timedelta(days=7)).strftime('%d.%m.%Y')
        assert task_dict["priority"] == "средний"
        assert task_dict["status"] == "выполнено"

    def test_to_dict_with_datetime_due_date(self):

        datetime_due_date = datetime(2024, 12, 15)

        task = Task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date=datetime_due_date,
            priority="высокий",
            status="не выполнено"
        )

        task_dict = task.to_dict()

        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["category"] == "Test Category"
        assert task_dict["due_date"] == datetime_due_date.strftime('%d.%m.%Y')
        assert task_dict["priority"] == "высокий"
        assert task_dict["status"] == "не выполнено"