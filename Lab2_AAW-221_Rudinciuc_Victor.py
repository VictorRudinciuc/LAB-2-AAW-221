import pickle
import datetime
import logging

class Logger:
    def __init__(self, filename="operations.log"):
        logging.basicConfig(filename=filename, level=logging.INFO)

    def log(self, message):
        logging.info(message)

logger = Logger()
#VictorRudinciuc
class StudyField:
    MECHANICAL_ENGINEERING = "MECHANICAL ENGINEERING"
    SOFTWARE_ENGINEERING = "SOFTWARE ENGINEERING"
    FOOD_TECHNOLOGY = "FOOD TECHNOLOGY"
    URBANISM = "URBANISM"
    ARCHITECTURE = "ARCHITECTURE"
    VETERINARY_MEDICINE = "VETERINARY MEDICINE"

class Student:
    def __init__(self, firstName, lastName, email, enrollmentDate, dateOfBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.enrollmentDate = enrollmentDate
        self.dateOfBirth = dateOfBirth
        self.faculty = None

class Faculty:
    def __init__(self, name, abbreviation, studyField):
        self.name = name
        self.abbreviation = abbreviation
        self.studyField = studyField
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        student.faculty = self

    def graduate_student(self, student):
        self.students.remove(student)
        student.faculty = None

    def display_students(self):
        for student in self.students:
            print(student.firstName, student.lastName)

    def is_student_in_faculty(self, student):
        return student in self.students

class University:
    def __init__(self):
        self.faculties = []

    def add_faculty(self, faculty):
        self.faculties.append(faculty)

    def find_student_faculty(self, email):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == email:
                    return faculty
        return None

    def display_faculties(self):
        for faculty in self.faculties:
            print(faculty.name)

    def display_faculties_by_field(self, field):
        for faculty in self.faculties:
            if faculty.studyField == field:
                print(faculty.name)

university = University()

class SaveManager:
    @staticmethod
    def save(university, filename="university.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(university, file)

    @staticmethod
    def load(filename="university.pkl"):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return University()

university = SaveManager.load()


while True:
    print("1. Add faculty")
    print("2. Add student to faculty")
    print("3. Graduate student from faculty")
    print("4. Display students in faculty")
    print("5. Display graduates from faculty")
    print("6. Check if student is in faculty")
    print("7. Find student's faculty")
    print("8. Display all faculties")
    print("9. Display faculties by field")
    print("10. Save university state")
    print("11. Batch enrollment")
    print("12. Batch graduation")
    print("0. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 0:
        if input("Do you want to save before exit? (y/n) ") == "y":
            SaveManager.save(university)
        break
    elif choice == 1:
        name = input("Enter faculty name: ")
        abbreviation = input("Enter faculty abbreviation: ")
        studyField = input("Enter study field: ")
        faculty = Faculty(name, abbreviation, studyField)
        university.add_faculty(faculty)
    elif choice == 2:
        faculty_name = input("Enter faculty name: ")
        first_name = input("Enter student first name: ")
        last_name = input("Enter student last name: ")
        email = input("Enter student email: ")
        enrollment_date = datetime.datetime.now()
        date_of_birth = input("Enter student date of birth (yyyy-mm-dd): ")
        date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
        student = Student(first_name, last_name, email, enrollment_date, date_of_birth)
        for faculty in university.faculties:
            if faculty.name == faculty_name:
                faculty.add_student(student)
                break
       
    elif choice == 3:
        faculty_name = input("Enter faculty name: ")
        email = input("Enter student email: ")
        for faculty in university.faculties:
            if faculty.name == faculty_name:
                for student in faculty.students:
                    if student.email == email:
                        faculty.graduate_student(student)
                        print(f"Student {student.firstName} {student.lastName} has graduated from {faculty.name}")
                        break
    elif choice == 4:
        faculty_name = input("Enter faculty name: ")
        for faculty in university.faculties:
            if faculty.name == faculty_name:
                print(f"Students in {faculty.name}:")
                faculty.display_students()
    elif choice == 5:
        
        faculty_name = input("Enter faculty name: ")
        for faculty in university.faculties:
            if faculty.name == faculty_name:
                print(f"Graduates from {faculty.name}:")
                faculty.display_graduates()
    elif choice == 6:
        faculty_name = input("Enter faculty name: ")
        email = input("Enter student email: ")
        for faculty in university.faculties:
            if faculty.name == faculty_name:
                for student in faculty.students:
                    if student.email == email:
                        print(f"Student {student.firstName} {student.lastName} is in {faculty.name}")
                        break
    elif choice == 7:
        email = input("Enter student email: ")
        faculty = university.find_student_faculty(email)
        if faculty:
            print(f"Student belongs to {faculty.name}")
        else:
            print("Student not found in any faculty")
    elif choice == 8:
        print("All faculties:")
        university.display_faculties()
    elif choice == 9:
        field = input("Enter field: ")
        print(f"Faculties in field {field}:")
        university.display_faculties_by_field(field)
    elif choice == 10:
        SaveManager.save(university)
        logger.log("Saved university state")
        print("University state saved.")
    elif choice == 11:
        filename = input("Enter filename for batch enrollment: ")
        with open(filename, "r") as file:
            for line in file:
                first_name, last_name, email, date_of_birth, faculty_name = line.strip().split(",")
                date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
                student = Student(first_name, last_name, email, datetime.datetime.now(), date_of_birth)
                for faculty in university.faculties:
                    if faculty.name == faculty_name:
                        faculty.add_student(student)
                        logger.log(f"Enrolled student {email} to {faculty_name}")
                        print(f"Enrolled student {email} to {faculty_name}")
                        break
                else:
                    print(f"Cannot enroll student {email}: Faculty {faculty_name} not found")
                    logger.log(f"Failed to enroll student {email}: Faculty {faculty_name} not found")
    elif choice == 12:
        filename = input("Enter filename for batch graduation: ")
        with open(filename, "r") as file:
            for line in file:
                email, faculty_name = line.strip().split(",")
                for faculty in university.faculties:
                    if faculty.name == faculty_name:
                        for student in faculty.students:
                            if student.email == email:
                                faculty.graduate_student(student)
                                logger.log(f"Graduated student {email} from {faculty_name}")
                                print(f"Graduated student {email} from {faculty_name}")
                                break
                        else:
                            print(f"Cannot graduate student {email}: Student not found in {faculty_name}")
                            logger.log(f"Failed to graduate student {email}: Student not found in {faculty_name}")
                    break
                else:
                    print(f"Cannot graduate student {email}: Faculty {faculty_name} not found")
                    logger.log(f"Failed to graduate student {email}: Faculty {faculty_name} not found")
