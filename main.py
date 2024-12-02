import argparse
from datetime import datetime

from tasks.task_manager import TaskManager


def main():

    filename = input("Введите имя файла: ")

    task_manager = TaskManager(filename)

    parser = argparse.ArgumentParser(description="Менеджер Задач")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Добавление задачи
    add_parser = subparsers.add_parser("add", help="Добавить задачу")
    add_parser.add_argument("--title", required=True, help="Название задачи")
    add_parser.add_argument("--description", required=True, help="Описание задачи")
    add_parser.add_argument("--category", required=True, help="Категория задачи")
    add_parser.add_argument("--due_date", type=int, required=True, help="Срок выполнения задачи (в днях)")
    add_parser.add_argument("--priority", choices=["низкий", "средний", "высокий"], default="средний", help="Приоритет задачи")
    add_parser.add_argument("--status", choices=["выполнено", "не выполнено"], default="не выполнено", help="Статус выполнения задачи")

    # Удаление задачи
    delete_parser = subparsers.add_parser("delete", help="Удалить задачу")
    delete_parser.add_argument("--id", help="ID задачи")
    delete_parser.add_argument("--category", help="Категория задачи")

    # Просмотр задач
    view_parser = subparsers.add_parser("view", help="Просмотреть задачи")
    view_parser.add_argument("--category", help="Категория для фильтрации задачи")

    # Поиск задач
    search_parser = subparsers.add_parser("search", help="Поиск задач")
    search_parser.add_argument("--title", help="Название задачи")
    search_parser.add_argument("--description", help="Описание задачи")
    search_parser.add_argument("--category", help="Категория задачи")
    search_parser.add_argument("--priority", choices=["низкий", "средний", "высокий"], help="Приоритет задачи")
    search_parser.add_argument("--status", choices=["выполнено", "не выполнено"], help="Статус выполнения задачи")

    # Обновление задач
    update_parser = subparsers.add_parser("update", help="Обновить задачу")
    update_parser.add_argument("--id", required=True, help="ID задачи для обновления")
    update_parser.add_argument("--title", help="Новое название задачи")
    update_parser.add_argument("--description", help="Новое описание задачи")
    update_parser.add_argument("--category", help="Новая категория задачи")
    update_parser.add_argument("--due_date",  help="Новый срок выполнения задачи")
    update_parser.add_argument("--priority", choices=["низкий", "средний", "высокий"], help="Новый приоритет задачи")
    update_parser.add_argument("--status", choices=["выполнено", "не выполнено"], help="Новый статус выполнения задачи")

    # Сохранение задач
    save_parser = subparsers.add_parser("save", help="Сохранить задачи в JSON-файл")

    # Загрузка задач
    load_parser = subparsers.add_parser("load", help="Загрузить задачи из JSON-файла")

    args = parser.parse_args()

    if args.command == "add":
        
        task_manager.add_task(
            args.title,
            args.description,
            args.category,
            args.due_date,
            args.priority,
            args.status
        )

    elif args.command == "delete":
        
        if args.category:
            task_manager.delete_task_by_category(category=args.category)
            task_manager.save_json()
        elif args.id:
            task_manager.delete_task_by_id(task_id=args.id)
            task_manager.save_json()
        else:
            print("Укажите категорию или ID задачи для удаления")

    elif args.command == "view":

        task_list = task_manager.view_tasks(tasks=task_manager.tasks, category=args.category)
        print(task_list)

    elif args.command == "search":

        results = task_manager.search_task(
            title=args.title,
            description=args.description,
            category=args.category,
            priority=args.priority,
            status=args.status
        )

        if results:
            print("Результаты поиска:\n")
            print(task_manager.view_tasks({task.id: task for task in results}))
        else:
            print("Задачи не найдены.")

    elif args.command == "update":

        if args.due_date.isdigit():
            due_date = int(args.due_date)
        else:
            try:
                due_date = datetime.strptime(args.due_date, "%d.%m.%Y")
            except ValueError as e:
                raise ValueError ("Дата должна быть в формате YYYY-MM-DD или числом (количество дней до дедлайна)") from e
            
        
        task_manager.update_task(
            task_id=args.id,
            title=args.title,
            description=args.description,
            category=args.category,
            due_date=due_date,
            priority=args.priority,
            status=args.status)

        task_manager.save_json()
        print("Задача обновлена!")

    elif args.command == "save":

        task_manager.save_json()
        print("Задачи сохранены!")

    elif args.command == "load":

        task_manager.load_json()
    
    else:
        print("Неизвестная команда")
        parser.print_help()

if __name__ == "__main__":
    main()


    
    