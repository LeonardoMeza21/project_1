from PyQt6.QtWidgets import QApplication
from student_grade_logic import StudentGrade

def main():
    application = QApplication([])
    window = StudentGrade()
    window.show()
    application.exec()

if __name__ == '__main__':
    main()
