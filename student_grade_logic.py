import csv
import os
import re

from PyQt6.QtWidgets import *
from gui import *


class StudentGrade(QMainWindow, Ui_Students_Grades_Window):
    def __init__(self) -> None:
        """
        Sets the default instance variables and initializes the number of attempts input,
        score input fields, labels, and error labels.
        """
        super().__init__()
        self.setupUi(self)
        self.student_name_input.setMaxLength(50)
        self.num_attempts_input.setRange(1, 4)
        self.num_attempts_input.valueChanged.connect(self.student_attempts)
        self.students_scores_input = [self.score_input_1, self.score_input_2, self.score_input_3, self.score_input_4]
        self.students_scores_label = [self.score_label_1, self.score_label_2, self.score_label_3, self.score_label_4]
        self.submit_pushButton.clicked.connect(self.submit)
        self.grades_results = [self.highest_grade_result_label, self.lowest_grade_result_label, self.average_grade_result_label]
        self.students_scores_error = [self.score_error_label_1, self.score_error_label_2, self.score_error_label_3, self.score_error_label_4]
        for i in self.students_scores_error:
            i.setStyleSheet("color: red;")
        self.hide_values_and_labels()
        self.student_name_error_label.setStyleSheet("color: red;")

    def hide_values_and_labels(self) -> None:
        """
        Hides the dynamic score input boxes, their labels and error messages,
        as well as the frame used for displaying final grade output.
        """
        for i  in self.students_scores_input[1:4]:
            i.hide()
        for j  in self.students_scores_label[1:4]:
            j.hide()
        for k  in self.students_scores_error[1:4]:
            k.hide()
        self.frame.hide()

    def student_attempts(self) -> None:
        """
        Displays the dynamic score input boxes, their labels and error messages,
        as well as the frame used for showing final grade output.
        """
        number_of_attempts = self.num_attempts_input.value()
        self.hide_values_and_labels()
        for j in range (number_of_attempts):
            self.students_scores_input[j].show()
            self.students_scores_label[j].show()
            self.students_scores_error[j].show()
            self.frame.show()

    def final_grade (self) -> None:
        """
        Calculates and displays the student's highest, lowest, and average grades
        based on all entered attempts and selected checkboxes.
        """
        for i in self.grades_results:
            i.clear()
        highest_grade = self.highest_grade_checkBox.isChecked()
        lowest_grade = self.lowest_grade_checkBox.isChecked()
        average_grade = self.average_grade_checkBox.isChecked()
        number_of_attempts = self.num_attempts_input.value()
        grades = []
        for j in range(number_of_attempts):
            students_scores_input = self.students_scores_input[j].text()
            try:
                grade = float(students_scores_input)
                grades.append(grade)
            except ValueError:
                continue
        if highest_grade and grades:
            high = max(grades)
            self.highest_grade_result_label.setText(f"High Score: {high:.2f}")
            self.highest_grade_result_label.setStyleSheet("color: green;")
        if lowest_grade and grades:
            low = min(grades)
            self.lowest_grade_result_label.setText(f"Low Score: {low:.2f}")
            self.lowest_grade_result_label.setStyleSheet("color: green;")
        if average_grade and grades:
            avg = sum(grades) / len(grades)
            self.average_grade_result_label.setText(f"Avg Score: {avg:.2f}")
            self.average_grade_result_label.setStyleSheet("color: green;")
        self.student_name_grade_label.setText(f"{self.student_name_input.text().strip()} Score: ")
        self.student_name_grade_label.setStyleSheet("color: green;")

    def submit(self) -> None:
        """
        Calls final_grade(), checks for runtime errors and displays error messages, saves user
        input to a CSV file, and resets the form after storing a student's grades.
        """
        student_name = self.student_name_input.text().strip()
        saved_scores = []
        number_of_attempts = self.num_attempts_input.value()
        if not student_name:
            self.student_name_error_label.setText("Please enter a student name.")
            self.student_name_input.clear()
            self.student_name_input.setFocus()
            return
        elif not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)*", student_name):
            self.student_name_error_label.setText("Only letters and single spaces are allowed.")
            self.student_name_input.clear()
            self.student_name_input.setFocus()
            return
        self.student_name_error_label.clear()
        for i in self.students_scores_error:
            i.setText("")
        for j in range(number_of_attempts):
            error_msg_input = self.students_scores_input[j].text()
            try:
                error_msg_checker = float(error_msg_input)
                if not 0 <= error_msg_checker <= 100:
                    self.students_scores_error[j].setText("Error: Enter a score btw 0 and 100")
                    self.students_scores_input[j].clear()
                    return
                else:
                    saved_scores.append(error_msg_checker)
                    continue
            except ValueError:
                self.students_scores_error[j].setText("Error: Enter score (numbers only)")
                self.students_scores_input[j].clear()
                return
        highest_score = max(saved_scores)
        lowest_score = min(saved_scores)
        average_score = sum(saved_scores) / len(saved_scores)
        write_header = not os.path.exists('data.csv') or os.path.getsize('data.csv') == 0
        with open('data.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Highest", "Lowest", "Average"])
            while len(saved_scores) < 4:
                saved_scores.append(0.0)
            row = [student_name] + saved_scores + [highest_score, lowest_score, average_score]
            writer.writerow(row)
        self.final_grade()
        for k in self.students_scores_input:
            k.clear()
        self.num_attempts_input.setValue(1)
        self.student_name_input.clear()
        self.student_name_input.setFocus()
        self.highest_grade_checkBox.setChecked(False)
        self.lowest_grade_checkBox.setChecked(False)
        self.average_grade_checkBox.setChecked(False)



