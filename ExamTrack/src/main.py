import sys
from datetime import datetime
from services import services

def safe_int_input(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Ошибка ввода: требуется ввести целое число (ID). Попробуйте снова.")

def safe_str_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка ввода: строка не может быть пустой. Попробуйте снова.")

def safe_date_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Ошибка ввода: неверный формат даты. Используйте ГГГГ-ММ-ДД (например, 2026-12-31).")

def admin_menu(user):
    while True:
        print(f"\n--- Меню Администратора ({user.login}) ---")
        print("1. Сформировать ведомость")
        print("0. Выйти")
        
        choice = safe_str_input("Выберите действие: ")
        
        if choice == "1":
            try:
                group_id = safe_int_input("ID группы: ")
                subject_id = safe_int_input("ID дисциплины: ")
                teacher_id = safe_int_input("ID преподавателя: ")
                exam_date = safe_date_input("Дата экзамена (YYYY-MM-DD): ")
                
                services.create_statement(user, group_id, subject_id, teacher_id, exam_date)
                print("Успех: Ведомость успешно сформирована")
            except Exception as e:
                print(f"Ошибка бизнес-логики: {e}")
                
        elif choice == "0":
            break
        else:
            print("Ошибка: Неверный пункт меню.")

def teacher_menu(user):
    while True:
        print(f"\n--- Меню Преподавателя ({user.login}) ---")
        print("1. Поставить оценку")
        print("0. Выйти")
        
        choice = safe_str_input("Выберите действие: ")
        
        if choice == "1":
            try:
                statement_id = safe_int_input("ID ведомости: ")
                student_id = safe_int_input("ID студента: ")
                mark = safe_str_input("Оценка (2, 3, 4, 5 или 'н/я'): ")
                
                # Запрашиваем заметку 
                note = input("Заметка (необязательно, нажмите Enter для пропуска): ").strip()
                if not note:
                    note = None
                
                services.set_student_mark(user, statement_id, student_id, mark, note)
                print("Успех: Оценка и заметка успешно сохранены")
            except Exception as e:
                print(f"Ошибка бизнес-логики: {e}")
                
        elif choice == "0":
            break
        else:
            print("Ошибка: Неверный пункт меню.")

def main():
    while True:
        print("\n=== Система ExamTrack ===")
        login = safe_str_input("Логин: ")
        password = safe_str_input("Пароль: ")
        
        try:
            user = services.authenticate(login, password)
            if user.role == "Администратор":
                admin_menu(user)
            elif user.role == "Преподаватель":
                teacher_menu(user)
            else:
                print("Ошибка: Неизвестная роль пользователя.")
        except Exception as e:
            print(f"Ошибка входа: {e}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n Программа безопасно завершена. До свидания!")
        sys.exit(0)
