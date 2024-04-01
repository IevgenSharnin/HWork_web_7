from datetime import datetime
from random import randint, choice
from db_connection import session
from sqlalchemy import select, and_, desc, func
from sqlalchemy.exc import SQLAlchemyError
from create_tables import Group, Student, Teacher, Course, Grade

# Вибір випадкових значень з бази для використання у запитах
courses_exist = session.query (Course).all()
random_course_id = choice(courses_exist).id

teachers_exist = session.query (Teacher).all()
random_teacher_id = choice(teachers_exist).id

groups_exist = session.query (Group).all()
random_group_id = choice(groups_exist).id

students_exist = session.query (Student).all()
random_student_id = choice(students_exist).id

def select_1():
    return session.query(
        Student.student_name, func.round(func.avg(Grade.grade_value), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.student_name).order_by(desc('avg_grade')).limit(5).all()

def select_2():
    return session.query(
        Course.course_name, Student.student_name, func.round(func.avg(Grade.grade_value), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).join(Course).where(Course.id == random_course_id)\
        .group_by(Course.course_name, Student.student_name)\
        .order_by(desc('avg_grade')).limit(1).all()
    
def select_3():
    return session.query(
        Course.course_name, Group.group_name, func.round(func.avg(Grade.grade_value), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).join(Group).join(Course).where(Course.id == random_course_id)\
        .group_by(Group.group_name, Course.course_name).order_by(Group.group_name).all()

def select_4():
    return session.query(
        func.round(func.avg(Grade.grade_value), 2).label('avg_grade'))\
        .select_from(Grade).all()

def select_5():
    return session.query(
        Teacher.teacher_name, Course.course_name)\
        .select_from(Teacher).join(Course).where(Teacher.id == random_teacher_id)\
        .order_by(Course.course_name).all()

def select_6():
    return session.query(
        Group.group_name, Student.student_name)\
        .select_from(Group).join(Student).where(Group.id == random_group_id)\
        .order_by(Student.student_name).all()

def select_7():
    return session.query(
        Course.course_name, Group.group_name, Student.student_name, Grade.date_of, Grade.grade_value)\
        .select_from(Grade).join(Student).join(Group).join(Course)\
        .where(Group.id == random_group_id, Course.id == random_course_id).order_by(Student.student_name).all()

def select_8():
    return session.query(
        Teacher.teacher_name, Course.course_name, func.round(func.avg(Grade.grade_value), 2).label('avg_grade'))\
        .select_from(Grade).join(Course).join(Teacher).where(Teacher.id == random_teacher_id)\
        .group_by(Teacher.teacher_name, Course.course_name).order_by(Course.course_name).all()

def select_9():
    return session.query(
        Student.student_name, Course.course_name)\
        .select_from(Grade).join(Student).join(Course).where(Student.id == random_student_id)\
        .group_by(Student.student_name, Course.course_name).order_by(Course.course_name).all()

def select_10():
    return session.query(
        Teacher.teacher_name, Student.student_name, Course.course_name)\
        .select_from(Grade).join(Student).join(Course).join(Teacher)\
        .where(Teacher.id == random_teacher_id, Student.id == random_student_id)\
        .group_by(Teacher.teacher_name, Student.student_name, Course.course_name).order_by(Course.course_name).all()

def select_11():
    return session.query(
        Teacher.teacher_name, Student.student_name, func.round (func.avg (Grade.grade_value), 2))\
        .select_from(Grade).join(Student).join(Course).join(Teacher)\
        .where(Teacher.id == random_teacher_id, Student.id == random_student_id)\
        .group_by(Teacher.teacher_name, Student.student_name).all()

def select_12():
    answer = session.query(
        Course.course_name, Group.group_name, Student.student_name, Grade.date_of, Grade.grade_value)\
        .select_from(Grade).join(Student).join(Group).join(Course)\
        .where(Group.id == random_group_id, Course.id == random_course_id).order_by(desc(Grade.date_of)).all()
    last_date_grades = []
    last_date_grades.append (answer[0])
    for each in answer[1:]:
        if each[-2] == last_date_grades[0][-2]:
            last_date_grades.append (each)
        else: 
            break
    return last_date_grades

queries = {}
queries.update ({'1': ["1) Знайти 5 студентів із найбільшим середнім балом з усіх предметів.", select_1]})
queries.update ({'2': ["2) Знайти студента із найвищим середнім балом з певного предмета.", select_2]})
queries.update ({'3': ["3) Знайти середній бал у групах з певного предмета.", select_3]})
queries.update ({'4': ["4) Знайти середній бал на потоці (по всій таблиці оцінок).", select_4]})
queries.update ({'5': ["5) Знайти які курси читає певний викладач.", select_5]})
queries.update ({'6': ["6) Знайти список студентів у певній групі.", select_6]})
queries.update ({'7': ["7) Знайти оцінки студентів у окремій групі з певного предмета.", select_7]})
queries.update ({'8': ["8) Знайти середній бал, який ставить певний викладач зі своїх предметів.", select_8]})
queries.update ({'9': ["9) Знайти список курсів, які відвідує студент.", select_9]})
queries.update ({'10': ["10) Список курсів, які певному студенту читає певний викладач.", select_10]})
queries.update ({'11': ["11) Середній бал, який певний викладач ставить певному студентові.", select_11]})
queries.update ({'12': ["12) Оцінки студентів у певній групі з певного предмета на останньому занятті.", select_12]})

if __name__ == '__main__':
    print ('\nДля виведення доступні наступні запити:')
    for number, query in queries.items():
        print (query[0])
    
    number = input ('\nВведіть номер запиту або щось інше для виходу: ')
    print ('Якщо у запиті "певний" чи "окремий", виводжу по рандомному значенню у базі.\n')
    try:
        if int (number) in range (1, len(queries)+1):
            answers_as_list = queries[number][-1]
            for row_number in answers_as_list():
                print (row_number)
    except SQLAlchemyError as e:
        print (e)
    except ValueError:
        pass
