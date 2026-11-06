import hashlib
from datetime import datetime
from models.models import User
from repositories.user_repository import UserRepository
from repositories.teacher_repository import TeacherRepository
from repositories.group_repository import GroupRepository
from repositories.subject_repository import SubjectRepository
from repositories.student_repository import StudentRepository
from repositories.statement_repository import StatementRepository
from repositories.statement_result_repository import StatementResultRepository

user_repo = UserRepository()
teacher_repo = TeacherRepository()
group_repo = GroupRepository()
subject_repo = SubjectRepository()
student_repo = StudentRepository()
statement_repo = StatementRepository()
result_repo = StatementResultRepository()

def authenticate(login: str, password_input: str) -> User:
    user = user_repo.get_by_login(login)
    if not user:
        raise Exception("Неверный логин или пароль")
        
    input_hash = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
    if user.password_hash != input_hash:
        raise Exception("Неверный логин или пароль")
        
    return user

def create_statement(user: User, group_id: int, subject_id: int, teacher_id: int, exam_date: str):
    if user.role != "Администратор":
        raise Exception("Требуются права администратора")

    group = group_repo.get_by_id(group_id)
    subject = subject_repo.get_by_id(subject_id)
    teacher = teacher_repo.get_by_id(teacher_id)
    
    if not group or not subject:
        raise Exception("Указанная группа или дисциплина не найдены")
    if not teacher:
        raise Exception("Указанный преподаватель не найден")

    semester = subject.semester

    if statement_repo.check_exists(group_id, subject_id, semester):
        raise Exception("Ведомость по данной дисциплине уже создана")

    active_students = student_repo.get_active_by_group(group_id)
    if not active_students:
        raise Exception("В выбранной группе нет активных студентов")

    statement_id = statement_repo.create(group_id, subject_id, teacher_id, semester, exam_date)
    
    student_ids = [s.id for s in active_students]
    result_repo.generate_empty_results(statement_id, student_ids)

def set_student_mark(user, statement_id: int, student_id: int, mark_value: str, note: str = None):
    if user.role != "Преподаватель":
        raise Exception("Действие разрешено только экзаменатору")
        
    statement = statement_repo.get_by_id(statement_id)
    if not statement or statement.status != "Открыта":
        raise Exception("Ведомость заблокирована или не существует")
        
    teacher = teacher_repo.get_by_user_id(user.id)
    if not teacher or statement.teacher_id != teacher.id:
        raise Exception("Вы не являетесь экзаменатором данной ведомости")
        
    valid_marks = ["2", "3", "4", "5", "н/я"]
    mark_str = str(mark_value).strip().lower()
    if mark_str not in valid_marks:
        raise Exception("Недопустимый формат оценки")
        
    mark_int = int(mark_str) if mark_str.isdigit() else None
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    
    is_updated = result_repo.update_mark(statement_id, student_id, mark_int, mark_str, current_date, note)
    
    if not is_updated:
        raise Exception("Студент с таким ID не числится в данной ведомости")