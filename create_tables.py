from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(20), nullable=False, unique=True)

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(150), nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_name = Column(String(150), nullable=False)
    group_id = Column(ForeignKey('groups.id', ondelete='CASCADE'), nullable = False)
    group = relationship('Group')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(150), nullable=False)
    teacher_id = Column(ForeignKey('teachers.id', ondelete='CASCADE'), nullable = False)
    teacher = relationship('Teacher')

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade_value = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    student_id = Column(ForeignKey('students.id'), nullable = False)
    student = relationship('Student')
    course_id = Column(ForeignKey('courses.id'), nullable = False)
    course = relationship('Course')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
