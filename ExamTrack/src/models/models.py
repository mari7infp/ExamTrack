from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    login: str
    password_hash: str
    role: str
    created_at: str

@dataclass
class Teacher:
    id: int
    user_id: int
    full_name: str
    department: str
    email: str

@dataclass
class AcademicGroup:
    id: int
    code: str
    course: int
    faculty: str

@dataclass
class Subject:
    id: int
    title: str
    control_type: str
    semester: int
    hours: int

@dataclass
class Student:
    id: int
    group_id: int
    record_book_number: str
    full_name: str
    status: str
    email: str

@dataclass
class Statement:
    id: int
    group_id: int
    subject_id: int
    teacher_id: int
    semester: int
    exam_date: str
    status: str

@dataclass
class StatementResult:
    id: int
    statement_id: int
    student_id: int
    mark: Optional[int]
    mark_text: Optional[str]
    grade_date: Optional[str]
    note: Optional[str]