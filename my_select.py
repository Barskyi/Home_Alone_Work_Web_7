from sqlalchemy import func, desc, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():  # Find the 5 students with the highest GPA in all subjects.
    """
    select
s.id,
s.fullname,
ROUND(AVG(g.grade), 2) as average_grade
    from students s
    join grades g on s.id = g.student_id
    group by s.id
    order by average_grade desc
    limit 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():  # Find the students with the highest GPA in a particular subject.
    """
    select
s.id,
s.fullname,
    ROUND(AVG(g.grade), 2) as average_grade
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 1
    group by s.id
    order by average_grade desc
    limit 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 83).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result


def select_03():  # Find the average score in groups for a particular subject.
    """
SELECT
    g.subject_id,
    s.group_id,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM
    grades g
JOIN
    students s ON g.student_id = s.id
JOIN
    subjects sub ON g.subject_id = sub.id
WHERE
    sub.name = 'Chemistry'
GROUP BY
    g.subject_id,
    s.group_id;
    """

    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label("average_grade")) \
        .join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.name == 'Chemistry').group_by(Student.group_id).all()
    return result


def select_04():  # Find the average score on a thread the entire grade table.
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
FROM grades;
    :return:
    """
    result = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    return result


def select_05():  # Find which courses a particular teacher teaches.
    """
    SELECT
    teachers.fullname AS teacher_name,
    subjects.name AS course_name
FROM
    teachers
JOIN
    subjects ON teachers.id = subjects.teacher_id;
    :return:
    """
    result = session.query(Teacher.fullname.label("teacher_name"), Subject.name.label("course_name")) \
        .join(Subject, Teacher.id == Subject.teacher_id) \
        .all()
    return result


def select_06():  # Find a list of students in a specific group.
    """
    SELECT students.id, students.fullname, groups.name AS group_name
FROM students
JOIN groups ON students.group_id = groups.id;
    :return:
    """
    result = session.query(Student.id, Student.fullname, Group.name.label("group_name")) \
        .join(Group, Student.group_id == Group.id).all()
    return result


def select_07():  # Find students grades in a separate group for a specific subject.
    """
    SELECT students.fullname, grades.grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON subjects.id = grades.subject_id
JOIN groups ON students.group_id = groups.id
WHERE groups.name = 'Group B' AND subjects.name = 'Mathematics';

    :return:
    """
    result = session.query(Student.fullname, Grade.grade).join(Grade).join(Subject).join(Group).filter(
        and_(Group.name == "Group A", Subject.name == "Mathematics")).all()
    return result


def select_08():  # Find the average grade given by a particular teacher in his/her subjects.
    """
    SELECT teachers.fullname AS teacher_name, round(AVG(grades.grade),2) AS average_grade
FROM teachers
JOIN subjects ON teachers.id = subjects.teacher_id
JOIN grades ON subjects.id = grades.subject_id
GROUP BY teachers.fullname;
    :return:
    """
    result = (session.query(Teacher.fullname.label("teacher_name"),
                            func.round(func.avg(Grade.grade), 2).label("average_grade"))
              .join(Subject, Teacher.id == Subject.teacher_id)) \
        .join(Grade, Subject.id == Grade.subject_id).group_by(Teacher.fullname).all()
    return result


def select_09():  # Find a list of courses taken by a particular student.
    """
    SELECT id, fullname FROM students;

SELECT students.fullname, subjects.name AS course_name
FROM students
JOIN groups ON students.group_id = groups.id
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.id = 454
    :return:
    """
    result = (
        session.query(Student.fullname, Subject.name.label("course_name"))
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Student.id == 454)
        .all()
    )
    return result


def select_10():  # List of courses taught by a certain teacher to a certain student.
    """
    SELECT s.fullname AS student_name, t.fullname AS teacher_name, su.name AS subject_name
FROM students s
JOIN groups g ON s.group_id = g.id
JOIN grades gr ON gr.student_id = s.id
JOIN subjects su ON gr.subject_id = su.id
JOIN teachers t ON su.teacher_id = t.id
WHERE s.id = 454;

    :return:
    """
    result = (
        session.query(
            Student.fullname.label("student_name"),
            Teacher.fullname.label("teacher_name"),
            Subject.name.label("subject_name")
        )
        .join(Group, Student.group_id == Group.id)
        .join(Grade, Student.id == Grade.student_id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Student.id == 454)
        .all()
    )
    return result


if __name__ == '__main__':
    info_menu = ("1 -> Find the 5 students with the highest GPA in all subjects.\n"
                 "2 -> Find the students with the highest GPA in a particular subject.\n"
                 "3 -> Find the average score in groups for a particular subject.\n"
                 "4 -> Find the average score on a thread the entire grade table.\n"
                 "5 -> Find which courses a particular teacher teaches.\n"
                 "6 -> Find a list of students in a specific group.\n"
                 "7 -> Find students grades in a separate group for a specific subject.\n"
                 "8 -> Find the average grade given by a particular teacher in his/her subjects.\n"
                 "9 -> Find a list of courses taken by a particular student.\n"
                 "10 -> List of courses taught by a certain teacher to a certain student.\n")
    while True:
        choice = input(
            "Enter the number of the query you want to execute (1-10), or 'exit' to quit or 0 to call info menu: ")

        if choice.lower() == 'exit':
            break

        try:
            choice = int(choice)
            if choice == 1:
                print("<--------------------------------------------------------->")
                print(f"Five best students \n{select_01()}")
                print("<--------------------------------------------------------->")
            elif choice == 2:
                print("<--------------------------------------------------------->")
                print(select_02())
                print("<--------------------------------------------------------->")
            elif choice == 3:
                print("<--------------------------------------------------------->")
                print(select_03())
                print("<--------------------------------------------------------->")
            elif choice == 4:
                print("<--------------------------------------------------------->")
                print(select_04())
                print("<--------------------------------------------------------->")
            elif choice == 5:
                print("<--------------------------------------------------------->")
                print(select_05())
                print("<--------------------------------------------------------->")
            elif choice == 6:
                print("<--------------------------------------------------------->")
                print(select_06())
                print("<--------------------------------------------------------->")
            elif choice == 7:
                print("<--------------------------------------------------------->")
                print(select_07())
                print("<--------------------------------------------------------->")
            elif choice == 8:
                print("<--------------------------------------------------------->")
                print(select_08())
                print("<--------------------------------------------------------->")
            elif choice == 9:
                print("<--------------------------------------------------------->")
                print(select_09())
                print("<--------------------------------------------------------->")
            elif choice == 10:
                print("<--------------------------------------------------------->")
                print(select_10())
                print("<--------------------------------------------------------->")
            elif choice == 0:
                print(info_menu)
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number or 'exit'.")  # TODO: потрібно гарно все оформити!
