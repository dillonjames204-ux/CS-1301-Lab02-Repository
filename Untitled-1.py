FILENAME = "courses.txt"


class Course:
    def __init__(self, name, credits, grade):
        self.name = name
        self.credits = credits
        self.grade = grade

    def get_letter(self):
        if self.grade >= 90:
            return "A"
        elif self.grade >= 80:
            return "B"
        elif self.grade >= 70:
            return "C"
        elif self.grade >= 60:
            return "D"
        else:
            return "F"

    def get_points(self):
        letter = self.get_letter()
        if letter == "A":
            return 4
        elif letter == "B":
            return 3
        elif letter == "C":
            return 2
        elif letter == "D":
            return 1
        else:
            return 0

    def summary(self):
        return f"{self.name}: {self.credits} credits, {self.grade} ({self.get_letter()})"


class GradeBook:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def total_credits(self):
        total = 0
        for c in self.courses:
            total += c.credits
        return total

    def calculate_gpa(self):
        total_points = 0
        for c in self.courses:
            total_points += c.get_points() * c.credits
        credits = self.total_credits()
        if credits == 0:
            return 0
        return total_points / credits

    def display(self):
        print("\nYour courses:")
        for c in self.courses:
            print(c.summary())
        print(f"\nTotal credit hours: {self.total_credits()}")
        print(f"GPA: {self.calculate_gpa():.2f}")

    def save(self, filename):
        with open(filename, "w") as file:
            for c in self.courses:
                file.write(f"{c.name},{c.credits},{c.grade}\n")

    def load(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    name, credits, grade = line.strip().split(",")
                    self.add_course(Course(name, int(credits), float(grade)))
        except FileNotFoundError:
            pass


def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def ask_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


def main():
    book = GradeBook()
    book.load(FILENAME)
    print(f"Loaded {len(book.courses)} saved course(s).")

    while True:
        name = input("What course are you taking? (type done to finish) ")
        if name.lower() == "done":
            break

        credits = ask_int("How many credits is this course? ")
        grade = ask_float("What is your grade in the course? ")

        if grade < 0 or grade > 100:
            print("Grade must be between 0 and 100.")
            continue

        book.add_course(Course(name, credits, grade))

    book.save(FILENAME)
    book.display()


main()