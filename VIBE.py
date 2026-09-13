#Orianna Romero
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator.

This program uses Option B: a Student class for each student record.
"""

from pathlib import Path


DATA_FILE = Path("student_grades.txt")


class Student:
	"""Store a student's scores and calculate their grade."""

	def __init__(self, name, student_id, test1, test2, test3,
				 average=None, grade=None):
		self.name = name
		self.student_id = student_id
		self.test1 = test1
		self.test2 = test2
		self.test3 = test3
		self.average = (test1 + test2 + test3) / 3
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (f"{self.name}|{self.student_id}|{self.test1:.2f}|"
				f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|"
				f"{self.grade}\n")


def is_escape(value):
	"""Return True when the user pressed the Escape key."""
	return value == "\x1b"


def prompt_text(message):
	"""Prompt for text and return None when the user requests exit."""
	value = input(message).strip()
	if is_escape(value):
		return None
	return value


def prompt_score(test_name):
	"""Prompt for a score from 0 through 100."""
	while True:
		value = input(f"{test_name} score (0-100, or ESC to exit): ").strip()
		if is_escape(value):
			return None
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Please enter a score between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and append one student record."""
	print("\nAdd Student (press ESC at any prompt to return to the menu)")
	name = prompt_text("Student name: ")
	if name is None:
		return
	student_id = prompt_text("Student ID: ")
	if student_id is None:
		return
	if not name or not student_id:
		print("Name and ID cannot be blank.")
		return

	scores = []
	for test_number in range(1, 4):
		score = prompt_score(f"Test {test_number}")
		if score is None:
			return
		scores.append(score)

	student = Student(name, student_id, *scores)
	students.append(student)
	print(f"Added {student.name}: average {student.average:.2f}, grade {student.grade}.")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 91)
	print(f"{'Name':<22}{'ID':<14}{'Test 1':>10}{'Test 2':>10}"
		  f"{'Test 3':>10}{'Average':>12}{'Grade':>8}")
	print("-" * 91)
	for student in students:
		print(f"{student.name:<22.22}{student.student_id:<14.14}"
			  f"{student.test1:>10.2f}{student.test2:>10.2f}"
			  f"{student.test3:>10.2f}{student.average:>12.2f}"
			  f"{student.grade:>8}")
	print("-" * 91)


def display_statistics(students):
	"""Display highest, lowest, and class average scores."""
	if not students:
		print("\nNo student records found.")
		return

	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students):
	"""Find and display students whose names contain the search text."""
	search_name = prompt_text("\nEnter a name to search (or ESC to return): ")
	if search_name is None:
		return
	matches = [student for student in students
			   if search_name.lower() in student.name.lower()]
	if not matches:
		print("No matching students found.")
		return
	display_students(matches)


def load_students(filename=DATA_FILE):
	"""Load student records from a pipe-delimited file."""
	students = []
	try:
		with filename.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					students.append(Student(fields[0], fields[1],
											float(fields[2]), float(fields[3]),
											float(fields[4])))
				except ValueError:
					print(f"Skipping invalid scores on line {line_number}.")
	except FileNotFoundError:
		print("No saved records found. Starting with an empty roster.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students, filename=DATA_FILE):
	"""Save all student records in the required pipe-delimited format."""
	try:
		with filename.open("w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Saved {len(students)} student record(s) to {filename}.")
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by student name")
	print("5. Save records")
	print("Press ESC to save and exit")


def main():
	"""Run the Student Grade Calculator menu loop."""
	students = load_students()
	while True:
		display_menu()
		choice = input("Choose an option: ").strip()
		if is_escape(choice):
			save_students(students)
			print("Goodbye!")
			return
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid choice. Please select 1 through 5 or press ESC.")


if __name__ == "__main__":
	main()


