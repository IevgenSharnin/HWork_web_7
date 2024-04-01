from datetime import datetime
import faker
from random import randint, choice
from db_connection import session
from sqlalchemy.exc import SQLAlchemyError
from create_tables import Group, Student, Teacher, Course, Grade

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 33
NUMBER_TEACHERS = 5
NUMBER_COURSES = 8
NUMBER_GRADES_FOR_EACH_STUDENT = 20


def generate_fake_data_wo_rel():
    fake_data = faker.Faker()

    # Створимо набір груп 
    for gr in range(NUMBER_GROUPS):
        group = Group (
            group_name = f'group_{gr+1}'
        )
        session.add (group)

    # Згенеруємо викладачів
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(
            teacher_name = fake_data.name()
        )
        session.add (teacher)


def generate_fake_data_with_rel_courses_students():
    fake_data = faker.Faker()

    # Вибірка груп, вчителів що сформувалися раніше, щоб з них обрати пов'язане значення
    groups_exist = session.query (Group).all()
    teachers_exist = session.query (Teacher).all()

    # Генеруємо студентів, курси
    for _ in range(NUMBER_STUDENTS):
        student = Student (
            student_name = fake_data.name(),
            group_id = choice(groups_exist).id
        )
        session.add (student)

    for _ in range(NUMBER_COURSES):
        course = Course (
            course_name = fake_data.job(),
            teacher_id = choice(teachers_exist).id
        )
        session.add (course)
    

def generate_fake_data_with_rel_grades():
    fake_data = faker.Faker()

    # Вибірка студентів, курсів, що сформувалися раніше, щоб з них обрати пов'язане значення
    students_exist = session.query (Student).all()
    courses_exist = session.query (Course).all()

    # Генеруємо базу оцінок
    for _ in range(NUMBER_STUDENTS):
        for _ in range (NUMBER_GRADES_FOR_EACH_STUDENT):
            grade = Grade (
                grade_value = randint(2, 5),
                date_of = datetime(2023, randint (9, 12), randint(1, 30)).date(),
                student_id = choice (students_exist).id,
                course_id = choice (courses_exist).id
            )
            session.add (grade)

if __name__ == '__main__':
    try:
        generate_fake_data_wo_rel()
        session.commit()
        generate_fake_data_with_rel_courses_students()
        session.commit()
        generate_fake_data_with_rel_grades()
        session.commit()
        print ('\nТаблички успішно заповнено рандомними даними:')
        print (f' - {NUMBER_GROUPS} груп(-и);')
        print (f' - {NUMBER_STUDENTS} студентів;')
        print (f' - {NUMBER_TEACHERS} викладачів;')
        print (f' - {NUMBER_COURSES} предметів;')
        print (f' - {NUMBER_GRADES_FOR_EACH_STUDENT * NUMBER_STUDENTS} оцінок.\n')
    except SQLAlchemyError as e:
        print (e)
        session.rollback()
    finally:
        session.close()