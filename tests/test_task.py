from datetime import datetime, timedelta

import pytest

from tasks.task import Task


def test_tash_creation():

    title = "Задача"
    description = "Описание задачи"
    category = "Категория"
    due_date = 1

    task = Task(title, description, category, due_date)

    assert task.title == title
    assert task.description == description
    assert task.category == category
    assert task.due_date.date() == (datetime.now() + timedelta(days=due_date)).date() and isinstance(task.due_date, datetime)
    assert task.priority == "средний"
    assert task.status == "не выполнено"

def test_invalid_title():

    with pytest.raises(ValueError, match="Задача не может быть пустой и должна быть строкой"):
        Task("", "Описание задачи", "Категория", 1)
    
    with pytest.raises(ValueError, match="Задача не может быть пустой и должна быть строкой"):
        Task(None, "Описание задачи", "Категория", 1)

def test_invalid_description():

    with pytest.raises(ValueError, match="Описание задачи не может быть пустым и должно быть строкой"):
        Task("Задача", "", "Категория", 1)
    
    with pytest.raises(ValueError, match="Описание задачи не может быть пустым и должно быть строкой"):
        Task("Задача", None, "Категория", 1)

def test_invalid_category():

    with pytest.raises(ValueError, match="Категория задачи не может быть пустой и должна быть строкой"):
        Task("Задача", "Описание задачи", "", 1)

    with pytest.raises(ValueError, match="Категория задачи не может быть пустой и должна быть строкой"):
        Task("Задача", "Описание задачи", None, 1)

def test_invalid_due_date():

    with pytest.raises(ValueError, match="Срок выполнения задачи не может быть пустой и должен быть числом"):
        Task("Задача", "Описание задачи", "Категория", None)

    with pytest.raises(ValueError, match="Срок выполнения задачи не может быть пустой и должен быть числом"):
        Task("Задача", "Описание задачи", "Категория", "1")

def task_to_dict():

    task = Task("Задача", "Описание задачи", "Категория", 1)
    task_dict = task.to_dict()

    assert task_dict["id"] == task.id
    assert task_dict["title"] == task.title
    assert task_dict["description"] == task.description
    assert task_dict["category"] == task.category
    assert task_dict["due_date"] == task.due_date.strftime('%d.%m.%Y')
    assert task_dict["priority"] == task.priority
    assert task_dict["status"] == task.status

def test_eq():

    task1 = Task("Задача", "Описание задачи", "Категория", 1)
    task2 = Task("Задача", "Описание задачи", "Категория", 1)

    assert task1 != task2

    task3 = Task("Задача", "Описание задачи", "Категория", 2)

    task1.id = task3.id

    assert task1 == task3