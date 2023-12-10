import random
from faker import Faker
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Group, Subject, Grade

fake = Faker('uk-UA')



def insert_student():
    for _ in range(1, 30):
        student = Student(
            fullname=fake.name()
        )
        session.merge(student)


def insert_teacher():
    for _ in range(1, 4):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.merge(teacher)


def insert_group():
    groups = ['Group A', 'Group B', 'Group C']
    for group_name in groups:
        group = Group(name=group_name)
        session.merge(group)



def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(1, 20)):
                grade = Grade(
                    student_id=student.id,
                    grade_date=fake.date_this_decade(),
                    subject_id=subject.id,
                    grade=random.randint(1, 12)
                )
                session.merge(grade)  # merge (оновлює дані) add ( додає до існуючих )


def kick_students_null():  # згодом видалити
    students_to_delete = session.query(Student).filter(or_(Student.group_id is None, Student.group_id.is_(None))).all()

    try:
        for student in students_to_delete:
            session.delete(student)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def insert_subject():
    teachers = session.query(Teacher).all()
    subjects = ['Mathematics', 'Physics', 'Biology', 'Chemistry', 'History']

    for idx, subject_name in enumerate(subjects):
        teacher = teachers[idx % len(teachers)]

        subject = Subject(
            name=subject_name,
            teacher_id=teacher.id
        )
        session.merge(subject)


if __name__ == '__main__':
    try:

        """if null kick nah :D"""
        # kick_students_null()
        # session.commit()

        """Create db"""
        # get_random_group()
        # insert_student()
        # session.commit()
        # insert_teacher()
        # session.commit()
        # insert_group()
        # session.commit()
        # insert_subject()
        # session.commit()
        insert_grades()
        session.commit()

        """if teachers null -> nah :D"""
        # session.query(Subject).filter(Subject.teacher_id == None).delete()
        # session.commit()

        """Delete all db"""
        # session.query(Grade).delete()
        # session.commit()
        # session.query(Student).delete()
        # session.commit()
        # session.query(Teacher).delete()
        # session.commit()
        # session.query(Subject).delete()
        # session.commit()
        # session.query(Group).delete()
        # session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
